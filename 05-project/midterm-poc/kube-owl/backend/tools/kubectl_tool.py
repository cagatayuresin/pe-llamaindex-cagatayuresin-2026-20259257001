"""
KubeOps Agent — Gerçek kubectl Aracı
Subprocess ile kubectl komutları çalıştırır (read-only whitelist).
"""

import logging
import subprocess
from llama_index.core.tools import FunctionTool

from ..utils.security import validate_kubectl_command, sanitize_kubectl_output
from ..api.system import get_active_session_details

logger = logging.getLogger(__name__)


def kubectl_exec(command: str) -> str:
    """
    Kubernetes cluster'ında kubectl komutu çalıştırır (SADECE okuma komutları).
    Cluster'daki pod, service, node durumlarını kontrol etmek için kullan.

    İzin verilen komutlar: get, describe, logs, top
    Örnek kullanım: "get pods -n default", "describe pod my-pod -n production", "logs my-pod --tail=50"

    Args:
        command: kubectl'den sonra gelecek komut (kubectl kelimesini yazma,
                 örn: "get pods -n default")

    Returns:
        kubectl komutunun çıktısı
    """
    logger.info(f"kubectl komutu çalıştırılıyor: kubectl {command}")

    # Güvenlik kontrolü
    is_valid, error_msg = validate_kubectl_command(command)
    if not is_valid:
        logger.warning(f"kubectl komutu engellendi: {command} — {error_msg}")
        return f"HATA: {error_msg}"

    try:
        session = get_active_session_details()
        output = ""
        exit_code = 0
        
        if session:
            # SSH ile uzaktan çalıştır
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                connect_kwargs = {
                    "hostname": session["host"],
                    "port": session.get("port", 22),
                    "username": session["username"],
                }
                if session.get("auth_type") == "key" and session.get("key_path"):
                    connect_kwargs["key_filename"] = session["key_path"]
                else:
                    connect_kwargs["password"] = session.get("password")
                
                client.connect(**connect_kwargs)
                full_command = f"kubectl {command}"
                stdin, stdout, stderr = client.exec_command(full_command, timeout=30)
                
                out = stdout.read().decode('utf-8')
                err = stderr.read().decode('utf-8')
                
                if out:
                    output = out
                if err:
                    if output:
                        output += f"\n--- stderr ---\n{err}"
                    else:
                        output = err
                        
                if not output:
                    output = "(komut çıktı üretmedi)"
                exit_code = stdout.channel.recv_exit_status()
                logger.info(f"SSH kubectl komutu tamamlandı (exit code: {exit_code})")
            finally:
                client.close()
        else:
            # Lokal çalıştır
            cmd_parts = ["kubectl"] + command.split()
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=30,
            )
            exit_code = result.returncode
    
            if result.stdout:
                output = result.stdout
            if result.stderr:
                if output:
                    output += f"\n--- stderr ---\n{result.stderr}"
                else:
                    output = result.stderr
    
            if not output:
                output = "(komut çıktı üretmedi)"
            logger.info(f"Lokal kubectl komutu tamamlandı (exit code: {exit_code})")

        # Hassas bilgileri maskele
        output = sanitize_kubectl_output(output)

        return output

    except subprocess.TimeoutExpired:
        error_msg = "kubectl komutu zaman aşımına uğradı (30 saniye)"
        logger.error(error_msg)
        return f"HATA: {error_msg}"
    except FileNotFoundError:
        error_msg = "kubectl komutu bulunamadı. kubectl'in kurulu ve PATH'te olduğundan emin olun."
        logger.error(error_msg)
        return f"HATA: {error_msg}"
    except Exception as e:
        error_msg = f"kubectl çalıştırma hatası: {str(e)}"
        logger.error(error_msg)
        return f"HATA: {error_msg}"


def get_kubectl_tool() -> FunctionTool:
    """FunctionTool olarak sarmalanmış gerçek kubectl aracını döndürür."""
    return FunctionTool.from_defaults(
        fn=kubectl_exec,
        name="kubectl_exec",
        description=(
            "Kubernetes cluster'ında kubectl komutu çalıştırır (SADECE okuma komutları). "
            "Cluster'daki pod, service, deployment, node durumlarını kontrol etmek için kullan. "
            "İzin verilen komutlar: get, describe, logs, top. "
            "Örnek: kubectl_exec('get pods -n default') veya kubectl_exec('describe pod my-pod -n production'). "
            "Komutun başına 'kubectl' yazma, sadece alt komutu yaz."
        ),
    )

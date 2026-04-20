"""
KubeOps Agent — Güvenlik Modülü
kubectl komut whitelist kontrolü ve sanitization.
"""

import logging
import re

logger = logging.getLogger(__name__)

# İzin verilen kubectl alt komutları (read-only)
ALLOWED_COMMANDS = ["get", "describe", "logs", "top"]

# Yasaklanan pattern'ler (injection, write operasyonları)
BLOCKED_PATTERNS = [
    "|", ">", ">>", "&&", "||", ";", "`", "$(", "${",
    "exec", "delete", "apply", "edit", "patch", "scale",
    "cordon", "drain", "taint", "label", "annotate",
    "port-forward", "cp", "attach", "run", "create",
    "replace", "rollout", "autoscale", "expose",
]


def validate_kubectl_command(command: str) -> tuple[bool, str]:
    """
    kubectl komutunu whitelist'e göre kontrol eder.

    Args:
        command: kubectl'den sonra gelecek komut string'i
                 (örn: "get pods -n default")

    Returns:
        (is_valid, error_message): Geçerliyse (True, ""),
                                   geçersizse (False, "hata açıklaması")
    """
    if not command or not command.strip():
        return False, "Boş komut gönderilemez."

    command = command.strip()

    # Blocked pattern kontrolü
    command_lower = command.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in command_lower:
            logger.warning(f"Engellenen kubectl komutu: {command} (pattern: {pattern})")
            return False, f"Bu komut güvenlik nedeniyle engellenmiştir. Yasaklanan pattern: '{pattern}'"

    # İlk kelime kontrolü (alt komut)
    parts = command.split()
    if not parts:
        return False, "Geçersiz komut formatı."

    sub_command = parts[0].lower()
    if sub_command not in ALLOWED_COMMANDS:
        logger.warning(f"İzin verilmeyen kubectl alt komutu: {sub_command}")
        return False, (
            f"'{sub_command}' komutu izin verilmiyor. "
            f"İzin verilen komutlar: {', '.join(ALLOWED_COMMANDS)}"
        )

    logger.info(f"kubectl komutu doğrulandı: {command}")
    return True, ""


def sanitize_kubectl_output(output: str) -> str:
    """
    kubectl çıktısından hassas bilgileri maskeler.

    Args:
        output: kubectl çıktı string'i

    Returns:
        Maskelenmiş çıktı
    """
    if not output:
        return output

    # Token ve secret değerlerini maskele
    sanitized = re.sub(
        r'(token|secret|password|api[_-]?key)\s*[:=]\s*\S+',
        r'\1: [REDACTED]',
        output,
        flags=re.IGNORECASE
    )

    # Base64 encoded data'yı maskele (uzun base64 string'leri)
    sanitized = re.sub(
        r'[A-Za-z0-9+/]{50,}={0,2}',
        '[BASE64_REDACTED]',
        sanitized
    )

    return sanitized

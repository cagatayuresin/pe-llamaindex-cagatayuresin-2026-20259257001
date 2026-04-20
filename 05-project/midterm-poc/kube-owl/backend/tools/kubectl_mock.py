"""
KubeOps Agent — Mock kubectl Aracı
Gerçek cluster yokken demo/test amaçlı sahte kubectl çıktıları üretir.
5 önceden tanımlanmış senaryo içerir.
"""

import logging
import re
from datetime import datetime, timedelta
from llama_index.core.tools import FunctionTool

from ..utils.security import validate_kubectl_command

logger = logging.getLogger(__name__)

# ============================================================
# SENARYO VERİLERİ
# ============================================================

# Ortak tarih/zaman değerleri
NOW = datetime.now()
AGO_1H = (NOW - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
AGO_2H = (NOW - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
AGO_30M = (NOW - timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
AGO_5M = (NOW - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
AGO_2D = (NOW - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
AGO_10D = (NOW - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ")

# ─── GET PODS ────────────────────────────────────────────────

PODS_DEFAULT = """NAME                              READY   STATUS             RESTARTS        AGE
api-server-7d9f8b6c4-x2k9l       0/1     CrashLoopBackOff   15 (2m ago)     3h
api-server-7d9f8b6c4-m3n7p       0/1     CrashLoopBackOff   12 (3m ago)     3h
worker-5c8d7e9f1-q4w8r            1/1     Running            0               10d
redis-6b4c9d8e2-j5k1s             1/1     Running            0               10d
nginx-ingress-8f7e6d5c3-p9q2r     1/1     Running            0               10d"""

PODS_PRODUCTION = """NAME                              READY   STATUS             RESTARTS        AGE
api-server-7d9f8b6c4-x2k9l       0/1     CrashLoopBackOff   15 (2m ago)     3h
api-server-7d9f8b6c4-m3n7p       0/1     CrashLoopBackOff   12 (3m ago)     3h
worker-5c8d7e9f1-q4w8r            1/1     Running            0               10d
redis-6b4c9d8e2-j5k1s             1/1     Running            0               10d"""

PODS_STAGING = """NAME                              READY   STATUS             RESTARTS   AGE
frontend-app-6a5b4c3d2-w1x2y     0/1     ImagePullBackOff   0          45m
frontend-app-6a5b4c3d2-z3a4b     0/1     ImagePullBackOff   0          45m
backend-api-9c8d7e6f5-h7g8i      1/1     Running            0          5d
postgres-db-2b3c4d5e6-k9l0m      1/1     Running            0          5d"""

PODS_MONITORING = """NAME                              READY   STATUS    RESTARTS   AGE
prometheus-server-7f8g9h0-a1b2   1/1     Running   0          15d
grafana-3d4e5f6g7-c3d4e           1/1     Running   0          15d
alertmanager-8h9i0j1k-f5g6h       1/1     Running   0          15d
node-exporter-l2m3n                1/1     Running   0          15d"""

PODS_KUBE_SYSTEM = """NAME                                    READY   STATUS    RESTARTS      AGE
coredns-5d78c9869d-j7k8l               1/1     Running   0             30d
coredns-5d78c9869d-m9n0o               1/1     Running   0             30d
etcd-master-1                           1/1     Running   0             30d
kube-apiserver-master-1                 1/1     Running   0             30d
kube-controller-manager-master-1        1/1     Running   0             30d
kube-proxy-p1q2r                        1/1     Running   0             30d
kube-proxy-s3t4u                        1/1     Running   0             30d
kube-scheduler-master-1                 1/1     Running   0             30d
calico-node-v5w6x                       1/1     Running   0             30d
calico-node-y7z8a                       1/1     Running   0             30d
pending-job-runner-4e5f6g7h-b9c0        0/1     Pending   0             20m"""

# ─── GET NODES ───────────────────────────────────────────────

NODES_OUTPUT = """NAME          STATUS     ROLES           AGE   VERSION
master-1      Ready      control-plane   30d   v1.28.4
worker-1      Ready      <none>          30d   v1.28.4
worker-2      NotReady   <none>          30d   v1.28.4
worker-3      Ready      <none>          30d   v1.28.4"""

# ─── DESCRIBE POD ────────────────────────────────────────────

DESCRIBE_API_SERVER = """Name:             api-server-7d9f8b6c4-x2k9l
Namespace:        production
Priority:         0
Service Account:  default
Node:             worker-1/10.0.1.11
Start Time:       {ago_3h}
Labels:           app=api-server
                  pod-template-hash=7d9f8b6c4
Status:           Running
IP:               10.244.1.15
Controlled By:    ReplicaSet/api-server-7d9f8b6c4
Containers:
  api-server:
    Container ID:   containerd://a1b2c3d4e5f6
    Image:          myregistry/api-server:v2.3.1
    Image ID:       myregistry/api-server@sha256:abc123
    Port:           8080/TCP
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    137
      Started:      {ago_5m}
      Finished:     {ago_2m}
    Ready:          False
    Restart Count:  15
    Limits:
      cpu:     500m
      memory:  256Mi
    Requests:
      cpu:     250m
      memory:  128Mi
    Environment:
      DATABASE_URL:  postgresql://db:5432/app
      REDIS_URL:     redis://redis:6379
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access
Conditions:
  Type              Status
  Initialized       True
  Ready             False
  ContainersReady   False
  PodScheduled      True
Events:
  Type     Reason     Age                 From               Message
  ----     ------     ----                ----               -------
  Normal   Scheduled  3h                  default-scheduler  Successfully assigned production/api-server-7d9f8b6c4-x2k9l to worker-1
  Normal   Pulled     2m (x15 over 3h)    kubelet            Container image "myregistry/api-server:v2.3.1" already present on machine
  Normal   Created    2m (x15 over 3h)    kubelet            Created container api-server
  Normal   Started    2m (x15 over 3h)    kubelet            Started container api-server
  Warning  BackOff    30s (x45 over 3h)   kubelet            Back-off restarting failed container api-server in pod api-server-7d9f8b6c4-x2k9l
  Warning  OOMKilling 2m                  kernel-monitor     Memory cgroup out of memory: Killed process 12345 (node) total-vm:524288kB, anon-rss:262144kB""".format(
    ago_3h=(NOW - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    ago_5m=AGO_5M,
    ago_2m=(NOW - timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ"),
)

DESCRIBE_FRONTEND = """Name:             frontend-app-6a5b4c3d2-w1x2y
Namespace:        staging
Priority:         0
Service Account:  default
Node:             worker-1/10.0.1.11
Start Time:       {ago_45m}
Labels:           app=frontend-app
                  pod-template-hash=6a5b4c3d2
Status:           Pending
IP:               10.244.1.20
Controlled By:    ReplicaSet/frontend-app-6a5b4c3d2
Containers:
  frontend:
    Container ID:
    Image:          myregistry/frontend-app:v3.0.0-beta
    Port:           3000/TCP
    State:          Waiting
      Reason:       ImagePullBackOff
    Ready:          False
    Restart Count:  0
    Limits:
      cpu:     200m
      memory:  256Mi
    Requests:
      cpu:     100m
      memory:  128Mi
    Environment:
      API_URL:  http://backend-api:8080
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access
Conditions:
  Type              Status
  Initialized       True
  Ready             False
  ContainersReady   False
  PodScheduled      True
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  45m                default-scheduler  Successfully assigned staging/frontend-app-6a5b4c3d2-w1x2y to worker-1
  Normal   Pulling    44m (x3 over 45m)  kubelet            Pulling image "myregistry/frontend-app:v3.0.0-beta"
  Warning  Failed     44m (x3 over 45m)  kubelet            Failed to pull image "myregistry/frontend-app:v3.0.0-beta": rpc error: code = NotFound desc = failed to pull and unpack image "myregistry/frontend-app:v3.0.0-beta": failed to resolve reference "myregistry/frontend-app:v3.0.0-beta": myregistry/frontend-app:v3.0.0-beta: not found
  Warning  Failed     44m (x3 over 45m)  kubelet            Error: ImagePullBackOff
  Normal   BackOff    5m (x120 over 45m) kubelet            Back-off pulling image "myregistry/frontend-app:v3.0.0-beta" """.format(
    ago_45m=(NOW - timedelta(minutes=45)).strftime("%Y-%m-%dT%H:%M:%SZ"),
)

DESCRIBE_NODE_WORKER2 = """Name:               worker-2
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    kubernetes.io/hostname=worker-2
                    kubernetes.io/os=linux
                    node.kubernetes.io/instance-type=m5.large
Annotations:        node.alpha.kubernetes.io/ttl: 0
CreationTimestamp:   {ago_30d}
Taints:             node.kubernetes.io/not-ready:NoSchedule
Conditions:
  Type                 Status    LastHeartbeatTime           Reason                       Message
  ----                 ------    -----------------           ------                       -------
  MemoryPressure       False     {ago_2h}                    KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure         False     {ago_2h}                    KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure          False     {ago_2h}                    KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready                False     {ago_2h}                    KubeletNotReady              PLEG is not healthy: pleg was last seen active 10m ago
Addresses:
  InternalIP:  10.0.1.12
  Hostname:    worker-2
Capacity:
  cpu:                4
  memory:             16384Mi
  pods:               110
Allocatable:
  cpu:                3800m
  memory:             15892Mi
  pods:               110
System Info:
  OS Image:                   Ubuntu 22.04.3 LTS
  Operating System:           linux
  Architecture:               amd64
  Container Runtime Version:  containerd://1.7.2
  Kubelet Version:            v1.28.4
  Kube-Proxy Version:         v1.28.4
Events:
  Type     Reason                   Age    From     Message
  ----     ------                   ----   ----     -------
  Warning  NodeNotReady             2h     kubelet  Node worker-2 status is now: NodeNotReady
  Warning  FailedNodeCondition      2h     kubelet  PLEG is not healthy""".format(
    ago_30d=(NOW - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    ago_2h=AGO_2H,
)

DESCRIBE_NODE_WORKER3 = """Name:               worker-3
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    kubernetes.io/hostname=worker-3
                    kubernetes.io/os=linux
Conditions:
  Type                 Status    LastHeartbeatTime     Reason                       Message
  ----                 ------    -----------------     ------                       -------
  MemoryPressure       False     {ago_5m}              KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure         True      {ago_5m}              KubeletHasDiskPressure       kubelet has disk pressure
  PIDPressure          False     {ago_5m}              KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready                True      {ago_5m}              KubeletReady                 kubelet is posting ready status
Capacity:
  cpu:                4
  memory:             16384Mi
  ephemeral-storage:  102400Mi
  pods:               110
Allocatable:
  cpu:                3800m
  memory:             15892Mi
  ephemeral-storage:  94580Mi
  pods:               110
Events:
  Type     Reason               Age   From     Message
  ----     ------               ----  ----     -------
  Warning  FreeDiskSpaceFailed  30m   kubelet  failed to garbage collect required amount of images
  Warning  EvictionThreshold    20m   kubelet  Attempting to reclaim ephemeral-storage
  Warning  Evicted              15m   kubelet  pod monitoring/node-exporter-l2m3n evicted due to DiskPressure""".format(
    ago_5m=AGO_5M,
)

DESCRIBE_PENDING_POD = """Name:             pending-job-runner-4e5f6g7h-b9c0
Namespace:        kube-system
Priority:         0
Service Account:  default
Node:             <none>
Labels:           app=job-runner
Status:           Pending
Controlled By:    ReplicaSet/pending-job-runner-4e5f6g7h
Containers:
  job-runner:
    Image:          myregistry/job-runner:v1.0.0
    Port:           <none>
    Limits:
      cpu:     8
      memory:  32Gi
      nvidia.com/gpu: 2
    Requests:
      cpu:     4
      memory:  16Gi
      nvidia.com/gpu: 2
Conditions:
  Type           Status
  PodScheduled   False
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  20m   default-scheduler  0/4 nodes are available: 1 node(s) had untolerable taint {node.kubernetes.io/not-ready: }, 3 Insufficient nvidia.com/gpu, 3 Insufficient memory."""

# ─── LOGS ────────────────────────────────────────────────────

LOGS_API_SERVER = """2025-03-29T10:15:22Z [INFO] Starting api-server v2.3.1...
2025-03-29T10:15:23Z [INFO] Connecting to database: postgresql://db:5432/app
2025-03-29T10:15:23Z [INFO] Database connection established
2025-03-29T10:15:24Z [INFO] Connecting to Redis: redis://redis:6379
2025-03-29T10:15:24Z [INFO] Redis connection established
2025-03-29T10:15:25Z [INFO] Loading ML model into memory...
2025-03-29T10:15:26Z [INFO] ML model loaded (245MB)
2025-03-29T10:15:27Z [INFO] Server listening on :8080
2025-03-29T10:15:30Z [INFO] Processing request: POST /api/predict
2025-03-29T10:15:31Z [INFO] Model inference completed (1.2s)
2025-03-29T10:15:35Z [WARN] Memory usage high: 240Mi / 256Mi (93.7%)
2025-03-29T10:15:36Z [INFO] Processing request: POST /api/predict
2025-03-29T10:15:37Z [INFO] Model inference completed (1.4s)
2025-03-29T10:15:38Z [FATAL] Out of memory: runtime: out of memory
2025-03-29T10:15:38Z [FATAL] goroutine 1 [running]:
runtime.throw({0x1234567, 0x15})
    /usr/local/go/src/runtime/panic.go:992 +0x71"""

LOGS_FRONTEND = """Error from server: container "frontend" in pod "frontend-app-6a5b4c3d2-w1x2y" is waiting to start: image can't be pulled"""

# ─── TOP ─────────────────────────────────────────────────────

TOP_PODS_DEFAULT = """NAME                              CPU(cores)   MEMORY(bytes)
api-server-7d9f8b6c4-x2k9l       45m          248Mi
api-server-7d9f8b6c4-m3n7p       38m          245Mi
worker-5c8d7e9f1-q4w8r            120m         89Mi
redis-6b4c9d8e2-j5k1s             30m          64Mi
nginx-ingress-8f7e6d5c3-p9q2r     15m          32Mi"""

TOP_PODS_PRODUCTION = """NAME                              CPU(cores)   MEMORY(bytes)
api-server-7d9f8b6c4-x2k9l       45m          248Mi
api-server-7d9f8b6c4-m3n7p       38m          245Mi
worker-5c8d7e9f1-q4w8r            120m         89Mi
redis-6b4c9d8e2-j5k1s             30m          64Mi"""

TOP_NODES = """NAME          CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
master-1      350m         17%    2048Mi          25%
worker-1      890m         44%    6144Mi          75%
worker-2      0m           0%     0Mi             0%
worker-3      1200m        60%    12288Mi         75%"""

# ─── EVENTS ──────────────────────────────────────────────────

EVENTS_DEFAULT = """LAST SEEN   TYPE      REASON              OBJECT                                    MESSAGE
2m          Warning   BackOff             pod/api-server-7d9f8b6c4-x2k9l           Back-off restarting failed container
2m          Warning   OOMKilling          pod/api-server-7d9f8b6c4-x2k9l           Memory cgroup out of memory: Killed process
3m          Warning   BackOff             pod/api-server-7d9f8b6c4-m3n7p           Back-off restarting failed container
5m          Normal    Pulled              pod/api-server-7d9f8b6c4-x2k9l           Container image already present on machine
10m         Normal    Started             pod/worker-5c8d7e9f1-q4w8r               Started container worker"""

EVENTS_PRODUCTION = EVENTS_DEFAULT

EVENTS_STAGING = """LAST SEEN   TYPE      REASON              OBJECT                                    MESSAGE
5m          Warning   Failed              pod/frontend-app-6a5b4c3d2-w1x2y         Failed to pull image "myregistry/frontend-app:v3.0.0-beta"
5m          Warning   Failed              pod/frontend-app-6a5b4c3d2-w1x2y         Error: ImagePullBackOff
5m          Warning   Failed              pod/frontend-app-6a5b4c3d2-z3a4b         Failed to pull image "myregistry/frontend-app:v3.0.0-beta"
10m         Normal    Pulling             pod/frontend-app-6a5b4c3d2-w1x2y         Pulling image "myregistry/frontend-app:v3.0.0-beta"
30m         Normal    Scheduled           pod/frontend-app-6a5b4c3d2-w1x2y         Successfully assigned staging/frontend-app-6a5b4c3d2-w1x2y"""

EVENTS_KUBE_SYSTEM = """LAST SEEN   TYPE      REASON              OBJECT                                    MESSAGE
20m         Warning   FailedScheduling    pod/pending-job-runner-4e5f6g7h-b9c0     0/4 nodes are available: insufficient resources
2h          Warning   NodeNotReady        node/worker-2                             Node worker-2 status is now: NodeNotReady
30m         Warning   EvictionThreshold   node/worker-3                             Attempting to reclaim ephemeral-storage"""

# ─── GET SERVICES / DEPLOYMENTS ──────────────────────────────

SERVICES_DEFAULT = """NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP        30d
api-server        ClusterIP   10.96.45.123     <none>        8080/TCP       10d
redis             ClusterIP   10.96.78.234     <none>        6379/TCP       10d
nginx-ingress     NodePort    10.96.12.56      <none>        80:30080/TCP   10d"""

DEPLOYMENTS_DEFAULT = """NAME              READY   UP-TO-DATE   AVAILABLE   AGE
api-server        0/2     2            0           10d
worker            1/1     1            1           10d
redis             1/1     1            1           10d
nginx-ingress     1/1     1            1           10d"""

DEPLOYMENTS_STAGING = """NAME              READY   UP-TO-DATE   AVAILABLE   AGE
frontend-app      0/2     2            0           45m
backend-api       1/1     1            1           5d
postgres-db       1/1     1            1           5d"""


# ============================================================
# KOMUT YÖNLENDIRME
# ============================================================

def _parse_namespace(command: str) -> str:
    """Komuttan namespace'i parse eder."""
    parts = command.split()
    for i, part in enumerate(parts):
        if part in ("-n", "--namespace") and i + 1 < len(parts):
            return parts[i + 1]
    return "default"


def _parse_resource_name(command: str) -> str:
    """Komuttan resource adını parse eder (describe/logs için)."""
    parts = command.split()
    # describe <type> <name> veya logs <name>
    ns_skip = set()
    for i, part in enumerate(parts):
        if part in ("-n", "--namespace"):
            ns_skip.add(i)
            ns_skip.add(i + 1)

    clean_parts = [p for i, p in enumerate(parts) if i not in ns_skip]

    if clean_parts[0] == "describe" and len(clean_parts) >= 3:
        return clean_parts[2]
    elif clean_parts[0] == "logs" and len(clean_parts) >= 2:
        return clean_parts[1]
    return ""


def _handle_get(command: str) -> str:
    """GET komutlarını işler."""
    parts = command.lower().split()
    ns = _parse_namespace(command)

    # Resource tipini bul
    resource = parts[1] if len(parts) > 1 else ""

    if resource in ("pods", "pod", "po"):
        if ns == "production":
            return PODS_PRODUCTION
        elif ns == "staging":
            return PODS_STAGING
        elif ns == "monitoring":
            return PODS_MONITORING
        elif ns == "kube-system":
            return PODS_KUBE_SYSTEM
        else:
            return PODS_DEFAULT

    elif resource in ("nodes", "node", "no"):
        return NODES_OUTPUT

    elif resource in ("services", "service", "svc"):
        return SERVICES_DEFAULT

    elif resource in ("deployments", "deployment", "deploy"):
        if ns == "staging":
            return DEPLOYMENTS_STAGING
        return DEPLOYMENTS_DEFAULT

    elif resource in ("events", "event"):
        if ns == "production":
            return EVENTS_PRODUCTION
        elif ns == "staging":
            return EVENTS_STAGING
        elif ns == "kube-system":
            return EVENTS_KUBE_SYSTEM
        return EVENTS_DEFAULT

    return f"No resources found in {ns} namespace."


def _handle_describe(command: str) -> str:
    """DESCRIBE komutlarını işler."""
    parts = command.lower().split()
    ns = _parse_namespace(command)
    resource_name = _parse_resource_name(command)

    if len(parts) < 2:
        return "error: You must specify the type of resource to describe."

    resource_type = parts[1]

    if resource_type in ("pod", "pods", "po"):
        if "api-server" in resource_name:
            return DESCRIBE_API_SERVER
        elif "frontend" in resource_name:
            return DESCRIBE_FRONTEND
        elif "pending" in resource_name:
            return DESCRIBE_PENDING_POD
        return f"Error from server (NotFound): pods \"{resource_name}\" not found"

    elif resource_type in ("node", "nodes", "no"):
        if "worker-2" in resource_name:
            return DESCRIBE_NODE_WORKER2
        elif "worker-3" in resource_name:
            return DESCRIBE_NODE_WORKER3
        return f"Error from server (NotFound): nodes \"{resource_name}\" not found"

    return f"Error from server (NotFound): {resource_type} \"{resource_name}\" not found"


def _handle_logs(command: str) -> str:
    """LOGS komutlarını işler."""
    resource_name = _parse_resource_name(command)

    if "api-server" in resource_name:
        return LOGS_API_SERVER
    elif "frontend" in resource_name:
        return LOGS_FRONTEND
    return f"Error from server (NotFound): pods \"{resource_name}\" not found"


def _handle_top(command: str) -> str:
    """TOP komutlarını işler."""
    parts = command.lower().split()
    ns = _parse_namespace(command)

    resource = parts[1] if len(parts) > 1 else ""

    if resource in ("pods", "pod", "po"):
        if ns == "production":
            return TOP_PODS_PRODUCTION
        return TOP_PODS_DEFAULT

    elif resource in ("nodes", "node", "no"):
        return TOP_NODES

    return "error: You must specify the type of resource to get metrics for."


# ============================================================
# ANA TOOL FONKSİYONU
# ============================================================

def kubectl_mock(command: str) -> str:
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
    logger.info(f"[MOCK] kubectl komutu: kubectl {command}")

    # Güvenlik kontrolü (mock olsa da aynı kurallar geçerli)
    is_valid, error_msg = validate_kubectl_command(command)
    if not is_valid:
        return f"HATA: {error_msg}"

    parts = command.strip().split()
    if not parts:
        return "error: You must specify a kubectl sub-command."

    sub_command = parts[0].lower()

    try:
        if sub_command == "get":
            return _handle_get(command)
        elif sub_command == "describe":
            return _handle_describe(command)
        elif sub_command == "logs":
            return _handle_logs(command)
        elif sub_command == "top":
            return _handle_top(command)
        else:
            return f"error: unknown command \"{sub_command}\""
    except Exception as e:
        logger.error(f"[MOCK] Hata: {e}")
        return f"error: {str(e)}"


def get_kubectl_mock_tool() -> FunctionTool:
    """FunctionTool olarak sarmalanmış mock kubectl aracını döndürür."""
    return FunctionTool.from_defaults(
        fn=kubectl_mock,
        name="kubectl_exec",
        description=(
            "Kubernetes cluster'ında kubectl komutu çalıştırır (SADECE okuma komutları). "
            "Cluster'daki pod, service, deployment, node durumlarını kontrol etmek için kullan. "
            "İzin verilen komutlar: get, describe, logs, top. "
            "Örnek: kubectl_exec('get pods -n default') veya kubectl_exec('describe pod my-pod -n production'). "
            "Komutun başına 'kubectl' yazma, sadece alt komutu yaz."
        ),
    )

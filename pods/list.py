import sys
from kubernetes import client, config

def list_pod_for_all_namespaces():
    """모든 namespace pod조회"""
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def list_pod_namespace():
    """namespace pod조회"""
    v1 = client.CoreV1Api()
    namespace = "kube-system"

    podList: client.models.V1PodList = v1.list_namespaced_pod(namespace=namespace)
    podObjs: list[client.models.V1Pod] = podList.items

    for podObj in podObjs:
        pod_metadata: client.models.V1ObjectMeta = podObj.metadata
        print(pod_metadata.name)

def main():
    # list_pod_for_all_namespaces()
    list_pod_namespace()

if __name__ == "__main__":
    try:
        config.load_kube_config()
    except Exception as e:
        print("Load config error")
        sys.exit(1)

    main()
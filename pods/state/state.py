import sys
from kubernetes import client, config
from typing import List, Union
from pydantic import BaseModel


def print_status(pod_metadata: client.models.V1ObjectMeta, pod_status: client.models.V1PodStatus):
    """pod label 조회"""
    container_statuses: List[client.models.V1ContainerStatus] = pod_status.container_statuses

    # reference: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1PodStatus.md
    print(f"==== {pod_metadata.name}'s containers status ===")
    print(f"pod's phase: {pod_status.phase}")
    for container_status in container_statuses:
        print(f"container name: {container_status.name}\tready:{container_status.ready}")


def list_pod_with_label_filter_namespace():
    """namespace pod조회"""
    v1 = client.CoreV1Api()
    namespace = "default"

    podList: client.models.V1PodList = v1.list_namespaced_pod(namespace=namespace)
    podObjs: list[client.models.V1Pod] = podList.items

    for podObj in podObjs:
        pod_metadata: client.models.V1ObjectMeta = podObj.metadata
        pod_status: client.models.V1PodStatus = podObj.status

        print_status(pod_metadata=pod_metadata, pod_status=pod_status)
        print("")

def main():
    # list_pod_for_all_namespaces()
    list_pod_with_label_filter_namespace()

if __name__ == "__main__":
    try:
        config.load_kube_config()
    except Exception as e:
        print("Load config error")
        sys.exit(1)

    main()
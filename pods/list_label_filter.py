import sys
from kubernetes import client, config
from typing import Dict, List
from pydantic import BaseModel


class PodLabel(BaseModel):
    """pod 라벨관리"""
    name: str
    value: str

def print_label_using_pydantic(pod_metadata: client.models.V1ObjectMeta):
    labels: List[PodLabel] = []

    for key, value in pod_metadata.labels.items():
        labels.append(PodLabel(
            name=key,
            value=value
        ))

    print(f"==== {pod_metadata.name}'s labels ===")
    for label in labels:
        print(f"{label.name}: {label.value}")

def print_labels(pod_metadata: client.models.V1ObjectMeta):
    """pod label 조회"""
    labels: Dict["str", "str"] = pod_metadata.labels

    print(f"==== {pod_metadata.name}'s labels ===")
    for key, value in labels.items():
        print(f"{key}: {value}")

def list_pod_with_label_filter_namespace():
    """namespace pod조회"""
    v1 = client.CoreV1Api()
    namespace = "kube-system"

    podList: client.models.V1PodList = v1.list_namespaced_pod(namespace=namespace)
    podObjs: list[client.models.V1Pod] = podList.items

    for podObj in podObjs:
        pod_metadata: client.models.V1ObjectMeta = podObj.metadata
        # print_labels(pod_metadata)
        print_label_using_pydantic(pod_metadata)
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
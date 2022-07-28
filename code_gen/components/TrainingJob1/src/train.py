import argparse
import yaml
import logging
import boto3
import os
from kubernetes import client, config, utils

def submit_job_request(k8s_core, ack_yaml):
    """
    args: 
        k8s_client: an ApiClient object, initialized with the client args.
        ack_yaml: List[dict]. Optional list of YAML objects; used instead
            of reading the `yaml_file`. Default is None.
    """
    print("========================")
    print(ack_yaml)
    utils.create_from_yaml(
        k8s_client=k8s_core, yaml_objects=ack_yaml, namespace="", verbose=True
    )

    ## after job submitted, log job submitted in console

def get_job_status(k8s_client, cr_group, cr_version, cr_name):
    """
    args: 
        cr_group: the custom resource's group (parsed from ack_yaml)
        cr_version: the custom resource's version (parsed from ack_yaml)
        cr_namespace: The custom resource's namespace (parsed from ack_yaml, if empty, then 'default')
        cr_plural: the custom resource's plural name. (from ACK YAML CRD)
        cr_name: the custom object's name (required)
    return:
        boolean if job has completed, whether succeed or fail.
    """
    pass

def main():
    ## parse input arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--ack_yaml",
        type=yaml.safe_load,
        help="Raw YAML for deployment",
        default="{}"
    )

    args = parser.parse_args()

    ack_yaml = args.ack_yaml
    logging.info(ack_yaml)
    logging.info('\n')
    logging.info('===========================')

    # ## configure identity to access Kubenete/ACK/kubecli? 
    # # user input an IAM role 
    # # python client provides this KFP pod/container access to EKS/Sagemaker/S3 etc.
    # region = 'us-west-1'
    # cluster_name = 'kf-ack-west-1'
    # arn_role = 'arn:aws:iam::369148113735:role/admin'
    # config_file = "config_EKS.txt"

    # # Set up the client
    # s = boto3.Session(region_name=region)
    # eks = s.client("eks")
    # # get cluster details
    # cluster = eks.describe_cluster(name=cluster_name)
    # logging.info(cluster)
    # logging.info('\n')
    # logging.info('===========================')

    # os.system("aws eks update-kubeconfig --region %s --name %s --role-arn %s" % (region, cluster_name, arn_role) )

    # logging.info('\n')
    # logging.info('===========================')

    ############################################################
    ## configure kubectl client
    config.load_kube_config()
    k8s_core_client = client.CoreV1Api()
    k8s_custom_client = client.CustomObjectsApi()

    # list pods test
    # ret = k8s_core_client.list_pod_for_all_namespaces(watch=False)
    # for i in ret.items:
    #     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    #     logging.info("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    # kubectl describe trainingjobs ack-xgboost-training-job-369148113735-5 --namespace default
    # api_response = k8s_custom_client.get_namespaced_custom_object_status(group='sagemaker.services.k8s.aws', version='v1alpha1', namespace='default', plural='trainingjobs', name='ack-xgboost-training-job-369148113735-6')
    # print(api_response['status'])
    
    # Similar to kubectl get trainingjobs --all-namespaces 
    # but list or watch cluster scoped custom objects in YAML DETAILS
    # https://stackoverflow.com/questions/61594447/python-kubernetes-client-equivalent-of-kubectl-get-custom-resource
    # api_response = k8s_custom_client.list_cluster_custom_object(group='sagemaker.services.k8s.aws', version='v1alpha1', plural='trainingjobs')
    # print(api_response)

    # submit_job_request(k8s_core_client, ack_yaml)

    # write to tmp file
    # with open('/tmp/whatever_output.txt', 'w') as f:
    #     f.write(ret)

if __name__ == "__main__":
    main()

## https://stackoverflow.com/questions/54953190/amazon-eks-generate-update-kubeconfig-via-python-script

import boto3
import yaml

# 
region = 'us-west-1'
cluster_name = 'kf-ack-west-1'
config_file = "config_EKS.txt"


# Set up the client
s = boto3.Session(region_name=region)
eks = s.client("eks")

# get cluster details
cluster = eks.describe_cluster(name=cluster_name)
cluster_cert = cluster["cluster"]["certificateAuthority"]["data"]
cluster_endpoint = cluster["cluster"]["endpoint"]

# build the cluster config hash
cluster_config = {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
            {
                "cluster": {
                    "server": str(cluster_endpoint),
                    "certificate-authority-data": str(cluster_cert)
                },
                "name": "kubernetes"
            }
        ],
        "contexts": [
            {
                "context": {
                    "cluster": "kubernetes",
                    "user": "aws"
                },
                "name": "aws"
            }
        ],
        "current-context": "aws",
        "preferences": {},
        "users": [
            {
                "name": "aws",
                "user": {
                    "exec": {
                        "apiVersion": "client.authentication.k8s.io/v1alpha1",
                        "command": "heptio-authenticator-aws",
                        "args": [
                            "token", "-i", cluster_name
                        ]
                    }
                }
            }
        ]
    }

# Write in YAML.
config_text=yaml.dump(cluster_config, default_flow_style=False)

with open(config_file, 'w') as f:
    f.write(config_text)
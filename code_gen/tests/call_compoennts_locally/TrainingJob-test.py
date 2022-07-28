import os
import random

from numpy import argsort
import yaml
from code_gen.components.TrainingJob.src.TrainingJob_component import (
    SageMakerTrainingJobComponent,
)

"""
Call component implementation src/TrainingJob.py locally. 

Imitate how the component calls the implementation script in a container image: (snippet from component.yaml)

implementation:
  container:
    image: rdpen/kfp-component-sagemaker:latest
    command: [python3]
    args:
      - code_gen/components/TrainingJob/src/TrainingJob.py
      - --algorithm_specification
      - { inputValue: algorithm_specification }
      - --checkpoint_config
      - { inputValue: checkpoint_config }
      - ...

sample parameters:
https://github.com/aws-controllers-k8s/sagemaker-controller/blob/main/samples/training/my-training-job.yaml
https://aws-controllers-k8s.github.io/community/docs/tutorials/sagemaker-example/
"""
##############################################################################################################

# set up input values

# with open("code_gen/components/TrainingJob/src/TrainingJob_request.yaml.tpl", "r") as f:
#     yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
#     job_num = yaml_dict["metadata"]["name"].split("-")[-1]

trainingJobName = "kfp-ack-training-job-" + str(random.randint(0, 99999))

hyperParameters = {
    "max_depth": "2",
    "gamma": "10",
    "eta": "0.3",
    "min_child_weight": "6",
    "objective": "multi:softmax",
    "num_class": "10",
    "num_round": "10",
}

algorithmSpecification = {
    "trainingImage": "746614075791.dkr.ecr.us-west-1.amazonaws.com/sagemaker-xgboost:1.2-1",
    # "trainingImage": "746614075791.dkr.ecr.us-west-1.amazonaws.com/sagemaker-xgboost:1.2", # delete: wrong image
    "trainingInputMode": "File",
}

roleARN = "arn:aws:iam::402026529871:role/ack-sagemaker-execution-role-402026529871"

outputDataConfig = {"s3OutputPath": "s3://ack-sagemaker-bucket-402026529871"}

resourceConfig = {
    "instanceCount": 1,
    "instanceType": "ml.m4.xlarge",
    "volumeSizeInGB": 5,
}

stoppingCondition = {"maxRuntimeInSeconds": 86400}

inputDataConfig = [
    {
        "channelName": "train",
        "dataSource": {
            "s3DataSource": {
                "s3DataType": "S3Prefix",
                "s3URI": "s3://ack-sagemaker-bucket-402026529871/sagemaker/xgboost/train",
                "s3DataDistributionType": "FullyReplicated",
            },
        },
        "contentType": "text/libsvm",
        "compressionType": "None",
    },
    {
        "channelName": "validation",
        "dataSource": {
            "s3DataSource": {
                "s3DataType": "S3Prefix",
                "s3URI": "s3://ack-sagemaker-bucket-402026529871/sagemaker/xgboost/validation",
                "s3DataDistributionType": "FullyReplicated",
            },
        },
        "contentType": "text/libsvm",
        "compressionType": "None",
    },
]

REQUIRED_ARGS = {
    "--algorithm_specification": '"' + str(algorithmSpecification) + '"',
    # "--checkpoint_config": """ """,
    # "--debug_hook_config": """ """,
    # "--debug_rule_configurations": """ """,
    # "--enable_inter_container_traffic_encryption": """ """,
    # "--enable_managed_spot_training": """ """,
    # "--enable_network_isolation": """ """,
    # "--environment": """ """,
    # "--experiment_config": """ """,
    "--hyper_parameters": '"' + str(hyperParameters) + '"',
    "--input_data_config": '"' + str(inputDataConfig) + '"',
    "--output_data_config": '"' + str(outputDataConfig) + '"',
    # "--profiler_config": """ """,
    # "--profiler_rule_configurations": """ """,
    "--resource_config": '"' + str(resourceConfig) + '"',
    "--role_arn": '"' + str(roleARN) + '"',
    "--stopping_condition": '"' + str(stoppingCondition) + '"',
    # "--tags": """ """,
    # "--tensor_board_output_config": """ """,
    "--training_job_name": '"' + str(trainingJobName) + '"',
    # "--vpc_config": """ """,
}

arguments = ""
for key in REQUIRED_ARGS:
    arguments = arguments + " " + key + " " + REQUIRED_ARGS[key]
# print(arguments)

# file_loc = "code_gen/components/TrainingJob/src/TrainingJob.py"
file_loc = "code_gen/components/TrainingJob/src/TrainingJob_component.py"
# file_loc = "code_gen/components/TrainingJob1/src/TrainingJob1.py"

os.system("python3 " + file_loc + arguments)

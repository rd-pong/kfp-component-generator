import os
import random

"""
Call component.py locally
"""

hyperParameterTuningJobName = "kfp-ack-hpo-job-" + str(random.randint(0, 99999))
hyperParameterTuningJobConfig = {
    "strategy": "Bayesian",
    "hyperParameterTuningJobObjective": {
        "type_": "Minimize",
        "metricName": "validation:error",
    },
    "resourceLimits": {"maxNumberOfTrainingJobs": 2, "maxParallelTrainingJobs": 1},
    "parameterRanges": {
        "integerParameterRanges": [
            {
                "name": "num_round",
                "minValue": "10",
                "maxValue": "20",
                "scalingType": "Linear",
            }
        ],
        "continuousParameterRanges": [],
        "categoricalParameterRanges": [],
    },
}
trainingJobDefinition = {
    "staticHyperParameters": {
        "base_score": "0.5",
        "booster": "gbtree",
        "csv_weights": "0",
        "dsplit": "row",
        "grow_policy": "depthwise",
        "lambda_bias": "0.0",
        "max_bin": "256",
        "max_leaves": "0",
        "normalize_type": "tree",
        "objective": "reg:linear",
        "one_drop": "0",
        "prob_buffer_row": "1.0",
        "process_type": "default",
        "rate_drop": "0.0",
        "refresh_leaf": "1",
        "sample_type": "uniform",
        "scale_pos_weight": "1.0",
        "silent": "0",
        "sketch_eps": "0.03",
        "skip_drop": "0.0",
        "tree_method": "auto",
        "tweedie_variance_power": "1.5",
        "updater": '"grow_colmaker,prune"',
    },
    "algorithmSpecification": {
        "trainingImage": "632365934929.dkr.ecr.us-west-1.amazonaws.com/xgboost:1",
        "trainingInputMode": "File",
    },
    "roleARN": "arn:aws:iam::402026529871:role/ack-sagemaker-execution-role-402026529871",
    "inputDataConfig": [
        {
            "channelName": "train",
            "dataSource": {
                "s3DataSource": {
                    "s3DataType": "S3Prefix",
                    "s3URI": "s3://ack-sagemaker-bucket-402026529871/sagemaker/xgboost/train",
                    "s3DataDistributionType": "FullyReplicated",
                }
            },
            "contentType": "text/libsvm",
            "compressionType": "None",
            "recordWrapperType": "None",
            "inputMode": "File",
        },
        {
            "channelName": "validation",
            "dataSource": {
                "s3DataSource": {
                    "s3DataType": "S3Prefix",
                    "s3URI": "s3://ack-sagemaker-bucket-402026529871/sagemaker/xgboost/validation",
                    "s3DataDistributionType": "FullyReplicated",
                }
            },
            "contentType": "text/libsvm",
            "compressionType": "None",
            "recordWrapperType": "None",
            "inputMode": "File",
        },
    ],
    "outputDataConfig": {"s3OutputPath": "s3://ack-sagemaker-bucket-402026529871"},
    "resourceConfig": {
        "instanceType": "ml.m4.xlarge",
        "instanceCount": 1,
        "volumeSizeInGB": 25,
    },
    "stoppingCondition": {"maxRuntimeInSeconds": 3600},
    "enableNetworkIsolation": True,
    "enableInterContainerTrafficEncryption": False,
}

REQUIRED_ARGS = {
    "--hyper_parameter_tuning_job_config": '"'
    + str(hyperParameterTuningJobConfig)
    + '"',
    "--hyper_parameter_tuning_job_name": '"' + str(hyperParameterTuningJobName) + '"',
    # "--tags": """ '[]' """,
    "--training_job_definition": '"' + str(trainingJobDefinition) + '"',
    # "--training_job_definitions": """ '[]' """,
    # "--warm_start_config": '"' + str(warm_start_config) + '"',
}

arguments = ""

for key in REQUIRED_ARGS:
    arguments = arguments + " " + key + " " + REQUIRED_ARGS[key]

# print(arguments)

# file_loc = "code_gen/components/HyperParameterTuningJob1/src/HyperParameterTuningJob.py"
file_loc = "code_gen/components/HyperParameterTuningJob/src/HyperParameterTuningJob_component.py"

# os.system("pwd")
os.system("python " + file_loc + arguments)

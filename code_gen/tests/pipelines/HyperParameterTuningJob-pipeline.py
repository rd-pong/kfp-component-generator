#!/usr/bin/env python3

# Uncomment the apply(use_aws_secret()) below if you are not using OIDC
# more info : https://github.com/kubeflow/pipelines/tree/master/samples/contrib/aws-samples/README.md

# RUN in dir: code_gen/tests/pipelines/HyperParameterTuningJob-pipeline.py
# dsl-compile --py HyperParameterTuningJob-pipeline.py --output HyperParameterTuningJob-pipeline.tar.gz

import kfp
import json
import copy
from kfp import components
from kfp import dsl
from kfp.aws import use_aws_secret
import random

# users can prepare complex input args (object, array) here:

hyperParameterTuningJobName = "kfp-ack-hpo-job-" + str(random.randint(0, 999999))
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
        "updater": 'grow_colmaker,prune',
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

###########################GENERATED SECTION BELOW############################

sagemaker_HyperParameterTuningJob_op = components.load_component_from_file(
    "../../components/HyperParameterTuningJob/component.yaml"
)


@dsl.pipeline(
    name="HyperParameterTuningJob",
    description="SageMaker HyperParameterTuningJob component",
)
def HyperParameterTuningJob(
    hyper_parameter_tuning_job_config=hyperParameterTuningJobConfig,  # JsonObject
    hyper_parameter_tuning_job_name=hyperParameterTuningJobName,  # String
    tags=None,  # JsonArray
    training_job_definition=trainingJobDefinition,  # JsonObject
    training_job_definitions=None,  # JsonArray
    warm_start_config=None,  # JsonObject
):
    HyperParameterTuningJob = sagemaker_HyperParameterTuningJob_op(
        hyper_parameter_tuning_job_config=hyper_parameter_tuning_job_config,
        hyper_parameter_tuning_job_name=hyper_parameter_tuning_job_name,
        tags=tags,
        training_job_definition=training_job_definition,
        training_job_definitions=training_job_definitions,
        warm_start_config=warm_start_config,
    ).apply(use_aws_secret("aws-secret", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"))


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(HyperParameterTuningJob, __file__ + ".zip")

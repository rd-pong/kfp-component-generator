#!/usr/bin/env python3

# Uncomment the apply(use_aws_secret()) below if you are not using OIDC
# more info : https://github.com/kubeflow/pipelines/tree/master/samples/contrib/aws-samples/README.md

# RUN in dir: code_gen/components/${CRD_NAME}/pipeline/
# dsl-compile --py ${CRD_NAME}-pipeline.py --output ${CRD_NAME}-pipeline.tar.gz

import kfp
import json
import copy
from kfp import components
from kfp import dsl
from kfp.aws import use_aws_secret
import yaml

#############################################################################
# users can prepare complex input args (object, array) here:




###########################GENERATED SECTION BELOW############################

sagemaker_${CRD_NAME}_op = components.load_component_from_file(
    "../component.yaml"
    # "code_gen/components/${CRD_NAME}/component.yaml"
)

@dsl.pipeline(name="${CRD_NAME}", description="SageMaker ${CRD_NAME} component")
def ${CRD_NAME}(
${PIPELINE_USER_INPUTS}
):
    ${CRD_NAME} = sagemaker_${CRD_NAME}_op(
${PIPELINE_ARGS_ASSIGN}
    )  # .apply(use_aws_secret('aws-secret', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'))

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(${CRD_NAME}, __file__ + ".zip")

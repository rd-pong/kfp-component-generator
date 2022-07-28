name: "Sagemaker - ${CRD_NAME}"
description: Create ${CRD_NAME}
inputs:
  ###########################GENERATED SECTION BELOW############################
  ${YAML_INPUTS}
  ###########################GENERATED SECTION ABOVE############################

outputs:
  ###########################GENERATED SECTION BELOW############################
  ${YAML_OUTPUTS}
  ###########################GENERATED SECTION ABOVE############################

implementation:
  container:
    image: ${COMPONENT_CONTAINER_IMAGE}
    command: [python3]
    args:
      - code_gen/components/${CRD_NAME}/src/${CRD_NAME}_component.py
      ###########################GENERATED SECTION BELOW############################
      ${YAML_ARGS}
      ###########################GENERATED SECTION ABOVE############################


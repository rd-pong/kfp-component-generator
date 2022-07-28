"""Specification for the SageMaker - ${CRD_NAME}"""

from dataclasses import dataclass

from typing import List
from code_gen.common.sagemaker_component_spec import (
    SageMakerComponentSpec,
    SageMakerComponentBaseOutputs,
)
from code_gen.common.spec_input_parsers import SpecInputParsers
from code_gen.common.common_inputs import (
    SageMakerComponentInput as Input,
    SageMakerComponentOutput as Output,
    SageMakerComponentInputValidator as InputValidator,
    SageMakerComponentOutputValidator as OutputValidator,
)


@dataclass(frozen=True)
class ${INPUT_CLASS_NAME}:
    """Defines the set of inputs for the ${CRD_NAME} component."""
    ${SPEC_INPUT_DEFINITIONS}


@dataclass
class ${OUTPUT_CLASS_NAME}(SageMakerComponentBaseOutputs):
    """Defines the set of outputs for the ${CRD_NAME} component."""
    ${SPEC_OUTPUT_DEFINITIONS}


class ${SPEC_CLASS_NAME}(
    SageMakerComponentSpec[${INPUT_CLASS_NAME}, ${OUTPUT_CLASS_NAME}]
):
    INPUTS: ${INPUT_CLASS_NAME} = ${INPUT_CLASS_NAME}(
        ${SPEC_INPUT_VALIDATORS}
    )
    
    OUTPUTS = ${OUTPUT_CLASS_NAME}(
        ${SPEC_OUTPUT_VALIDATORS}
    )

    def __init__(self, arguments: List[str]):
        super().__init__(arguments, ${INPUT_CLASS_NAME}, ${OUTPUT_CLASS_NAME})

    @property
    def inputs(self) -> ${INPUT_CLASS_NAME}:
        return self._inputs

    @property
    def outputs(self) -> ${OUTPUT_CLASS_NAME}:
        return self._outputs

    @property
    def output_paths(self) -> ${OUTPUT_CLASS_NAME}:
        return self._output_paths


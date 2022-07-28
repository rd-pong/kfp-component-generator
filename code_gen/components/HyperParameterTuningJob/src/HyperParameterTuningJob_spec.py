"""Specification for the SageMaker - HyperParameterTuningJob"""

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
class SageMakerHyperParameterTuningJobInputs:
    """Defines the set of inputs for the HyperParameterTuningJob component."""
    
    hyper_parameter_tuning_job_config: Input
    hyper_parameter_tuning_job_name: Input
    tags: Input
    training_job_definition: Input
    training_job_definitions: Input
    warm_start_config: Input


@dataclass
class SageMakerHyperParameterTuningJobOutputs(SageMakerComponentBaseOutputs):
    """Defines the set of outputs for the HyperParameterTuningJob component."""
    
    ack_resource_metadata: Output
    best_training_job: Output
    conditions: Output
    failure_reason: Output
    hyper_parameter_tuning_job_status: Output
    overall_best_training_job: Output


class SageMakerHyperParameterTuningJobSpec(
    SageMakerComponentSpec[SageMakerHyperParameterTuningJobInputs, SageMakerHyperParameterTuningJobOutputs]
):
    INPUTS: SageMakerHyperParameterTuningJobInputs = SageMakerHyperParameterTuningJobInputs(
        
        hyper_parameter_tuning_job_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="['The HyperParameterTuningJobConfig object that describes the tuning job, including the search strateg']",
            required=True
        ), 
        hyper_parameter_tuning_job_name=InputValidator(
            input_type=str,
            description="['The name of the tuning job. This name is the prefix for the names of all training jobs that this tun']",
            required=True
        ), 
        tags=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_list,
            description="['An array of key-value pairs. You can use tags to categorize your Amazon Web Services resources in di']",
            required=False
        ), 
        training_job_definition=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="['The HyperParameterTrainingJobDefinition object that describes the training jobs that this tuning job']",
            required=False
        ), 
        training_job_definitions=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_list,
            description="['A list of the HyperParameterTrainingJobDefinition objects launched for this tuning job.']",
            required=False
        ), 
        warm_start_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="['Specifies the configuration for starting the hyperparameter tuning job using one or more previous tu']",
            required=False
        ), 
    )
    
    OUTPUTS = SageMakerHyperParameterTuningJobOutputs(
        
        ack_resource_metadata=OutputValidator(
            description="['All CRs managed by ACK have a common `Status.ACKResourceMetadata` member that is used to contain res']",
        ), 
        best_training_job=OutputValidator(
            description="['A TrainingJobSummary object that describes the training job that completed with the best current Hyp']",
        ), 
        conditions=OutputValidator(
            description="['All CRS managed by ACK have a common `Status.Conditions` member that contains a collection of `ackv1']",
        ), 
        failure_reason=OutputValidator(
            description="['If the tuning job failed, the reason it failed.']",
        ), 
        hyper_parameter_tuning_job_status=OutputValidator(
            description="['The status of the tuning job: InProgress, Completed, Failed, Stopping, or Stopped.']",
        ), 
        overall_best_training_job=OutputValidator(
            description="['If the hyperparameter tuning job is an warm start tuning job with a WarmStartType of IDENTICAL_DATA_']",
        ), 
    )

    def __init__(self, arguments: List[str]):
        super().__init__(arguments, SageMakerHyperParameterTuningJobInputs, SageMakerHyperParameterTuningJobOutputs)

    @property
    def inputs(self) -> SageMakerHyperParameterTuningJobInputs:
        return self._inputs

    @property
    def outputs(self) -> SageMakerHyperParameterTuningJobOutputs:
        return self._outputs

    @property
    def output_paths(self) -> SageMakerHyperParameterTuningJobOutputs:
        return self._output_paths


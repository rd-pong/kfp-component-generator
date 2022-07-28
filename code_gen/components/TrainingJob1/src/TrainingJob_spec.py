"""Specification for the SageMaker - TrainingJob"""

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
class SageMakerTrainingJobInputs:
    """Defines the set of inputs for the TrainingJob component."""
    
    algorithm_specification: Input
    checkpoint_config: Input
    debug_hook_config: Input
    debug_rule_configurations: Input
    enable_inter_container_traffic_encryption: Input
    enable_managed_spot_training: Input
    enable_network_isolation: Input
    environment: Input
    experiment_config: Input
    hyper_parameters: Input
    input_data_config: Input
    output_data_config: Input
    profiler_config: Input
    profiler_rule_configurations: Input
    resource_config: Input
    role_arn: Input
    stopping_condition: Input
    tags: Input
    tensor_board_output_config: Input
    training_job_name: Input
    vpc_config: Input


@dataclass
class SageMakerTrainingJobOutputs(SageMakerComponentBaseOutputs):
    """Defines the set of outputs for the TrainingJob component."""
    
    ack_resource_metadata: Output
    conditions: Output
    debug_rule_evaluation_statuses: Output
    failure_reason: Output
    model_artifacts: Output
    profiler_rule_evaluation_statuses: Output
    secondary_status: Output
    training_job_status: Output


class SageMakerTrainingJobSpec(
    SageMakerComponentSpec[SageMakerTrainingJobInputs, SageMakerTrainingJobOutputs]
):
    INPUTS: SageMakerTrainingJobInputs = SageMakerTrainingJobInputs(
        
        algorithm_specification=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="The registry path of the Docke",
            required=True
        ), 
        checkpoint_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="Contains information about the",
            required=False
        ), 
        debug_hook_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="Configuration information for ",
            required=False
        ), 
        debug_rule_configurations=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_list,
            description="Configuration information for ",
            required=False
        ), 
        enable_inter_container_traffic_encryption=InputValidator(
            input_type=SpecInputParsers.str_to_bool,
            description="To encrypt all communications ",
            required=False
        ), 
        enable_managed_spot_training=InputValidator(
            input_type=SpecInputParsers.str_to_bool,
            description="To train models using managed ",
            required=False
        ), 
        enable_network_isolation=InputValidator(
            input_type=SpecInputParsers.str_to_bool,
            description="Isolates the training containe",
            required=False
        ), 
        environment=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="The environment variables to s",
            required=False
        ), 
        experiment_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="Associates a SageMaker job as ",
            required=False
        ), 
        hyper_parameters=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="Algorithm-specific parameters ",
            required=False
        ), 
        input_data_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_list,
            description="An array of Channel objects. E",
            required=False
        ), 
        output_data_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="Specifies the path to the S3 l",
            required=True
        ), 
        profiler_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="Configuration information for ",
            required=False
        ), 
        profiler_rule_configurations=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_list,
            description="Configuration information for ",
            required=False
        ), 
        resource_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="The resources, including the M",
            required=True
        ), 
        role_arn=InputValidator(
            input_type=str,
            description="The Amazon Resource Name (ARN)",
            required=True
        ), 
        stopping_condition=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="Specifies a limit to how long ",
            required=True
        ), 
        tags=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_list,
            description="An array of key-value pairs. Y",
            required=False
        ), 
        tensor_board_output_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="Configuration of storage locat",
            required=False
        ), 
        training_job_name=InputValidator(
            input_type=str,
            description="The name of the training job. ",
            required=True
        ), 
        vpc_config=InputValidator(
            input_type=SpecInputParsers.yaml_or_json_dict,
            description="A VpcConfig object that specif",
            required=False
        ), 
    )
    
    OUTPUTS = SageMakerTrainingJobOutputs(
        
        ack_resource_metadata=OutputValidator(
            description="All CRs managed by ACK have a ",
        ), 
        conditions=OutputValidator(
            description="All CRS managed by ACK have a ",
        ), 
        debug_rule_evaluation_statuses=OutputValidator(
            description="Evaluation status of Debugger ",
        ), 
        failure_reason=OutputValidator(
            description="If the training job failed, th",
        ), 
        model_artifacts=OutputValidator(
            description="Information about the Amazon S",
        ), 
        profiler_rule_evaluation_statuses=OutputValidator(
            description="Evaluation status of Debugger ",
        ), 
        secondary_status=OutputValidator(
            description="Provides detailed information ",
        ), 
        training_job_status=OutputValidator(
            description="The status of the training job",
        ), 
    )

    def __init__(self, arguments: List[str]):
        super().__init__(arguments, SageMakerTrainingJobInputs, SageMakerTrainingJobOutputs)

    @property
    def inputs(self) -> SageMakerTrainingJobInputs:
        return self._inputs

    @property
    def outputs(self) -> SageMakerTrainingJobOutputs:
        return self._outputs

    @property
    def output_paths(self) -> SageMakerTrainingJobOutputs:
        return self._output_paths


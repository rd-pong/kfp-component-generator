import logging
from typing import Dict

from code_gen.components.TrainingJob.src.TrainingJob_spec import (
    SageMakerTrainingJobInputs,
    SageMakerTrainingJobOutputs,
    SageMakerTrainingJobSpec,
)
from code_gen.common.sagemaker_component import (
    SageMakerComponent,
    ComponentMetadata,
    SageMakerJobStatus,
    DebugRulesStatus,
)
from code_gen.generator.utils import snake_to_camel


@ComponentMetadata(
    name="SageMaker - TrainingJob",
    description="",
    spec=SageMakerTrainingJobSpec,
)
class SageMakerTrainingJobComponent(SageMakerComponent):
    """SageMaker component for training."""

    def Do(self, spec: SageMakerTrainingJobSpec):

        # set parameters
        self._ack_job_name = SageMakerComponent._generate_unique_timestamped_id(
            prefix="ack-trainingjob"
        )

        ############GENERATED SECTION BELOW############
        
        self.group = "sagemaker.services.k8s.aws"
        self.version = "v1alpha1"
        self.plural = "trainingjobs"
        self.namespace = "default"

        self.job_request_outline_location = (
            "code_gen/components/TrainingJob/src/TrainingJob_request.yaml.tpl"
        )
        self.job_request_location = (
            "code_gen/components/TrainingJob/src/TrainingJob_request.yaml"
        )
        ############GENERATED SECTION ABOVE############

        super().Do(spec.inputs, spec.outputs, spec.output_paths)

    def _create_job_request(
        self,
        inputs: SageMakerTrainingJobInputs,
        outputs: SageMakerTrainingJobOutputs,
    ) -> Dict:

        return super()._create_job_yaml(inputs, outputs)

    def _submit_job_request(self, request: Dict) -> object:
        # submit job request

        return super()._create_resource(request, 3, 10)

    def _after_submit_job_request(
        self,
        job: object,
        request: Dict,
        inputs: SageMakerTrainingJobInputs,
        outputs: SageMakerTrainingJobOutputs,
    ):
        logging.info(f"Created ACK custom object with name: {self._ack_job_name}")

        arn = super()._get_resource()["status"]["ackResourceMetadata"]["arn"]
        logging.info(f"Created Sagamaker Training Job with ARN: {arn}")

        # logging.info(
        #     f"Created Sagamaker Training Job with name: %s",
        #     request["spec"]["trainingJobName"],  # todo: developer customize
        # )

    def _get_job_status(self):
        ack_statuses = super()._get_resource()["status"]
        # logging.info(ack_statuses)
        sm_job_status = ack_statuses["trainingJobStatus"]  # todo: developer customize

        # print("Sagemaker job status: " + sm_job_status)

        if sm_job_status == "Completed":
            return SageMakerJobStatus(
                is_completed=True, has_error=False, raw_status="Completed"
            )
        if sm_job_status == "Failed":
            message = ack_statuses["failureReason"]
            return SageMakerJobStatus(
                is_completed=True,
                has_error=True,
                error_message=message,
                raw_status=sm_job_status,
            )

        return SageMakerJobStatus(is_completed=False, raw_status=sm_job_status)

    def _after_job_complete(
        self,
        job: object,
        request: Dict,
        inputs: SageMakerTrainingJobInputs,
        outputs: SageMakerTrainingJobOutputs,
    ):
        # prepare component outputs (defined in the spec)

        ack_statuses = super()._get_resource()["status"]

        ############GENERATED SECTION BELOW############

        outputs.ack_resource_metadata = (
            ack_statuses["ackResourceMetadata"]
            if "ackResourceMetadata" in ack_statuses
            else None
        )
        outputs.conditions = (
            ack_statuses["conditions"] if "conditions" in ack_statuses else None
        )
        outputs.debug_rule_evaluation_statuses = (
            ack_statuses["debugRuleEvaluationStatuses"]
            if "debugRuleEvaluationStatuses" in ack_statuses
            else None
        )
        outputs.failure_reason = (
            ack_statuses["failureReason"] if "failureReason" in ack_statuses else None
        )
        outputs.model_artifacts = (
            ack_statuses["modelArtifacts"] if "modelArtifacts" in ack_statuses else None
        )
        outputs.profiler_rule_evaluation_statuses = (
            ack_statuses["profilerRuleEvaluationStatuses"]
            if "profilerRuleEvaluationStatuses" in ack_statuses
            else None
        )
        outputs.secondary_status = (
            ack_statuses["secondaryStatus"]
            if "secondaryStatus" in ack_statuses
            else None
        )
        outputs.training_job_status = (
            ack_statuses["trainingJobStatus"]
            if "trainingJobStatus" in ack_statuses
            else None
        )
        ############GENERATED SECTION ABOVE############

        # print(outputs)


if __name__ == "__main__":
    import sys

    spec = SageMakerTrainingJobSpec(sys.argv[1:])

    component = SageMakerTrainingJobComponent()
    component.Do(spec)

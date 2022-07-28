import logging
from typing import Dict

from code_gen.components.HyperParameterTuningJob.src.HyperParameterTuningJob_spec import (
    SageMakerHyperParameterTuningJobInputs,
    SageMakerHyperParameterTuningJobOutputs,
    SageMakerHyperParameterTuningJobSpec,
)
from code_gen.common.sagemaker_component import (
    SageMakerComponent,
    ComponentMetadata,
    SageMakerJobStatus,
    DebugRulesStatus,
)
from code_gen.generator.utils import snake_to_camel


@ComponentMetadata(
    name="SageMaker - HyperParameterTuningJob",
    description="",
    spec=SageMakerHyperParameterTuningJobSpec,
)
class SageMakerHyperParameterTuningJobComponent(SageMakerComponent):

    """SageMaker component for training."""

    def Do(self, spec: SageMakerHyperParameterTuningJobSpec):

        # set parameters
        self._ack_job_name = SageMakerComponent._generate_unique_timestamped_id(
            prefix="ack-hyperparametertuningjob"
        )

        ############GENERATED SECTION BELOW############

        self.group = "sagemaker.services.k8s.aws"
        self.version = "v1alpha1"
        self.plural = "hyperparametertuningjobs"
        self.namespace = "default"

        self.job_request_outline_location = "code_gen/components/HyperParameterTuningJob/src/HyperParameterTuningJob_request.yaml.tpl"
        self.job_request_location = "code_gen/components/HyperParameterTuningJob/src/HyperParameterTuningJob_request.yaml"
        ############GENERATED SECTION ABOVE############

        super().Do(spec.inputs, spec.outputs, spec.output_paths)

    def _create_job_request(
        self,
        inputs: SageMakerHyperParameterTuningJobInputs,
        outputs: SageMakerHyperParameterTuningJobOutputs,
    ) -> Dict:

        return super()._create_job_yaml(inputs, outputs)

    def _submit_job_request(self, request: Dict) -> object:
        # submit job request

        return super()._create_resource(request, 5, 10)

    def _after_submit_job_request(
        self,
        job: object,
        request: Dict,
        inputs: SageMakerHyperParameterTuningJobInputs,
        outputs: SageMakerHyperParameterTuningJobOutputs,
    ):
        logging.info(f"Created ACK custom object with name: {self._ack_job_name}")

        arn = super()._get_resource()["status"]["ackResourceMetadata"]["arn"]
        logging.info(f"Created Sagamaker HyperParameterTuningJob with ARN: {arn}")

        # logging.info(
        #     f"Created Sagamaker Training Job with name: %s",
        #     request["spec"]["trainingJobName"],  # todo: developer customize
        # )

    def _get_job_status(self):
        ack_statuses = super()._get_resource()["status"]
        sm_job_status = ack_statuses[
            "hyperParameterTuningJobStatus"
        ]  # todo: developer customize

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
        inputs: SageMakerHyperParameterTuningJobInputs,
        outputs: SageMakerHyperParameterTuningJobOutputs,
    ):
        # prepare component outputs (defined in the spec)

        ack_statuses = super()._get_resource()["status"]

        ############GENERATED SECTION BELOW############

        outputs.ack_resource_metadata = (
            ack_statuses["ackResourceMetadata"]
            if "ackResourceMetadata" in ack_statuses
            else None
        )
        outputs.best_training_job = (
            ack_statuses["bestTrainingJob"]
            if "bestTrainingJob" in ack_statuses
            else None
        )
        outputs.conditions = (
            ack_statuses["conditions"] if "conditions" in ack_statuses else None
        )
        outputs.failure_reason = (
            ack_statuses["failureReason"] if "failureReason" in ack_statuses else None
        )
        outputs.hyper_parameter_tuning_job_status = (
            ack_statuses["hyperParameterTuningJobStatus"]
            if "hyperParameterTuningJobStatus" in ack_statuses
            else None
        )
        outputs.overall_best_training_job = (
            ack_statuses["overallBestTrainingJob"]
            if "overallBestTrainingJob" in ack_statuses
            else None
        )
        ############GENERATED SECTION ABOVE############

        # print(outputs)


if __name__ == "__main__":
    import sys

    spec = SageMakerHyperParameterTuningJobSpec(sys.argv[1:])

    component = SageMakerHyperParameterTuningJobComponent()
    component.Do(spec)

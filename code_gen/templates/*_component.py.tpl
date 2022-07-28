import logging
from typing import Dict

from code_gen.components.${CRD_NAME}.src.${CRD_NAME}_spec import (
    ${INPUT_CLASS_NAME},
    ${OUTPUT_CLASS_NAME},
    ${SPEC_CLASS_NAME},
)
from code_gen.common.sagemaker_component import (
    SageMakerComponent,
    ComponentMetadata,
    SageMakerJobStatus,
    DebugRulesStatus,
)
from code_gen.generator.utils import snake_to_camel


@ComponentMetadata(
    name="SageMaker - ${CRD_NAME}",
    description="",
    spec=${SPEC_CLASS_NAME},
)
class ${COMPONENT_CLASS_NAME}(SageMakerComponent):

    """SageMaker component for training."""

    def Do(self, spec: ${SPEC_CLASS_NAME}):

        # set parameters
        self._ack_job_name = SageMakerComponent._generate_unique_timestamped_id(
            prefix="ack-${CRD_NAME_LOWER}"
        )

        ############GENERATED SECTION BELOW############
        ${DO_PARAMETERS}
        ############GENERATED SECTION ABOVE############

        super().Do(spec.inputs, spec.outputs, spec.output_paths)

    def _create_job_request(
        self,
        inputs: ${INPUT_CLASS_NAME},
        outputs: ${OUTPUT_CLASS_NAME},
    ) -> Dict:

        return super()._create_job_yaml(inputs, outputs)

    def _submit_job_request(self, request: Dict) -> object:
        # submit job request

        return super()._create_resource(request, 5, 10)

    def _after_submit_job_request(
        self,
        job: object,
        request: Dict,
        inputs: ${INPUT_CLASS_NAME},
        outputs: ${OUTPUT_CLASS_NAME},
    ):
        logging.info(f"Created ACK custom object with name: {self._ack_job_name}")

        arn = super()._get_resource()["status"]["ackResourceMetadata"]["arn"]
        logging.info(f"Created Sagamaker ${CRD_NAME} with ARN: {arn}")

        # logging.info(
        #     f"Created Sagamaker Training Job with name: %s",
        #     request["spec"]["trainingJobName"],  # todo: developer customize
        # )

    def _get_job_status(self):
        ack_statuses = super()._get_resource()["status"]
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
        inputs: ${INPUT_CLASS_NAME},
        outputs: ${OUTPUT_CLASS_NAME},
    ):
        # prepare component outputs (defined in the spec)

        ack_statuses = super()._get_resource()["status"]

        ############GENERATED SECTION BELOW############
        ${OUTPUT_PREP}
        ############GENERATED SECTION ABOVE############

        # print(outputs)


if __name__ == "__main__":
    import sys

    spec = ${SPEC_CLASS_NAME}(sys.argv[1:])

    component = ${COMPONENT_CLASS_NAME}()
    component.Do(spec)

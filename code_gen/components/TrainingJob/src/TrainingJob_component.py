import logging
from typing import Dict
from enum import Enum, auto
from sagemaker.image_uris import retrieve
import yaml
from kubernetes import client, config, utils


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
        self.ack_job_name = SageMakerComponent._generate_unique_timestamped_id(
            prefix="ack-trainingjob"
        )
        self.group_name = "sagemaker.services.k8s.aws"
        self.version_name = "v1alpha1"
        self.plural_name = "trainingjobs"

        super().Do(spec.inputs, spec.outputs, spec.output_paths)

    def _create_job_request(
        self,
        inputs: SageMakerTrainingJobInputs,
        outputs: SageMakerTrainingJobOutputs,
    ) -> Dict:

        with open(
            "code_gen/components/TrainingJob/src/TrainingJob-request.yaml.tpl", "r"
        ) as job_request_outline:
            job_request_dict = yaml.load(job_request_outline, Loader=yaml.FullLoader)
            job_request_spec = job_request_dict["spec"]

            for para in vars(inputs):
                camel_para = snake_to_camel(para)
                if camel_para in job_request_spec:
                    job_request_spec[camel_para] = getattr(inputs, para)

            # job_request_dict["spec"] = job_request_spec
            job_request_dict["metadata"]["name"] = self.ack_job_name

            # print(job_request_dict)

            out_loc = "code_gen/components/TrainingJob/src/TrainingJob-request.yaml"
            with open(out_loc, "w+") as f:
                yaml.dump(job_request_dict, f, default_flow_style=False)
            print("CREATED: " + out_loc)

        return job_request_dict

    def _submit_job_request(self, request: Dict) -> object:
        # list pods test
        # ret = self._k8s_api_client.list_pod_for_all_namespaces(watch=False)
        # for i in ret.items:
        #     print(
        #         "%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name)
        #     )
        jobs = list()
        jobs.append(request)

        print("ack job name: " + request["metadata"]["name"])
        print("Sagemaker name: " + request["spec"]["trainingJobName"])

        # utils.create_from_yaml(
        #     k8s_client=self._k8s_api_client, yaml_objects=jobs, verbose=True
        # )

    def _get_job_status(self):

        job_statuses = super()._get_job_status()
        print(job_statuses["trainingJobStatus"])


if __name__ == "__main__":
    import sys

    spec = SageMakerTrainingJobSpec(sys.argv[1:])

    component = SageMakerTrainingJobComponent()
    component.Do(spec)

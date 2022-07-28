## Generate src/component_request.yaml.tpl content
import random
from code_gen.generator.utils import parse_crd, snake_to_camel, write_snippet_to_file


def get_ack_job_request_outline_spec(_input_spec_all):
    """
    Populate spec section in a ACK job request YAML
    Return a code snippet waiting to be written to ack_job_request.yaml.tpl template
    """
    _ack_job_request_outline_spec_buffer = ""

    for key in _input_spec_all:
        _ack_job_request_outline_spec_buffer += """  %s: \n""" % snake_to_camel(key)

    return _ack_job_request_outline_spec_buffer

if __name__ == "__main__":

    ##############User inputs##############
    ACK_CRD_YAML_LOCATION = (
        # "code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_hyperparametertuningjobs.yaml"
        "code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_trainingjobs.yaml"
    )
    ##############User inputs##############

    # From ACK CRD YAML, parse fields needed
    input_spec_required, input_spec_all, output_statuses, crd_name = parse_crd(
        ACK_CRD_YAML_LOCATION
    )

    ## prepare code snippet
    ack_job_request_outline_spec_buffer = get_ack_job_request_outline_spec(
        input_spec_all
    )

    ## set up output file directory
    output_src_dir = "code_gen/components/" + crd_name + "/src/"

    output_job_request_outline_location = (
        output_src_dir + crd_name + "_request.yaml.tpl"
    )
    job_request_location = output_src_dir + crd_name + "_request.yaml"


    ## replace placeholders in templates with buffer, then write to file
    ack_job_request_replace = {
        "CRD_NAME": crd_name,
        "CRD_NAME_LOWER": crd_name.lower(),
        "JOB_REQUEST_OUTLINE_SPEC": ack_job_request_outline_spec_buffer,
        "RAND_NUM": random.randrange(0, 99999, 1),
    }
    write_snippet_to_file(
        ack_job_request_replace,
        "code_gen/templates/ack_job_request.yaml.tpl",
        output_job_request_outline_location,
        output_src_dir,
    )
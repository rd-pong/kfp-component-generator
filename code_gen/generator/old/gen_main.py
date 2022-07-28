import random
from code_gen.generator.utils import (
    parse_crd,
    write_snippet_to_file,
)
from code_gen.generator.gen_comp_src import (
    get_py_add_argument,
    get_ack_job_request_outline_spec,
)
from code_gen.generator.gen_yaml import (
    get_yaml_inputs,
    get_yaml_args,
    get_yaml_outputs,
)

if __name__ == "__main__":

    ##############User inputs##############
    ACK_CRD_YAML_LOCATION = (
        # "code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_hyperparametertuningjobs.yaml"
        "code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_trainingjobs.yaml"
    )
    COMPONENT_CONTAINER_IMAGE = "rdpen/kfp-component-sagemaker:latest"
    ##############User inputs##############

    # From ACK CRD YAML, parse fields needed
    input_spec_required, input_spec_all, output_statuses, crd_name = parse_crd(
        ACK_CRD_YAML_LOCATION
    )

    # prepare code snippet for component.yaml
    yaml_inputs_buffer = get_yaml_inputs(input_spec_all)
    yaml_args_buffer = get_yaml_args(input_spec_all)
    yaml_outputs_buffer = get_yaml_outputs(output_statuses)

    # prepare code snippet for src/component.py
    py_add_argument_buffer = get_py_add_argument(input_spec_all, input_spec_required)

    # prepare code snippet for src/component_request.yaml.tpl
    ack_job_request_outline_spec_buffer = get_ack_job_request_outline_spec(
        input_spec_all
    )

    # set up output file directory/location
    output_component_dir = "code_gen/components/" + crd_name + "/"

    output_yaml_location = output_component_dir + "component.yaml"
    output_src_dir = output_component_dir + "src/"

    output_py_location = output_src_dir + crd_name + ".py"
    output_job_request_outline_location = (
        output_src_dir + crd_name + "_request.yaml.tpl"
    )
    job_request_location = output_src_dir + crd_name + "_request.yaml"

    # replace template placeholders with buffer, then write to file
    # (don't change the order, yaml comes first, create the /component dir first)
    yaml_replace = {
        "CRD_NAME": crd_name,
        "YAML_INPUTS": yaml_inputs_buffer,
        "YAML_OUTPUTS": yaml_outputs_buffer,
        "YAML_ARGS": yaml_args_buffer,
        "COMPONENT_CONTAINER_IMAGE": COMPONENT_CONTAINER_IMAGE,
    }
    write_snippet_to_file(
        yaml_replace,
        "code_gen/templates/component.yaml.tpl",
        output_yaml_location,
        output_component_dir,
    )

    py_replace = {
        "PY_ADD_ARGUMENT": py_add_argument_buffer,
        "JOB_REQUEST_OUTLINE_LOC": output_job_request_outline_location,
        "JOB_REQUEST_LOC": job_request_location,
    }
    write_snippet_to_file(
        py_replace,
        "code_gen/templates/component.py.tpl",
        output_py_location,
        output_src_dir,
    )

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

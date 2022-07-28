import random
from code_gen.generator.gen_component import (
    get_do_paramaters_snippet,
    get_output_prep_snippet,
)
from code_gen.generator.gen_request import get_ack_job_request_outline_spec
from code_gen.generator.gen_spec import (
    get_spec_input_snippets,
    get_spec_output_snippets,
)
from code_gen.generator.gen_yaml import get_yaml_args, get_yaml_inputs, get_yaml_outputs
from code_gen.generator.utils import (
    get_class_names,
    get_crd_info,
    parse_crd,
    write_snippet_to_file,
)


if __name__ == "__main__":

    ##############User inputs##############
    ACK_CRD_YAML_LOCATION = (
        "code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_hyperparametertuningjobs.yaml"
        # "code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_trainingjobs.yaml"
    )
    COMPONENT_CONTAINER_IMAGE = "rdpen/kfp-component-sagemaker:latest"
    ##############User inputs##############

    ## From ACK CRD YAML, parse fields needed
    input_spec_required, input_spec_all, output_statuses, crd_name = parse_crd(
        ACK_CRD_YAML_LOCATION
    )
    crd_info = get_crd_info(ACK_CRD_YAML_LOCATION)

    ## set up output file directory
    output_component_dir = "code_gen/components/" + crd_name + "/"
    output_src_dir = output_component_dir + "src/"

    output_spec_name = crd_name + "_spec.py"
    output_spec_path = output_src_dir + output_spec_name

    output_component_name = crd_name + "_component.py"
    output_component_path = output_src_dir + output_component_name

    output_job_request_outline_location = (
        output_src_dir + crd_name + "_request.yaml.tpl"
    )
    job_request_location = output_src_dir + crd_name + "_request.yaml"

    output_yaml_location = output_component_dir + "component.yaml"

    ## prepare code snippet

    (
        input_class_name,
        output_class_name,
        spec_class_name,
        component_class_name,
    ) = get_class_names(crd_name)

    # *_spec.py
    (
        spec_inputs_defi_snippet,
        spec_inputs_validators_snippet,
    ) = get_spec_input_snippets(input_spec_all, input_spec_required)

    (
        spec_outputs_defi_snippet,
        spec_outputs_validators_snippet,
    ) = get_spec_output_snippets(output_statuses)

    # *_component.py
    do_parameters_snippet = get_do_paramaters_snippet(
        output_src_dir, crd_name, crd_info
    )
    output_prep_snippet = get_output_prep_snippet(output_statuses)

    # *_request.yaml.tpl
    ack_job_request_outline_spec_snippet = get_ack_job_request_outline_spec(
        input_spec_all
    )

    # component.yaml
    yaml_inputs_snippet = get_yaml_inputs(input_spec_all)
    yaml_args_snippet = get_yaml_args(input_spec_all)
    yaml_outputs_snippet = get_yaml_outputs(output_statuses)


    ## replace placeholders in templates with snippet, then write to file
    spec_replace = {
        "CRD_NAME": crd_name,
        "INPUT_CLASS_NAME": input_class_name,
        "OUTPUT_CLASS_NAME": output_class_name,
        "SPEC_CLASS_NAME": spec_class_name,
        "SPEC_INPUT_DEFINITIONS": spec_inputs_defi_snippet,
        "SPEC_OUTPUT_DEFINITIONS": spec_outputs_defi_snippet,
        "SPEC_INPUT_VALIDATORS": spec_inputs_validators_snippet,
        "SPEC_OUTPUT_VALIDATORS": spec_outputs_validators_snippet,
    }
    write_snippet_to_file(
        spec_replace,
        "code_gen/templates/*_spec.py.tpl",
        output_spec_path,
        output_src_dir,
    )

    component_replace = {
        "CRD_NAME": crd_name,
        "CRD_NAME_LOWER": crd_name.lower(),
        "INPUT_CLASS_NAME": input_class_name,
        "OUTPUT_CLASS_NAME": output_class_name,
        "SPEC_CLASS_NAME": spec_class_name,
        "COMPONENT_CLASS_NAME": component_class_name,
        "DO_PARAMETERS": do_parameters_snippet,
        "OUTPUT_PREP": output_prep_snippet,
    }
    write_snippet_to_file(
        component_replace,
        "code_gen/templates/*_component.py.tpl",
        output_component_path,
        output_src_dir,
    )

    ack_job_request_replace = {
        "CRD_NAME": crd_name,
        "CRD_NAME_LOWER": crd_name.lower(),
        "JOB_REQUEST_OUTLINE_SPEC": ack_job_request_outline_spec_snippet,
    }
    write_snippet_to_file(
        ack_job_request_replace,
        "code_gen/templates/ack_job_request.yaml.tpl",
        output_job_request_outline_location,
        output_src_dir,
    )

    yaml_replace = {
        "CRD_NAME": crd_name,
        "YAML_INPUTS": yaml_inputs_snippet,
        "YAML_OUTPUTS": yaml_outputs_snippet,
        "YAML_ARGS": yaml_args_snippet,
        "COMPONENT_CONTAINER_IMAGE": COMPONENT_CONTAINER_IMAGE,
    }
    write_snippet_to_file(
        yaml_replace,
        "code_gen/templates/component.yaml.tpl",
        output_yaml_location,
        output_component_dir,
    )
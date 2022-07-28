from telnetlib import STATUS
from typing import Dict
from code_gen.generator.utils import (
    camel_to_snake,
    get_class_names,
    parse_crd,
    snake_to_camel,
    write_snippet_to_file,
)


CRD_TYPE_TO_ARGS_TYPE: Dict[str, str] = {
    "string": "str",
    "integer": "int",
    # "boolean": bool,
    # "string": SpecInputParsers.nullable_string_argument,
    "object": "SpecInputParsers.yaml_or_json_dict",
    "array": "SpecInputParsers.yaml_or_json_list",
    "boolean": "SpecInputParsers.str_to_bool",
}

## Generate src/*_spec.py content
def get_spec_input_snippets(_input_spec_all, _input_spec_required):
    _spec_inputs_defi_buffer = ""
    _spec_inputs_validators_buffer = ""

    for key in _input_spec_all:

        _spec_inputs_defi_buffer += """
    %s: Input""" % (
            camel_to_snake(key),
        )

        _spec_inputs_validators_buffer += """
        %s=InputValidator(
            input_type=%s,
            description="%s",
            required=%r
        ), """ % (
            camel_to_snake(key),
            CRD_TYPE_TO_ARGS_TYPE.get(_input_spec_all[key]["type"]),
            _input_spec_all[key]["description"][0:100].strip().split('\t'),
            key in _input_spec_required,
        )

    return (
        _spec_inputs_defi_buffer,
        _spec_inputs_validators_buffer,
    )


def get_spec_output_snippets(_output_statuses):
    _spec_outputs_defi_buffer = ""
    _spec_outputs_validators_buffer = ""

    for key in _output_statuses:
        _spec_outputs_defi_buffer += """
    %s: Output""" % (
            camel_to_snake(key),
        )

        _spec_outputs_validators_buffer += """
        %s=OutputValidator(
            description="%s",
        ), """ % (
            camel_to_snake(key),
            _output_statuses[key]["description"][0:100].strip().split('\t'),
        )

    return (
        _spec_outputs_defi_buffer,
        _spec_outputs_validators_buffer,
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

    ## prepare code snippet
    (
        spec_inputs_defi_buffer,
        spec_inputs_validators_buffer,
    ) = get_spec_input_snippets(input_spec_all, input_spec_required)

    (
        spec_outputs_defi_buffer,
        spec_outputs_validators_buffer,
    ) = get_spec_output_snippets(output_statuses)

    (
        input_class_name,
        output_class_name,
        spec_class_name,
        component_class_name,
    ) = get_class_names(crd_name)

    ## set up output file directory
    output_component_dir = "code_gen/components/" + crd_name + "/"
    output_src_dir = output_component_dir + "src/"
    output_spec_name = crd_name + "_spec.py"
    output_spec_path = output_src_dir + output_spec_name

    ## replace placeholders in templates with buffer, then write to file
    spec_replace = {
        "CRD_NAME": crd_name,
        "INPUT_CLASS_NAME": input_class_name,
        "OUTPUT_CLASS_NAME": output_class_name,
        "SPEC_CLASS_NAME": spec_class_name,
        "SPEC_INPUT_DEFINITIONS": spec_inputs_defi_buffer,
        "SPEC_OUTPUT_DEFINITIONS": spec_outputs_defi_buffer,
        "SPEC_INPUT_VALIDATORS": spec_inputs_validators_buffer,
        "SPEC_OUTPUT_VALIDATORS": spec_outputs_validators_buffer,
    }
    write_snippet_to_file(
        spec_replace,
        "code_gen/templates/*_spec.py.tpl",
        output_spec_path,
        output_src_dir,
    )

from telnetlib import STATUS
from typing import Dict
from code_gen.generator.utils import (
    camel_to_snake,
    get_class_names,
    get_crd_info,
    parse_crd,
    snake_to_camel,
    write_snippet_to_file,
)


def get_do_paramaters_snippet(_output_src_dir, _crd_name, _crd_info):

    group, version, plural, namespace = _crd_info

    _snippet = """
        self.group = "%s"
        self.version = "%s"
        self.plural = "%s"
        self.namespace = "%s"

        self.job_request_outline_location = (
            "%s"
        )
        self.job_request_location = (
            "%s"
        )""" % (
        group,
        version,
        plural,
        namespace,
        _output_src_dir + _crd_name + "_request.yaml.tpl",
        _output_src_dir + _crd_name + "_request.yaml",
    )

    return _snippet


def get_output_prep_snippet(_output_statuses):

    _snippet = ""

    for key in _output_statuses:

        _snippet += """
        outputs.%s = (
            ack_statuses["%s"]
            if "%s" in ack_statuses
            else None
        )""" % (
            camel_to_snake(key),
            key,
            key,
        )

    return _snippet


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

    crd_info = get_crd_info(ACK_CRD_YAML_LOCATION)

    ## set up output file directory
    output_component_dir = "code_gen/components/" + crd_name + "/"
    output_src_dir = output_component_dir + "src/"
    output_component_name = crd_name + "_component.py"
    output_component_path = output_src_dir + output_component_name

    output_job_request_outline_location = (
        output_src_dir + crd_name + "_request.yaml.tpl"
    )

    ## prepare code snippets
    (
        input_class_name,
        output_class_name,
        spec_class_name,
        component_class_name,
    ) = get_class_names(crd_name)

    do_parameters_snippet = get_do_paramaters_snippet(output_src_dir, crd_name, crd_info)
    output_prep_snippet = get_output_prep_snippet(output_statuses)

    ## replace placeholders in templates with buffer, then write to file
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

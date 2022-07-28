import random, yaml, re, os, string
from string import Template
from typing import Callable, Dict, Type, Union, List, NamedTuple, cast

from code_gen.common.spec_input_parsers import SpecInputParsers


# Run this script in /kfp-component-generator

##############User inputs##############
ACK_CRD_YAML_LOCATION = (
    "code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_hyperparametertuningjobs.yaml"
    # "code_gen/ack_crd_v0.3.3/sagemaker.services.k8s.aws_trainingjobs.yaml"
)
COMPONENT_CONTAINER_IMAGE = "rdpen/kfp-component-sagemaker:latest"
##############User inputs##############

# type conversion table (reference: KFP_TYPE_FROM_ARGS)
CRD_TYPE_TO_KFP_TYPE: Dict[str, str] = {
    "string": "String",
    "integer": "Integer",
    "boolean": "Bool",
    # SpecInputParsers.nullable_string_argument: "String", # todo
    "object": "JsonObject",
    "array": "JsonArray",
    # SpecInputParsers.str_to_bool: "Bool",
}

CRD_TYPE_TO_ARGS_TYPE: Dict[str, str] = {
    "string": "str",
    "integer": "int",
    # "boolean": bool,
    # "string": SpecInputParsers.nullable_string_argument,
    "object": "SpecInputParsers.yaml_or_json_dict",
    "array": "SpecInputParsers.yaml_or_json_list",
    "boolean": "SpecInputParsers.str_to_bool",
}

CRD_TYPE_TO_DEFAULT_VALUE: Dict[str, str] = {
    "string": """''""",
    "integer": 0,
    "boolean": """False""",
    "object": """'{}'""",
    "array": """'[]'""",
}


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def snake_to_camel(name):
    if name == "role_arn":
        return "roleARN"
    temp = name.split("_")
    return temp[0] + "".join(ele.title() for ele in temp[1:])


def parse_crd(_file_name):
    """
    Read in ACK CRD YAML file from file location
    Parse file and get fields
    """

    with open(_file_name, "r") as crd_file:
        crd_dict = yaml.load(crd_file, Loader=yaml.FullLoader)

        _input_spec_required = crd_dict["spec"]["versions"][0]["schema"][
            "openAPIV3Schema"
        ]["properties"]["spec"]["required"]
        _input_spec_all = crd_dict["spec"]["versions"][0]["schema"]["openAPIV3Schema"][
            "properties"
        ]["spec"]["properties"]
        _output_statuses = crd_dict["spec"]["versions"][0]["schema"]["openAPIV3Schema"][
            "properties"
        ]["status"]["properties"]
        _crd_name = crd_dict["spec"]["names"]["kind"]

    return _input_spec_required, _input_spec_all, _output_statuses, _crd_name


## Generate src/component.py content
def get_py_add_argument(_input_spec_all, _input_spec_required):
    """
    Populate parser.add_argument with name, type, description, ..
    Return a code snippet waiting to be written to component.py.tpl template
    """

    _py_add_argument_buffer = ""

    for key in _input_spec_all:
        _py_add_argument_buffer += """
    parser.add_argument(
        "--%s",
        type=%s,
        help="%s",
        required=%r
    )""" % (
            camel_to_snake(key),
            CRD_TYPE_TO_ARGS_TYPE.get(_input_spec_all[key]["type"]),
            _input_spec_all[key]["description"][0:50],
            key in _input_spec_required,
        )

    return _py_add_argument_buffer


## Generate component.yaml content
def get_yaml_inputs(_input_spec_all):
    """
    Populate input section with name, type, description, ..
    Return a code snippet waiting to be written to component.yaml.tpl template
    """

    _yaml_inputs_buffer = ""

    for key in _input_spec_all:
        _yaml_inputs_buffer += """
  - {
      name: %s,
      type: %s,
      default: %s,
      description: "%s",
    }""" % (
            camel_to_snake(key),
            CRD_TYPE_TO_KFP_TYPE.get(_input_spec_all[key]["type"]),
            CRD_TYPE_TO_DEFAULT_VALUE.get(_input_spec_all[key]["type"]),
            _input_spec_all[key]["description"][0:50],
        )

    return _yaml_inputs_buffer


def get_yaml_args(_input_spec_all):
    """
    Populate args section with name, type, description, ..
    Return a code snippet waiting to be written to component.yaml.tpl template
    """

    _yaml_args_buffer = ""

    for key in _input_spec_all:
        key = camel_to_snake(key)
        _yaml_args_buffer += """- --%s\n      - { inputValue: %s }
      """ % (
            key,
            key,
        )

    return _yaml_args_buffer


def get_yaml_outputs(_output_statuses):
    """
    Populate output section with name, type, description, ..
    Return a code snippet waiting to be written to component.yaml.tpl template
    """

    _yaml_outputs_buffer = ""

    for key in _output_statuses:
        _yaml_outputs_buffer += """
#  - {
#      name: %s,
#      type: %s,
#      description: "%s",
#    }""" % (
            camel_to_snake(key),
            CRD_TYPE_TO_KFP_TYPE.get(_output_statuses[key]["type"]),
            _output_statuses[key]["description"][0:50],
        )

    return _yaml_outputs_buffer


## Generate pipeline/component-pipeline.py content
def get_pipeline_user_inputs(_input_spec_all):
    """
    Populate user input section in a sample pipeline
    Return a code snippet waiting to be written to pipeline.py.tpl template
    """
    _pipeline_user_inputs_buffer = ""

    for key in _input_spec_all:
        _pipeline_user_inputs_buffer += """\t%s = ,\n""" % camel_to_snake(key)

    return _pipeline_user_inputs_buffer


def get_pipeline_args_assign(_input_spec_all):
    """
    Populate args section in a sample pipeline
    Return a code snippet waiting to be written to pipeline.py.tpl template
    """
    _pipeline_args_assign_buffer = ""

    for key in _input_spec_all:
        _pipeline_args_assign_buffer += """\t\t%s = %s,\n""" % (
            camel_to_snake(key),
            camel_to_snake(key),
        )

    return _pipeline_args_assign_buffer


## Generate src/component_request.yaml.tpl content
def get_ack_job_request_outline_spec(_input_spec_all):
    """
    Populate spec section in a ACK job request YAML
    Return a code snippet waiting to be written to ack_job_request.yaml.tpl template
    """
    _ack_job_request_outline_spec_buffer = ""

    for key in _input_spec_all:
        _ack_job_request_outline_spec_buffer += """  %s: \n""" % snake_to_camel(key)

    return _ack_job_request_outline_spec_buffer


def write_buffer_to_file(_replace_dict, _template_loc, _out_file_loc, _out_file_dir):
    """
    Open template file at _template_loc
    Substite placeholders in templates following mapping _replace_dict
    Create a dir _out_file_dir, if does not exist
    Write output file stream to file _out_file_loc
    """

    # replace placeholders in templates
    with open(_template_loc) as t:
        template = string.Template(t.read())
        file_draft = template.safe_substitute(_replace_dict)

    # if output dir not exist, create one and write to file
    if not os.path.exists(_out_file_dir):
        os.makedirs(_out_file_dir)
    with open(_out_file_loc, "w+") as f:
        f.write(file_draft)

    print("CREATED: " + _out_file_loc)


##############################

if __name__ == "__main__":
    # From ACK CRD YAML, parse fields needed
    input_spec_required, input_spec_all, output_statuses, crd_name = parse_crd(
        ACK_CRD_YAML_LOCATION
    )

    # get code snippet (buffer) to be filled in templates
    py_add_argument_buffer = get_py_add_argument(input_spec_all, input_spec_required)
    
    yaml_inputs_buffer = get_yaml_inputs(input_spec_all)
    yaml_args_buffer = get_yaml_args(input_spec_all)
    yaml_outputs_buffer = get_yaml_outputs(output_statuses)

    pipeline_user_inputs_buffer = get_pipeline_user_inputs(input_spec_all)
    pipeline_args_assign_buffer = get_pipeline_args_assign(input_spec_all)
    
    ack_job_request_outline_spec_buffer = get_ack_job_request_outline_spec(
        input_spec_all
    )

    # set up output file directory/location
    output_component_dir = "code_gen/components/" + crd_name + "/"

    output_pipeline_dir = output_component_dir + "pipeline/"
    output_pipeline_location = output_pipeline_dir + crd_name + "-pipeline" + ".py"

    output_yaml_location = output_component_dir + "component.yaml"
    output_src_dir = output_component_dir + "src/"

    output_py_location = output_src_dir + crd_name + ".py"
    output_job_request_outline_location = output_src_dir + crd_name + "_request.yaml.tpl"
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
    write_buffer_to_file(
        yaml_replace,
        "code_gen/templates/component.yaml.tpl",
        output_yaml_location,
        output_component_dir,
    )

    pipeline_replace = {
        "PIPELINE_USER_INPUTS": pipeline_user_inputs_buffer,
        "PIPELINE_ARGS_ASSIGN": pipeline_args_assign_buffer,
        "CRD_NAME": crd_name,
    }
    write_buffer_to_file(
        pipeline_replace,
        "code_gen/templates/pipeline.py.tpl",
        output_pipeline_location,
        output_pipeline_dir,
    )

    py_replace = {
        "PY_ADD_ARGUMENT": py_add_argument_buffer,
        "JOB_REQUEST_OUTLINE_LOC": output_job_request_outline_location,
        "JOB_REQUEST_LOC": job_request_location,
    }
    write_buffer_to_file(
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
    write_buffer_to_file(
        ack_job_request_replace,
        "code_gen/templates/ack_job_request.yaml.tpl",
        output_job_request_outline_location,
        output_src_dir,
    )

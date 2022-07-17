from typing import Dict
from code_gen.generator.gen_utils import camel_to_snake, snake_to_camel

CRD_TYPE_TO_ARGS_TYPE: Dict[str, str] = {
    "string": "str",
    "integer": "int",
    # "boolean": bool,
    # "string": SpecInputParsers.nullable_string_argument,
    "object": "SpecInputParsers.yaml_or_json_dict",
    "array": "SpecInputParsers.yaml_or_json_list",
    "boolean": "SpecInputParsers.str_to_bool",
}

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


## Generate src/component-request.yaml.tpl content
def get_ack_job_request_outline_spec(_input_spec_all):
    """
    Populate spec section in a ACK job request YAML
    Return a code snippet waiting to be written to ack_job_request.yaml.tpl template
    """
    _ack_job_request_outline_spec_buffer = ""

    for key in _input_spec_all:
        _ack_job_request_outline_spec_buffer += """  %s: \n""" % snake_to_camel(key)

    return _ack_job_request_outline_spec_buffer

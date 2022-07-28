from typing import Dict
from code_gen.generator.utils import camel_to_snake, snake_to_camel

CRD_TYPE_TO_KFP_TYPE: Dict[str, str] = {
    "string": "String",
    "integer": "Integer",
    "boolean": "Bool",
    # SpecInputParsers.nullable_string_argument: "String", # todo
    "object": "JsonObject",
    "array": "JsonArray",
    # SpecInputParsers.str_to_bool: "Bool",
}

CRD_TYPE_TO_DEFAULT_VALUE: Dict[str, str] = {
    "string": """''""",
    "integer": 0,
    "boolean": """False""",
    "object": """'{}'""",
    "array": """'[]'""",
}

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

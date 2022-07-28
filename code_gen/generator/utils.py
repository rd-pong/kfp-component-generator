import random
import yaml, re, os
from string import Template
import string
from typing import Callable, Dict, Type, Union, List, NamedTuple, cast
from code_gen.common.spec_input_parsers import SpecInputParsers


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


def get_crd_info(_file_name):
    with open(_file_name, "r") as crd_file:
        crd_dict = yaml.load(crd_file, Loader=yaml.FullLoader)

    _group = crd_dict["spec"]["group"]
    _plural = crd_dict["spec"]["names"]["plural"]
    _version = crd_dict["spec"]["versions"][0]["name"]
    _namespace = "default" if crd_dict["spec"]["scope"] == "Namespaced" else ""

    return _group, _version, _plural, _namespace


def get_class_names(_crd_name):
    _input_class_name = "SageMaker" + _crd_name + "Inputs"
    _output_class_name = "SageMaker" + _crd_name + "Outputs"
    _spec_class_name = "SageMaker" + _crd_name + "Spec"
    _component_class_name = "SageMaker" + _crd_name + "Component"

    return (
        _input_class_name,
        _output_class_name,
        _spec_class_name,
        _component_class_name,
    )


def write_snippet_to_file(_replace_dict, _template_loc, _out_file_loc, _out_file_dir):
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

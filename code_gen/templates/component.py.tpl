import argparse
import yaml
import logging
import os
from kubernetes import client, config, utils
from common.spec_input_parsers import SpecInputParsers


def snake_to_camel(name):
    """
    Convert snake case string to camel Case
    """
    if name == "role_arn":
        return "roleARN"
    temp = name.split('_')
    return temp[0] + ''.join(ele.title() for ele in temp[1:])


def build_job_yaml(_args):
    """
    Read the outline file src/component_request.yaml.tpl 
    Build an ack job (custom object) yaml file with user input args.
    Write the yaml file to src/component_request.yaml.
    """
    with open(
        "${JOB_REQUEST_OUTLINE_LOC}", 'r'
    ) as job_request_outline:
        job_request_dict = yaml.load(job_request_outline, Loader=yaml.FullLoader)
        job_request_spec = job_request_dict["spec"]
        for para in vars(_args):
            camel_para = snake_to_camel(para)
            if camel_para in job_request_spec:
                job_request_spec[camel_para] = getattr(_args, para)
        
        # print(job_request_spec)

        job_request_dict['spec'] = job_request_spec

        # print(job_request_dict)

        out_loc = "${JOB_REQUEST_LOC}"
        with open(out_loc, 'w+') as f:
            yaml.dump(job_request_dict, f, default_flow_style=False)
        print("CREATED: " + out_loc)


def main():
    parser = argparse.ArgumentParser()

    ###########################GENERATED SECTION BELOW############################
    ${PY_ADD_ARGUMENT}
    ###########################GENERATED SECTION ABOVE############################

    args = parser.parse_args()

    # logging.critical("----------------Print args below...-----------------")
    # logging.critical("Parsed args: %s", vars(args))
    # logging.critical("----------------------------------------------------")

    build_job_yaml(args)


if __name__ == "__main__":
    main()

import argparse
import yaml
import logging
import os
from kubernetes import client, config, utils
from common.spec_input_parsers import SpecInputParsers


def snake_to_camel(name):
    if name == "role_arn":
        return "roleARN"
    temp = name.split("_")
    return temp[0] + "".join(ele.title() for ele in temp[1:])


def build_job_yaml(_args):
    
    with open(
        "code_gen/components/TrainingJob/src/TrainingJob_request.yaml.tpl", "r"
    ) as job_request_outline:
        job_request_dict = yaml.load(job_request_outline, Loader=yaml.FullLoader)
        job_request_spec = job_request_dict["spec"]
        for para in vars(_args):
            camel_para = snake_to_camel(para)
            if camel_para in job_request_spec:
                job_request_spec[camel_para] = getattr(_args, para)

        # print(job_request_spec)

        job_request_dict["spec"] = job_request_spec

        # print(job_request_dict)

        out_loc = "code_gen/components/TrainingJob/src/TrainingJob_request.yaml"
        with open(out_loc, "w+") as f:
            yaml.dump(job_request_dict, f, default_flow_style=False)
        print("CREATED: " + out_loc)


def main():
    parser = argparse.ArgumentParser()

    ###########################GENERATED SECTION BELOW############################

    parser.add_argument(
        "--algorithm_specification",
        type=SpecInputParsers.yaml_or_json_dict,
        help="The registry path of the Docker image that contain",
        required=True,
    )
    parser.add_argument(
        "--checkpoint_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="Contains information about the output location for",
        required=False,
    )
    parser.add_argument(
        "--debug_hook_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="Configuration information for the Debugger hook pa",
        required=False,
    )
    parser.add_argument(
        "--debug_rule_configurations",
        type=SpecInputParsers.yaml_or_json_list,
        help="Configuration information for Debugger rules for d",
        required=False,
    )
    parser.add_argument(
        "--enable_inter_container_traffic_encryption",
        type=SpecInputParsers.str_to_bool,
        help="To encrypt all communications between ML compute i",
        required=False,
    )
    parser.add_argument(
        "--enable_managed_spot_training",
        type=SpecInputParsers.str_to_bool,
        help="To train models using managed spot training, choos",
        required=False,
    )
    parser.add_argument(
        "--enable_network_isolation",
        type=SpecInputParsers.str_to_bool,
        help="Isolates the training container. No inbound or out",
        required=False,
    )
    parser.add_argument(
        "--environment",
        type=SpecInputParsers.yaml_or_json_dict,
        help="The environment variables to set in the Docker con",
        required=False,
    )
    parser.add_argument(
        "--experiment_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="Associates a SageMaker job as a trial component wi",
        required=False,
    )
    parser.add_argument(
        "--hyper_parameters",
        type=SpecInputParsers.yaml_or_json_dict,
        help="Algorithm-specific parameters that influence the q",
        required=False,
    )
    parser.add_argument(
        "--input_data_config",
        type=SpecInputParsers.yaml_or_json_list,
        help="An array of Channel objects. Each channel is a nam",
        required=False,
    )
    parser.add_argument(
        "--output_data_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="Specifies the path to the S3 location where you wa",
        required=True,
    )
    parser.add_argument(
        "--profiler_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="Configuration information for Debugger system moni",
        required=False,
    )
    parser.add_argument(
        "--profiler_rule_configurations",
        type=SpecInputParsers.yaml_or_json_list,
        help="Configuration information for Debugger rules for p",
        required=False,
    )
    parser.add_argument(
        "--resource_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="The resources, including the ML compute instances ",
        required=True,
    )
    parser.add_argument(
        "--role_arn",
        type=str,
        help="The Amazon Resource Name (ARN) of an IAM role that",
        required=True,
    )
    parser.add_argument(
        "--stopping_condition",
        type=SpecInputParsers.yaml_or_json_dict,
        help="Specifies a limit to how long a model training job",
        required=True,
    )
    parser.add_argument(
        "--tags",
        type=SpecInputParsers.yaml_or_json_list,
        help="An array of key-value pairs. You can use tags to c",
        required=False,
    )
    parser.add_argument(
        "--tensor_board_output_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="Configuration of storage locations for the Debugge",
        required=False,
    )
    parser.add_argument(
        "--training_job_name",
        type=str,
        help="The name of the training job. The name must be uni",
        required=True,
    )
    parser.add_argument(
        "--vpc_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="A VpcConfig object that specifies the VPC that you",
        required=False,
    )
    ###########################GENERATED SECTION ABOVE############################

    args = parser.parse_args()

    logging.critical("Print args below...")
    logging.critical("Parsed args: %s", vars(args))
    logging.critical("----------------------------------------------------")

    build_job_yaml(args)


if __name__ == "__main__":
    main()

import argparse
import yaml
import logging
import os
from kubernetes import client, config, utils
from code_gen.common.spec_input_parsers import SpecInputParsers


def snake_to_camel(name):
    temp = name.split("_")
    return temp[0] + "".join(ele.title() for ele in temp[1:])


def build_job_yaml(_args):
    with open(
        "code_gen/components/HyperParameterTuningJob1/src/HyperParameterTuningJob.yaml.tpl",
        "r",
    ) as job_request_template:
        job_request_dict = yaml.load(job_request_template, Loader=yaml.FullLoader)
        job_request_spec = job_request_dict["spec"]
        for para in vars(_args):
            camel_para = snake_to_camel(para)
            if camel_para in job_request_spec:
                job_request_spec[camel_para] = getattr(_args, para)

        # print(job_request_spec)

        job_request_dict["spec"] = job_request_spec

        # print(job_request_dict)

        out_loc = "code_gen/components/HyperParameterTuningJob1/src/HyperParameterTuningJob.yaml"
        with open(out_loc, "w+") as f:
            yaml.dump(job_request_dict, f, default_flow_style=False)
        print("CREATED: " + out_loc)


def main():
    parser = argparse.ArgumentParser()

    ###########################GENERATED SECTION BELOW############################

    parser.add_argument(
        "--hyper_parameter_tuning_job_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="The HyperParameterTuningJobConfig object that desc",
        required=True,
    )
    parser.add_argument(
        "--hyper_parameter_tuning_job_name",
        type=str,
        help="The name of the tuning job. This name is the prefi",
        required=True,
    )
    parser.add_argument(
        "--tags",
        type=SpecInputParsers.yaml_or_json_list,
        help="An array of key-value pairs. You can use tags to c",
        required=False,
    )
    parser.add_argument(
        "--training_job_definition",
        type=SpecInputParsers.yaml_or_json_dict,
        help="The HyperParameterTrainingJobDefinition object tha",
        required=False,
    )
    parser.add_argument(
        "--training_job_definitions",
        type=SpecInputParsers.yaml_or_json_list,
        help="A list of the HyperParameterTrainingJobDefinition ",
        required=False,
    )
    parser.add_argument(
        "--warm_start_config",
        type=SpecInputParsers.yaml_or_json_dict,
        help="Specifies the configuration for starting the hyper",
        required=False,
    )
    ###########################GENERATED SECTION ABOVE############################

    args = parser.parse_args()

    logging.info("Testing----------------")
    logging.info("\n")
    logging.info(args.hyper_parameter_tuning_job_config)
    logging.info("\n")
    logging.info(args.hyper_parameter_tuning_job_name)
    logging.info("\n")
    logging.info(args.tags)
    logging.info("\n")
    logging.info(args.training_job_definition)
    logging.info("\n")
    logging.info(args.training_job_definitions)
    logging.info("\n")
    logging.info(args.warm_start_config)
    logging.info("\n")

    # print(args.hyper_parameter_tuning_job_config)
    # print(args.hyper_parameter_tuning_job_name)
    # print(args.warm_start_config)

    build_job_yaml(args)


if __name__ == "__main__":
    main()

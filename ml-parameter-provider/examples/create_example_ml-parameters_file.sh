#!/bin/bash

# This script generates a ml-parameters.json file based on given arguments 
# and template-ml-parameters.json file. 
# You have to install jq (https://stedolan.github.io/jq/download/) application to use this script!
# It can be executed with the following command:
# bash examples/create_example_ml-parameters_file.sh --account <account-id> --region <region> --bucket <s3bucket> --training_sg <training-security-group-id> --training_subnets "<subnet-id-1>,<subnet-id-2>,<subnet-id-3>" --hosting_sg <hosting-security-group-id> --hosting_subnets "<subnet-id-1>,<subnet-id-2>,<subnet-id-3>"

while [ $# -gt 0 ]; do

   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
        # echo $1 $2 // Optional to see the parameter:value result
   fi

  shift
done

if [ "$account" == "" ] || [ "$region" == "" ] || [ "$bucket" == "" ] || [ "${training_sg}" == "" ] || [ "${training_subnets}" == "" ] || [ "${hosting_sg}" == "" ] || [ "${hosting_subnets}" == "" ]
then
    echo "Usage: $0 bash examples/create_example_ml-parameters_file.sh --account <account-id> --region <region> --bucket <s3bucket> --training_sg <training-security-group-id> --training_subnets \"<subnet-id-1>,<subnet-id-2>,<subnet-id-3>\" --hosting_sg <hosting-security-group-id> --hosting_subnets \"<subnet-id-1>,<subnet-id-2>,<subnet-id-3>\""
    exit 1
fi


# Generates ml-parameters.json file
[ -e examples/ml-parameters.json ] && rm examples/ml-parameters.json
jq_ops="."
jq_ops+=" | .algorithmARN |= \"arn:aws:sagemaker:${region}:${account}:algorithm/h2o-gbm-algorithm\""
jq_ops+=" | .spotTrainingCheckpointS3Uri |= \"s3://${bucket}/model-training-checkpoint/\""
jq_ops+=" | .model.artifactsS3OutputPath |= \"s3://${bucket}/model-artifacts/\""
jq_ops+=" | .model.trainingSecurityGroupIds[0] |= \"${training_sg}\""
jq_ops+=" | .model.trainingSubnets |= (\"${training_subnets}\" | split(\",\"))"
jq_ops+=" | .model.hosting.securityGroupIds[0] |= \"${hosting_sg}\""
jq_ops+=" | .model.hosting.subnets |= (\"${hosting_subnets}\" | split(\",\"))"
cat "examples/template-ml-parameters.json" | jq -r "${jq_ops}" > examples/ml-parameters.json

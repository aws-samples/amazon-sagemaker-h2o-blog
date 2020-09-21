#!/usr/bin/env bash
# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/

# This script shows how to build the Docker image and push it to ECR to be ready for use
# by SageMaker.

# The argument to this script is the image name. This will be used as the image on the local
# machine and combined with the account and region to form the repository name for ECR.

image=$1
region=$2

if [ "$image" == "" ] || [ "$region" == "" ]
then
    echo "Usage: $0 <image-name> <region>"
    exit 1
fi

# Get the account number associated with the current IAM credentials
account=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]
then
    exit 255
fi

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --region ${region} --repository-names "${image}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --region ${region} --repository-name "${image}" > /dev/null
fi

# Get the login command from ECR and execute it directly
$(aws ecr get-login-password --region ${region}  | docker login --username AWS --password-stdin ${account}.dkr.ecr.${region}.amazonaws.com)

# Push the docker image to ECR with the full name.
docker tag ${image} ${fullname}
docker push ${fullname}

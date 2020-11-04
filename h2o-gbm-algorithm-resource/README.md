<p align="center">
  <img width="250" src="assets/icon.jpg" />
</p>

# h2o-gbm-algorithm-resource
> A Sagemaker Algorithm Resource for H2O Gradient Boosting Machines (GBM) as a Cloudformation stack.

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](contributing.md)
[![CodeBuild](https://s3-us-west-2.amazonaws.com/codefactory-us-west-2-prod-default-build-badges/passing.svg)](https://s3-us-west-2.amazonaws.com/codefactory-us-west-2-prod-default-build-badges/passing.svg)

Current version: **1.0.0**

Lead Maintainer: [Anil Sener](mailto:senera@amazon.com)

## 📋 Table of content

 - [Installation](#-install)
 - [Metrics](#-metrics)
 - [Pre-requisites](#-pre-requisites)
 - [Description](#-description)
 - [Usage](#-usage)
 - [See also](#-see-also)

## 🚀 Install

In order to add this block, head to your project directory in your terminal and add it using NPM.
Execute the following command to create a [Sagemaker Algorithm Resource](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-mkt-create-algo.html):

#### Linux/MacOs:

```sh
npm run deploy --region=<region> \
--account_id=<account-id> \
--s3bucket=<s3bucket> \
--environment=development \
--training_image_name=h2o-gbm-trainer \
--inference_image_name=h2o-gbm-predictor
```

## Windows:

```sh
npm run deploy-win ^
--region=<region> ^
--account_id=<account-id> ^
--s3bucket=<s3bucket> ^
--environment=development ^
--training_image_name=h2o-gbm-trainer ^
--inference_image_name=h2o-gbm-predictor
```

> ⚠️ You need to have the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) installed on your deployment machine before installing this package.

## 📊 Metrics

The below metrics displays approximate values associated with deploying and using this block.

Metric | Value
------ | ------
**Type** | Resource
**Installation Time** | Less than 2 minutes
**Audience** | Developers, Solutions Architects, Data Scientists
**Requirements** | [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html),[Node Package Manager](https://www.npmjs.com/get-npm)

## 🎒 Pre-requisites

 - Make sure that you have installed the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) on your deployment machine.
 - Make sure that you have created a custom Sagemaker Training Image on Amazon ECR as in [H2O GBM Trainer](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-trainer) project.
 - Make sure that you have created a custom Sagemaker Inference Image on Amazon ECR as in [H2O GBM Predictor](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-predictor) project.


## 🔰 Description

This block is to create a [Sagemaker Algorithm Resource](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-mkt-create-algo.html) for [H2O Gradient Boosting Machines (GBM)](http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/gbm.html) Estimator.

> This project supports H2O version 3.30.

## 🛠 Usage

A Sagemaker Algorithm Resource is created to support the [Bring Your Algorithm](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms.html) and/or [Bring Your Own Model](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms.html) approaches for Amazon Sagemaker Model Training and Deployment process. 

You can use this block as a standalone [Sagemaker Algorithm Resource](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-mkt-create-algo.html) or an input for other projects such as [Sagemaker Model Tuner with Endpoint Deployment](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment) or [Sagemaker Model Tuner](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner).

### Deployment Options

The deployment options that you can pass to this solution are described below.

Name           | Default value | Description
-------------- | ------------- | -----------
**region** | None | AWS Region to deploy the infrastructure for Sagemaker Algorithm Resource.
**account_id** | None | AWS Account ID to deploy the infrastructure for Sagemaker Algorithm Resource.
**s3bucket** | None | Please set the S3 bucket to deploy the stack packages.
**environment** | `development` | Environment to tag the created resources.
**AlgorithmName** | None | Unique name of [Sagemaker Algorithm Resource](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-mkt-create-algo.html). 
**TrainingImageURI** | None | URI of custom Training Image on Amazon ECR.
**InferenceImageURI** | None | URI of custom Inference Image on Amazon ECR.


## 👀 See also

In this section, you can list the projects and blocks on which you depend, or which are linked to your block.

 - The [Docker](https://docs.docker.com/) official documentation.
 - The [AWS Sagemaker](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html) official documentation.
 - The [H2O GBM Trainer](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-trainer) project.
 - The [H2O GBM Predictor](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-predictor) project.
 - The [Sagemaker Model Tuner](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner) project.
 - The [Sagemaker Model Tuner with Endpoint Deployment](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment) project.

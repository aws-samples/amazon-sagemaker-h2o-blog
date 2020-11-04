<p align="center">
  <img width="250" src="assets/icon.jpg" />
</p>

# h2o-gbm-trainer
> A project to create a Sagemaker Model Training Docker image for H2O GBM Estimator.

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](contributing.md)
[![CodeBuild](https://s3-us-west-2.amazonaws.com/codefactory-us-west-2-prod-default-build-badges/passing.svg)](https://s3-us-west-2.amazonaws.com/codefactory-us-west-2-prod-default-build-badges/passing.svg)

Current version: **1.0.0**

Lead Maintainer: [Anil Sener](mailto:senera@amazon.com)

## 📋 Table of content

 - [Pre-requisites](#-pre-requisites)
 - [Installation](#-install)
 - [Metrics](#-metrics)
 - [Features](#-features)
 - [Description](#-description)
 - [Building the Docker Image](#-building-the-docker-image)
 - [Testing in Local](#-testing-in-local)
 - [Deploying the Docker Image](#-deploying-the-docker-image)
 - [Usage](#-usage)
 - [See also](#-see-also)

## 🎒 Pre-requisites

 - You should have Administrator rights in your PC if you are a Windows user. If you are a Linux or MacOS user, your used should be a member of “docker” group.
 - If you are Windows user, [AWS Tools for Powershell](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-getting-set-up-windows.html) will be automatically installed to your PC by the deployment windows batch scripts (Minimum PowerShell version is 5.1).

## 🚀 Install

In order to add this block, head to your project directory in your terminal and add it using NPM.
You can build and push the Docker image created to Amazon ECR by executing the command below.

#### Linux/MacOs:

```sh
npm run deploy --region=<region>
```

#### Windows:

```sh
npm run deploy-win --region=<region>
```


## 📊 Metrics

The below metrics displays approximate values associated with deploying and using this block.

Metric | Value
------ | ------
**Type** | Resource
**Compilation Time** | Depends on your network bandwith
**Deployment Time** | Depends on your network bandwith
**Audience** | Developers, Solutions Architects, Data Scientists
**Requirements** | [Docker Engine](https://docs.docker.com/engine/install/),[Node Package Manager](https://www.npmjs.com/get-npm)

## 🔖 Features

 - Option to create [Model ObJect, Optimized](https://www.h2o.ai/community/glossary/model-object-optimized-mojo) (MOJO) and [Binary Model](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/save-and-load-model.html#binary-models) artifacts trained with [H2O](https://www.h2o.ai/) machine learning framework.
 - A [`Dockerfile`](./Dockerfile) build file which provides the dependencies that the image requires.

## 🔰 Description

This block is to create a Model Training Docker image for [H2O Gradient Boosting Machines (GBM) Estimator](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiHhOn5l4nrAhViTRUIHT51BjsQFjAAegQIARAC&url=https%3A%2F%2Fdocs.h2o.ai%2Fh2o%2Flatest-stable%2Fh2o-docs%2Fdata-science%2Fgbm.html&usg=AOvVaw1kTu8JkgeTw_lasTS927vl) for Amazon Sagemaker.

> This project supports Python 3.x and H2O 3.30.

## ⚡️ Building the Docker Image

In order to build the [`Dockerfile`](./Dockerfile) file associated with this library, you will need to have [Docker Engine](https://docs.docker.com/engine/install/) and [Node Package Manager](https://www.npmjs.com/get-npm) installed on your development or build machine. You can then navigate to the project base directory and execute the command below.

Linux/MacOs:

```sh
npm run build --build_mode=aws
```

#### Windows:

```sh
npm run build-win --build_mode=aws
```


## 🔖 Testing in Local

You can build and test the Docker image created in your local PC by executing the command below.

#### Linux/MacOs:

```sh
npm run test-local
```

#### Windows:

```sh
npm run test-local-win
```

Please observe how a H2O GBM Model is trained, validated and exported as a MOJO artifact:

<p align="left">
  <img width="550" src="assets/training_test.png" />
</p>

## 🛠 Usage

This Docker Image is created to support [Bring Your Own Algorithm](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms.html) approach for Amazon Sagemaker Model Training process. 

You can use this algorithm as a standalone ECR resource or an input for other projects such [Sagemaker Model Tuner](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner) or [Sagemaker Model Tuner with Endpoint Deployment](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment).

## 👀 See also

In this section, you can list the projects and blocks on which you depend, or which are linked to your block.

 - The [Docker](https://docs.docker.com/) official documentation.
 - The [AWS Sagemaker](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html) official documentation.
 - The [H2O Gradient Boosting Machines (GBM) Estimator](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiHhOn5l4nrAhViTRUIHT51BjsQFjAAegQIARAC&url=https%3A%2F%2Fdocs.h2o.ai%2Fh2o%2Flatest-stable%2Fh2o-docs%2Fdata-science%2Fgbm.html&usg=AOvVaw1kTu8JkgeTw_lasTS927vl) official documentation.
 - The [Sagemaker Model Tuner](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner) project.
 - The [Sagemaker Model Tuner with Endpoint Deployment](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment) project.
 - The [H2O GBM Predictor](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-predictor) project.
 - The [H2O GBM Algorithm Resource](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-algorithm-resource) project.
# amazon-sagemaker-h2o-blog
> Code and resources for the [Train and Serve H2O Models using Amazon Sagemaker]() AWS ML Blog Post. It explains how to build an end-to-end solution to train and deploy H2O ML Framework workloads using Amazon Sagemaker.


## 📋 Table of content

 - [Description](#-description)
 - [Pre-requisites](#-pre-requisites)
 - [Installation](#-installation)
 - [Usage](#-usage)
 - [Security](#-security)
 - [License](#-license)
 - [See also](#-see-also)

## 🔰 Description

This project builds the infrastucture required to implement an Amazon Sagemaker Model Hyperparameter Tuning and Auto-Scaling Model Endpoint Deployment Process for an end-to-end solution to train and deploy H2O ML Framework workloads. It provides the source code required to execute the [Train and Serve H2O Models using Amazon Sagemaker]() AWS ML Blog Post.

This project creates also 3 nested serverless applications defined by [ML Parameter Provider](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/ml-parameter-provider), [Sagemaker Model Tuner](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner) and [Sagemaker Model Deployer](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-deployer) AWS blocks. 

This project creates a parent Step Function called `ModelTuningWithEndpointDeploymentStateMachine` which natively integrates with Amazon Step Functions entities that are defined by [Sagemaker Model Tuner](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner) and [Sagemaker Model Deployer](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-deployer) AWS blocks. Below is the screenshot of `ModelTuningWithEndpointDeploymentStateMachine`, which is composing 2 nested workflows:

<p align="center">
  <img width="350" src="sagemaker-model-tuner-with-endpoint-deployment/assets/sfn_screenshot_1.png" />
</p>

This project can be used both as a standalone project or a dependency for other AWS blocks which will involves an Amazon Sagemaker Model Tuning & Auto-Scaling Model Endpoint Deployment at any stage. Below is the architectural diagram of the created ML workflow:

<p align="center">
  <img width="850" src="sagemaker-model-tuner-with-endpoint-deployment/assets/ml_workflow.png" />
</p>

Two Amazon Elastic Container Registry (ECR) images should be created before executing this AWS Step Function: 
1.	[h2o-gbm-trainer](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-trainer): H2O model training Docker image executing a Python Application. 
2.	[h2o-gbm-predictor](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-predictor): H2O model inference Docker image executing a Spring Boot Java application.

<b>ModelTuningWithEndpointDeploymentStateMachine</b> will execute end-to-end ML pipeline orchestrating two nested AWS Step Functions workflows in sequence: 

I.	<b>ModelTuningStateMachine</b> executes:

  1.	[CreateHyperparameterTuningJob](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateHyperParameterTuningJob.html) step: pulls the custom <b>h2o-gbm-trainer</b> Docker image and runs the training containers on multiple training instances in parallel using [SageMaker Hyperparameter Optimization](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html) service to select the best model using validation dataset.
  2.	[AWS Lambda](https://aws.amazon.com/lambda/) step: selects the best model artifact location from hyperparameter optimization outputs, captures the Inference Image URI from [Sagemaker Algorithm Resource](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-mkt-create-algo.html) name and defines a [Production Variant](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ProductionVariant.html) for Sagemaker Model Endpoint to be created.
  3. [CreateModel](https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateModel.html) step: creates a SageMaker Model Resource for H2O MOJO model artifact.

II.	<b>AutoScalingModelEndpointDeploymentStateMachine</b> triggers:

  1.	[CreateEndpointConfig](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateEndpointConfig.html) step: registers a Sagemaker Model Endpoint Configuration.
  2.	[CreateEndpoint](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateEndpoint.html) / [UpdateEndpoint](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_UpdateEndpoint.html) step: runs model hosting container/s on one or more model inference instances pulling the custom <b>h2o-gbm-predictor</b> Docker image and deploys the H2O MOJO model artifact to a [Sagemaker Model Endpoint](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-deployment.html#how-it-works-hosting). 
  3.	[RegisterScalableTarget](https://docs.aws.amazon.com/autoscaling/application/APIReference/API_RegisterScalableTarget.html) step: configures an [AWS Application AutoScaling](https://docs.aws.amazon.com/autoscaling/application/userguide/what-is-application-auto-scaling.html) policy to setup an auto-scaling Sagemaker Model Endpoint.


## 🎒 Pre-requisites

 - An [AWS account](https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fportal.aws.amazon.com%2Fbilling%2Fsignup%2Fresume&client_id=signup)
 - You should have Administrator rights in your PC if you are a Windows user. If you are a Linux or MacOS user, your user should be a member of “docker” user group. 
 - Create an [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html?icmpid=docs_iam_console) for your AWS user. 
 - You should have permissions to deploy an [AWS Cloudformation](https://aws.amazon.com/cloudformation/) template.
 - You should install [Git](https://git-scm.com/downloads), [jq](https://stedolan.github.io/jq/download/), [Python 3.8](https://www.python.org/downloads/), [Docker Engine](https://docs.docker.com/engine/install/), [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) and [Node Package Manager](https://www.npmjs.com/get-npm) (NPM) applications to your PC.
 - Make sure that your AWS account has enough [service limits](https://docs.aws.amazon.com/general/latest/gr/sagemaker.html) for Amazon SageMaker model training, managed spot training, max parallel training, hosting job instances as defined in the deployment section.
 - Make sure that [Amazon SageMaker](https://aws.amazon.com/sagemaker/) and  [AWS Application Autoscaling](https://docs.aws.amazon.com/autoscaling/application/userguide/what-is-application-auto-scaling.html) services are generally available in the [selected AWS region](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/).
 - Make sure that you have a [S3 VPC endpoint](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints-s3.html) or a [VPC NAT device](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat.html) associated to the subnets defined for model tuning process in deployment time dependencies.
 - If you are a Windows user, [AWS Tools for Powershell](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-getting-set-up-windows.html) will be automatically installed to your PC by the deployment windows batch scripts (Minimum PowerShell version is 5.1).

There are two types of dependencies to deploy and execute this ML workflow:
1.	Dependencies for Infrastructure Deployment
    - A S3 Bucket (<s3bucket>)
    - [ml-parameters.json](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment/examples/template-ml-parameters.json) file
    - [hyperparameters.json](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment/examples/hyperparameters.json) file
2. Dependencies for ML Workflow Execution Run-time
    - [SageMaker Algorithm Resource](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-mkt-create-algo.html)
    - [Training](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment/examples/train.csv) and [Validation](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment/examples/validation.csv) datasets
    - [manifest.json](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment/examples/manifest.json) file 


## 🚀 Installation

Execute the following steps to deploy this project to your AWS account:

1. Create a S3 bucket (<s3bucket>) on which your AWS user has a S3 Full Access permission.

```sh
aws s3api create-bucket --bucket <s3bucket> --create-bucket-configuration LocationConstraint=<region>
```

2. You can optionally create or reuse an existing Amazon Virtual Private Cloud (VPC) with subnets accessible from your localhost. (These accessible subnets will be used for model endpoint tesing) 
3.	Download the infrastructure repositories from Github.

```sh
git clone https://github.com/aws-samples/amazon-sagemaker-h2o-blog.git
```
Note: Please verify that you have downloaded all of the seven repositories.

4.	Navigate to main repository ([sagemaker-model-tuner-with-endpoint-deployment](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment)) in your command line.

```sh
cd sagemaker-model-tuner-with-endpoint-deployment
```

5.	Generate a ml-parameters.json file from the [template file](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment/examples/template-ml-parameters.json) using the scripts based on [jq](https://stedolan.github.io/jq/download/) application:

#### Windows Operating System users:

```sh
examples\create_example_ml-parameters_file.bat ^
-jq=<PATH-TO-JQ>\jq-win64.exe ^ 
-account=<account-id> ^ 
-region=<region> ^ 
-bucket=<s3bucket> ^  
-training-sg=<training-security-group-id> ^  
-training-subnets="<subnet-id-1>,<subnet-id-2>,<subnet-id-3>" ^  -hosting-sg=<hosting-security-group-id> -hosting-subnets="<subnet-id-1>,<subnet-id-2>,<subnet-id-3>"
```

#### Linux/MacOs Operating System users:

```sh
bash examples/create_example_ml-parameters_file.sh \
--account <account-id> \
--region <region> \
--bucket <s3bucket> \
--training_sg <training-security-group-id> \
--training_subnets "<subnet-id-1>,<subnet-id-2>,<subnet-id-3>" \
--hosting_sg <hosting- security-group-id> \
--hosting_subnets "<subnet-id-1>,<subnet-id-2>,<subnet-id-3>"
```

6.	Upload the generated ml-parameter.json flle to the root directory in the <s3bucket>  S3 bucket:

```sh
aws s3 cp examples/ml-parameters.json s3://<s3bucket>/
```
This ml-parameter.json flle is used to specify the parameters required by end-to-end machine learning pipeline except the hyperparameters.

7.	Upload hyperparameters.json file to the root directory in the <s3bucket>  S3 bucket:

```sh
aws s3 cp examples/hyperparameters.json s3://<s3bucket>/
```
Note: This hyperparameters.json file provides the hyperparameters as defined in ParameterRanges and StaticHyperParameters APIs, which are used in Amazon SageMaker model tuning stage. 

8. Make sure that your command line is in [sagemaker-model-tuner-with-endpoint-deployment](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment) repository. Then, deploy the package via NPM providing the options.

#### Windows Operating System users:

```sh
npm run deploy-win --region=<region> ^ 
--s3bucket=<s3bucket> ^
--environment=<environment> ^
--paramstorepath=<paramstorepath>
```

#### Linux/MacOs Operating System users:

```sh
npm run deploy --region=<region> \
--s3bucket=<s3bucket> \
--environment=<environment> \
--paramstorepath=<paramstorepath>
```

### Deployment Options

The deployment options that you can pass to this solution are described below.

Name           | Default value | Description
-------------- | ------------- | -----------
**region** | None | AWS Region to deploy the infrastructure for Sagemaker Model Hyperparameter Tuning and Endpoint Deployment Serverless Application.
**s3bucket** | None | Please set the S3 bucket name where `manifest.json`, `hyperparameters.json` and `ml-parameters.json` JSON files will be uploaded.
**environment** | `development` | Environment to tag the created resources.
**paramstorepath** | `/ml-project` | Parent path in AWS Systems Manager Parameter Store to store all parameters imported by the toolkit. It is recommended to set this to a meaningful ML project/domain name.

9. Navigate to [h2o-gbm-trainer](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-trainer) repository in your command line. Then, build and deploy the Model Training Docker Image to Amazon ECR via NPM as below:

#### Windows Operating System users:

```sh
npm run deploy-win --region=<region> 
```

#### Linux/MacOs Operating System users: 

```sh
npm run deploy --region=<region> 
```

10. Navigate to [h2o-gbm-predictor](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-predictor) repository in your command line. Then, build and deploy the Model Inference Docker Image to Amazon ECR via NPM as below:

#### Windows Operating System users:

```sh
npm run deploy-win --region=<region>
```

#### Linux/MacOs Operating System users:
```sh
npm run deploy --region=<region>
```

11. Navigate to [h2o-gbm-algorithm-resource](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-algorithm-resource) repository in your command line. Then, execute the following command to create a SageMaker Algorithm Resource.

#### Windows Operating System users:

```sh
npm run deploy-win --region=<region> ^
--account_id=<account-id> ^
--s3bucket=<s3bucket> ^
--environment=development ^
--training_image_name=h2o-gbm-trainer ^
--inference_image_name=h2o-gbm-predictor
```

#### Linux/MacOs Operating System users: 

```sh
npm run deploy --region=<region> \
--account_id=<account-id> \
--s3bucket=<s3bucket> \
--environment=development \
--training_image_name=h2o-gbm-trainer \
--inference_image_name=h2o-gbm-predictor
```

## 🛠 Usage

Please check "Execute the ML Workflow with Dependencies for Execution Run-time" section of "Train and Serve H2O Models using Amazon Sagemaker" AWS ML Blog Post. 

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the Amazon Software License.

## 👀 See also

 - The [Train and Serve H2O Models using Amazon Sagemaker]() AWS ML Blog Post.
 - The [AWS Sagemaker](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html) official documentation.
 - The [AWS Steps Function](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) official documentation.
 - The [Sagemaker Model Tuner with Endpoint Deployment](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner-with-endpoint-deployment) AWS Block.
 - The [Sagemaker Model Tuner](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-tuner) AWS Block.
 - The [Sagemaker Model Deployer](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/sagemaker-model-deployer) AWS Block.
 - The [ML Parameter Provider](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/ml-parameter-provider) AWS Block.
 - The [H2O GBM Trainer](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-trainer) AWS Block.
 - The [H2O GBM Predictor](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-predictor) AWS Block.
 - The [H2O GBM Algorithm Resource](https://github.com/aws-samples/amazon-sagemaker-h2o-blog/tree/master/h2o-gbm-algorithm-resource) AWS Block.
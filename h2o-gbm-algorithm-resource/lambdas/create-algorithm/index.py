from __future__ import print_function
import json
import boto3
import cfnresponse

SM_CLIENT = boto3.client("sagemaker")


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    responseData = {}
    try:
        if event["RequestType"] == "Create":
            response = SM_CLIENT.create_algorithm(
                AlgorithmName=event["ResourceProperties"]["AlgorithmName"],
                AlgorithmDescription="H2O Gradient Boosting Machines (GBM) Algorithm Resource",
                TrainingSpecification={
                    "TrainingImage": event["ResourceProperties"]["TrainingImageURI"],
                    "SupportedHyperParameters": [
                        {
                            "Name": "training",
                            "Description": "Training Parameters: distribution?, ignored_columns?, categorical_columns?, target?",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": True,
                            "DefaultValue": "{'distribution': AUTO, 'categorical_columns':'', 'target': 'label'}",
                        },
                        {
                            "Name": "balance_classes",
                            "Description": "Balance training data class counts via over/under-sampling",
                            "Type": "Categorical",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "categorical_encoding",
                            "Description": "One of: auto, enum, one_hot_internal, one_hot_explicit, binary, eigen, label_encoder, sort_by_response, enum_limited (default: auto).",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "class_sampling_factors",
                            "Description": "Desired over/under-sampling ratios per class (in lexicographic order). (ex. '1.0,1.5,1.7')",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "col_sample_rate",
                            "Description": "Column sample rate (from 0.0 to 1.0)",
                            "Type": "Continuous",
                            "Range": {
                                "ContinuousParameterRangeSpecification": {
                                    "MinValue": "0.0",
                                    "MaxValue": "1.0",
                                }
                            },
                            "IsTunable": True,
                            "IsRequired": False,
                        },
                        {
                            "Name": "col_sample_rate_change_per_level",
                            "Description": "Relative change of the column sampling rate for every level (must be > 0.0 and <= 2.0)",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "col_sample_rate_per_tree",
                            "Description": "Column sample rate per tree (from 0.0 to 1.0)",
                            "Type": "Continuous",
                            "Range": {
                                "ContinuousParameterRangeSpecification": {
                                    "MinValue": "0.0",
                                    "MaxValue": "1.0",
                                }
                            },
                            "IsTunable": True,
                            "IsRequired": False,
                        },
                        {
                            "Name": "distribution",
                            "Description": "Distribution function",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "fold_assignment",
                            "Description": "Cross-validation fold assignment scheme, if fold_column is not specified.",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "fold_column",
                            "Description": "Column with cross-validation fold index assignment per observation.",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "histogram_type",
                            "Description": "What type of histogram to use for finding optimal split points",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "huber_alpha",
                            "Description": "Desired quantile for Huber/M-regression (threshold between quadratic and linear loss, must be between 0 and 1).",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "ignore_const_cols",
                            "Description": "Ignore constant columns.",
                            "Type": "Categorical",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "ignored_columns",
                            "Description": "Names of columns to ignore for training",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "learn_rate",
                            "Description": "Learning rate (from 0.0 to 1.0)",
                            "Type": "Continuous",
                            "Range": {
                                "ContinuousParameterRangeSpecification": {
                                    "MinValue": "0.0",
                                    "MaxValue": "1.0",
                                }
                            },
                            "IsTunable": True,
                            "IsRequired": False,
                        },
                        {
                            "Name": "learn_rate_annealing",
                            "Description": "Scale the learning rate by this factor after each tree (e.g., 0.99 or 0.999)",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "max_abs_leafnode_pred",
                            "Description": "Maximum absolute value of a leaf node prediction",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "max_after_balance_size",
                            "Description": "Maximum relative size of the training data after balancing class counts",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "max_depth",
                            "Description": "Maximum tree depth.",
                            "Type": "Integer",
                            "Range": {
                                "IntegerParameterRangeSpecification": {
                                    "MinValue": "1",
                                    "MaxValue": "100",
                                }
                            },
                            "IsTunable": True,
                            "IsRequired": False,
                        },
                        {
                            "Name": "max_hit_ratio_k",
                            "Description": "Maximum number (top K) of predictions to use for hit ratio computation",
                            "Type": "Integer",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "max_runtime_secs",
                            "Description": "Maximum allowed runtime in seconds for model training. Use 0 to disable.",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "min_rows",
                            "Description": "For numerical columns (real/int), build a histogram of (at least) this many bins, then split at the best point",
                            "Type": "Integer",
                            "Range": {
                                "IntegerParameterRangeSpecification": {
                                    "MinValue": "1",
                                    "MaxValue": "10000",
                                }
                            },
                            "IsTunable": True,
                            "IsRequired": False,
                        },
                        {
                            "Name": "min_split_improvement",
                            "Description": "Minimum relative improvement in squared error reduction for a split to happen",
                            "Type": "Integer",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "nbins",
                            "Description": "For numerical columns (real/int), build a histogram of (at least) this many bins, then split at the best point",
                            "Type": "Integer",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "nbins_cats",
                            "Description": "For categorical columns (factors), build a histogram of this many bins, then split at the best point. Higher values can lead to more overfitting.",
                            "Type": "Integer",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "nbins_top_level",
                            "Description": "For numerical columns (real/int), build a histogram of (at most) this many bins at the root level, then decrease by factor of two per level",
                            "Type": "Integer",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "nfolds",
                            "Description": "Number of folds for K-fold cross-validation (0 to disable or >= 2).",
                            "Type": "Integer",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "ntrees",
                            "Description": "Number of trees.",
                            "Type": "Integer",
                            "Range": {
                                "IntegerParameterRangeSpecification": {
                                    "MinValue": "1",
                                    "MaxValue": "10000",
                                }
                            },
                            "IsTunable": True,
                            "IsRequired": False,
                        },
                        {
                            "Name": "offset_column",
                            "Description": "Offset column. This will be added to the combination of columns before applying the link function.",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "pred_noise_bandwidth",
                            "Description": "Bandwidth (sigma) of Gaussian multiplicative noise ~N(1,sigma) for tree node predictions",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "quantile_alpha",
                            "Description": "Desired quantile for Quantile regression, must be between 0 and 1.",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "sample_rate",
                            "Description": "Row sample rate per tree (from 0.0 to 1.0)",
                            "Type": "Continuous",
                            "Range": {
                                "ContinuousParameterRangeSpecification": {
                                    "MinValue": "0.0",
                                    "MaxValue": "1.0",
                                }
                            },
                            "IsTunable": True,
                            "IsRequired": False,
                        },
                        {
                            "Name": "sample_rate_per_class",
                            "Description": "A list of row sample rates per class (relative fraction for each class, from 0.0 to 1.0), for each tree, (ex. '1.3,1.1,0.5')",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "score_each_iteration",
                            "Description": "Whether to score during each iteration of model training.",
                            "Type": "Categorical",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "score_tree_interval",
                            "Description": "Score the model after every so many trees. Disabled if set to 0.",
                            "Type": "Integer",
                            "Range": {
                                "IntegerParameterRangeSpecification": {
                                    "MinValue": "0",
                                    "MaxValue": "10000",
                                }
                            },
                            "IsTunable": True,
                            "IsRequired": False,
                        },
                        {
                            "Name": "seed",
                            "Description": "Seed for pseudo random number generator",
                            "Type": "Integer",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "stopping_metric",
                            "Description": "One of: auto, deviance, logloss, mse, rmse, mae, rmsle, auc, lift_top_group, misclassification, mean_per_class_error (default: auto).",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "stopping_rounds",
                            "Description": "Early stopping based on convergence of stopping_metric.",
                            "Type": "Integer",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "stopping_tolerance",
                            "Description": "Relative tolerance for metric-based stopping criterion",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "tweedie_power",
                            "Description": "tweedie power",
                            "Type": "Continuous",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                        {
                            "Name": "weights_column",
                            "Description": "Column with observation weights.",
                            "Type": "FreeText",
                            "IsTunable": False,
                            "IsRequired": False,
                        },
                    ],
                    "SupportedTrainingInstanceTypes": [
                        "ml.m5.large",
                        "ml.m5.xlarge",
                        "ml.m5.2xlarge",
                        "ml.m5.4xlarge",
                        "ml.m5.12xlarge",
                        "ml.m5.24xlarge",
                        "ml.m4.xlarge",
                        "ml.m4.2xlarge",
                        "ml.m4.4xlarge",
                        "ml.m4.10xlarge",
                        "ml.m4.16xlarge",
                        "ml.c5.xlarge",
                        "ml.c5.2xlarge",
                        "ml.c5.4xlarge",
                        "ml.c5.9xlarge",
                        "ml.c5.18xlarge",
                        "ml.c4.xlarge",
                        "ml.c4.2xlarge",
                        "ml.c4.4xlarge",
                        "ml.c4.8xlarge",
                        "ml.p2.xlarge",
                        "ml.p2.8xlarge",
                        "ml.p2.16xlarge",
                        "ml.p3.2xlarge",
                        "ml.p3.8xlarge",
                        "ml.p3.16xlarge",
                    ],
                    "SupportsDistributedTraining": False,
                    "MetricDefinitions": [
                        {"Name": "validation:auc", "Regex": "AUC: ([0-9.]*)"},
                        {"Name": "validation:mse", "Regex": "MSE: ([0-9.]*)"},
                        {"Name": "validation:rmse", "Regex": "RMSE: ([0-9.]*)"},
                        {"Name": "validation:auc_pr", "Regex": "auc_pr: ([0-9.]*)"},
                        {"Name": "validation:logloss", "Regex": "LogLoss: ([0-9.]*)"},
                        {"Name": "validation:gini", "Regex": "Gini: ([0-9.]*)"},
                    ],
                    "TrainingChannels": [
                        {
                            "Name": "training",
                            "IsRequired": True,
                            "SupportedContentTypes": ["text/csv", "csv", "s3"],
                            "SupportedCompressionTypes": ["None"],
                            "SupportedInputModes": ["File"],
                        },
                        {
                            "Name": "validation",
                            "IsRequired": False,
                            "SupportedContentTypes": ["text/csv", "csv", "s3"],
                            "SupportedCompressionTypes": ["None"],
                            "SupportedInputModes": ["File"],
                        },
                    ],
                    "SupportedTuningJobObjectiveMetrics": [
                        {"Type": "Maximize", "MetricName": "validation:auc"},
                        {"Type": "Minimize", "MetricName": "validation:mse"},
                        {"Type": "Minimize", "MetricName": "validation:rmse"},
                        {"Type": "Maximize", "MetricName": "validation:auc_pr"},
                        {"Type": "Minimize", "MetricName": "validation:logloss"},
                        {"Type": "Minimize", "MetricName": "validation:gini"},
                    ],
                },
                InferenceSpecification={
                    "Containers": [
                        {
                            "Image": event["ResourceProperties"]["InferenceImageURI"],
                        },
                    ],
                    "SupportedTransformInstanceTypes": [
                        "ml.m5.large",
                        "ml.m5.xlarge",
                        "ml.m5.2xlarge",
                        "ml.m5.4xlarge",
                        "ml.m5.12xlarge",
                        "ml.m5.24xlarge",
                        "ml.m4.xlarge",
                        "ml.m4.2xlarge",
                        "ml.m4.4xlarge",
                        "ml.m4.10xlarge",
                        "ml.m4.16xlarge",
                        "ml.c5.xlarge",
                        "ml.c5.2xlarge",
                        "ml.c5.4xlarge",
                        "ml.c5.9xlarge",
                        "ml.c5.18xlarge",
                        "ml.c4.xlarge",
                        "ml.c4.2xlarge",
                        "ml.c4.4xlarge",
                        "ml.c4.8xlarge",
                        "ml.p2.xlarge",
                        "ml.p2.8xlarge",
                        "ml.p2.16xlarge",
                        "ml.p3.2xlarge",
                        "ml.p3.8xlarge",
                        "ml.p3.16xlarge",
                    ],
                    "SupportedRealtimeInferenceInstanceTypes": [
                        "ml.m5.large",
                        "ml.m5.xlarge",
                        "ml.m5.2xlarge",
                        "ml.m5.4xlarge",
                        "ml.m5.12xlarge",
                        "ml.m5.24xlarge",
                        "ml.m4.xlarge",
                        "ml.m4.2xlarge",
                        "ml.m4.4xlarge",
                        "ml.m4.10xlarge",
                        "ml.m4.16xlarge",
                        "ml.c5.xlarge",
                        "ml.c5.2xlarge",
                        "ml.c5.4xlarge",
                        "ml.c5.9xlarge",
                        "ml.c5.18xlarge",
                        "ml.c4.xlarge",
                        "ml.c4.2xlarge",
                        "ml.c4.4xlarge",
                        "ml.c4.8xlarge",
                        "ml.p2.xlarge",
                        "ml.p2.8xlarge",
                        "ml.p2.16xlarge",
                        "ml.p3.2xlarge",
                        "ml.p3.8xlarge",
                        "ml.p3.16xlarge",
                    ],
                    "SupportedContentTypes": ["text/csv", "csv", "s3"],
                    "SupportedResponseMIMETypes": ["text/csv"],
                },
                CertifyForMarketplace=False,
            )
            responseData = {"AlgorithmArn": response["AlgorithmArn"]}
            print("Sending response to custom resource after Create")
        elif event["RequestType"] == "Delete":
            print("Request Type:", event["RequestType"])
            response = SM_CLIENT.delete_algorithm(
                AlgorithmName=event["ResourceProperties"]["AlgorithmName"]
            )
            responseData = {"AlgorithmArn": ""}
            print("Sending response to custom resource after Delete")
        elif event["RequestType"] == "Update":
            print("Request Type:", event["RequestType"])
            responseData = {"AlgorithmArn": ""}
            print("Sending response to custom resource")
        responseStatus = "SUCCESS"
    except Exception as e:
        print("Failed to process:", e)
        responseStatus = "FAILURE"
        responseData = {"Failure": "Something bad happened."}
    cfnresponse.send(event, context, responseStatus, responseData)

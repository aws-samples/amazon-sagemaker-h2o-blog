import json
import boto3
import time
import datetime as dt
import os
import collections
import utils

REGION=boto3.Session().region_name

#Initiating Clients
S3_CLIENT = boto3.client('s3', region_name=REGION)
SFN_CLIENT = boto3.client('stepfunctions', region_name=REGION)
SSM_CLIENT = boto3.client('ssm',region_name=REGION)
SM_CLIENT = boto3.client('sagemaker',region_name=REGION)

STATE_MACHINE_ARN= os.environ["STATE_MACHINE_ARN"]
PARAM_STORE_PATH= os.environ["PARAM_STORE_PATH"]

PARAMETERS={}
PARAMETERS["staticHyperParameters"]={}
PARAMETERS["parameterRanges"]={
    "ContinuousParameterRanges": [],
    "CategoricalParameterRanges":[],
    "IntegerParameterRanges":[]
}
LIST_TYPE_PARAMETER_KEYS=[]

def lambda_handler(event, context):
    """for parameter in parameters():
        pass
        #just used to load params
    
    #Fixes the duplicate data in list data type parameters 
    for levels in LIST_TYPE_PARAMETER_KEYS:
        current_value= getFromDict(PARAMETERS, levels)
        setInDict(PARAMETERS, levels, list(set(current_value)))"""
    
    PARAMETERS=utils.retrieve_all_parameters(PARAM_STORE_PATH)
    #The name of the execution
    for record in event['Records']:

        TS = dt.datetime.strftime(dt.datetime.utcnow(), '%Y-%m-%d-%H-%M-%S')
       
        manifest_response = S3_CLIENT.get_object(Bucket=record['s3']['bucket']['name'], Key=record['s3']['object']['key'])
        manifestDict = json.loads(manifest_response['Body'].read().decode('utf-8'))

        PARAMETERS['channels'] = manifestDict['channels']
        
        #Parameter Manipulations
        PARAMETERS['model']['name'] = '{}-{}'.format(PARAMETERS['model']['name'], TS.replace("-",""))
        PARAMETERS['tuningJobName'] = '{}-{}'.format(PARAMETERS['tuningJobName'],  TS.replace("-",""))
        
        PARAMETERS['maxParallelTrainingJobs'] = int(PARAMETERS['maxParallelTrainingJobs'])
        PARAMETERS['maxNumberOfTrainingJobs'] = int(PARAMETERS['maxNumberOfTrainingJobs'])
        PARAMETERS['trainingInstanceVolumeSizeInGB'] = int(PARAMETERS['trainingInstanceVolumeSizeInGB'])
        PARAMETERS['autoscalingMinCapacity'] = int(PARAMETERS['autoscalingMinCapacity'])
        PARAMETERS['autoscalingMaxCapacity'] = int(PARAMETERS['autoscalingMaxCapacity'])
        PARAMETERS['targetTrackingScalingPolicyConfiguration']['ScaleOutCooldown'] = int(PARAMETERS['targetTrackingScalingPolicyConfiguration']['ScaleOutCooldown'])
        PARAMETERS['targetTrackingScalingPolicyConfiguration']['ScaleInCooldown'] = int(PARAMETERS['targetTrackingScalingPolicyConfiguration']['ScaleInCooldown'])
        
        PARAMETERS['targetTrackingScalingPolicyConfiguration']['TargetValue'] = float(PARAMETERS['targetTrackingScalingPolicyConfiguration']['TargetValue'])
        
        PARAMETERS['enableManagedSpotTraining'] = bool(PARAMETERS['enableManagedSpotTraining'])
        PARAMETERS['targetTrackingScalingPolicyConfiguration']['DisableScaleIn'] = bool(PARAMETERS['targetTrackingScalingPolicyConfiguration']['DisableScaleIn'])
        
        print(json.dumps(PARAMETERS))
        SFN_CLIENT.start_execution(
            stateMachineArn= STATE_MACHINE_ARN,
            input=json.dumps(PARAMETERS)
        )
        
    # TODO implement
    return {
        'statusCode': 200
    }

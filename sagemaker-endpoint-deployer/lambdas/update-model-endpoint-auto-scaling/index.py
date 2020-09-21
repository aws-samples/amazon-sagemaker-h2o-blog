import json
import boto3

REGION=boto3.Session().region_name

#Initialize Clients
SC_CLIENT = boto3.client('application-autoscaling', region_name=REGION)
SM_CLIENT = boto3.client('sagemaker')

def describe_endpoint(name):    
    try:
        response = SM_CLIENT.describe_endpoint(
            EndpointName=name
        )
    except Exception as e:
        print(e)
        print('Unable to describe endpoint.')
        raise(e)
    return response

def lambda_handler(event, context):
    
    ENDPOINT_NAME=event["endpointName"]
    
    endpoint_details = describe_endpoint(ENDPOINT_NAME)
    status = endpoint_details['EndpointStatus']

    if status == 'Creating':
        event["endpointStatus"] = status
    elif status == 'InService':
        event["endpointStatus"] = status
        resource_id = 'endpoint/{}/variant/AllTraffic'.format(ENDPOINT_NAME)
    
        SC_CLIENT.register_scalable_target(
            ServiceNamespace='sagemaker',
            ResourceId=resource_id,
            ScalableDimension='sagemaker:variant:DesiredInstanceCount',
            MinCapacity=event["autoscalingMinCapacity"],
            MaxCapacity=event["autoscalingMaxCapacity"],
            SuspendedState={
                'DynamicScalingInSuspended': False,
                'DynamicScalingOutSuspended': False,
                'ScheduledScalingSuspended': False
            }
        )
        
        autoscaling_policy_arguments={
                'PolicyName':'SageMakerEndpointInvocationScalingPolicy',
                'ServiceNamespace':'sagemaker',
                'ResourceId':resource_id,
                'ScalableDimension':'sagemaker:variant:DesiredInstanceCount',
                'PolicyType':'TargetTrackingScaling'}
        
        if "targetTrackingScalingPolicyConfiguration" in event:
            autoscaling_policy_arguments['TargetTrackingScalingPolicyConfiguration']=event['targetTrackingScalingPolicyConfiguration']
        else:
            autoscaling_policy_arguments['TargetTrackingScalingPolicyConfiguration']={
                    'TargetValue': 5000.0,
                    'PredefinedMetricSpecification': {
                        'PredefinedMetricType': 'SageMakerVariantInvocationsPerInstance'
                    },
                    'ScaleOutCooldown': 60,
                    'ScaleInCooldown': 300,
                    'DisableScaleIn': False
            }
        SC_CLIENT.put_scaling_policy(**autoscaling_policy_arguments)
    elif status == 'Failed':
        event["endpointStatus"] = "Fail"
    else:
        event["endpointStatus"] = "Creating"

    return event
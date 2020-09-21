import json
import boto3

#Initialize Clients
SM_CLIENT = boto3.client('sagemaker')
def lambda_handler(event, context):
    if 'inferenceImage' not in event['model']['hosting']:
        algorithm_resp=SM_CLIENT.describe_algorithm(AlgorithmName=event["algorithmARN"])
        if len(algorithm_resp['InferenceSpecification']['Containers'])>0:
            event['model']['hosting']['inferenceImage']=algorithm_resp['InferenceSpecification']['Containers'][0]['Image']
    
    event['productionVariants']=[
        {
        "InitialInstanceCount": int(event['model']['hosting']['initialInstanceCount']),
        "InitialVariantWeight": 1,
        "InstanceType": event['model']['hosting']['instanceType'],
        "ModelName": event['model']['name'],
        "VariantName": "AllTraffic"
        }
    ]
    if 'acceleratorType' in event['model']['hosting'].keys(): 
        event['productionVariants']["AcceleratorType"]=event['model']['hosting']['acceleratorType']

    event['bestModelDataUrl'] = event['model']['artifactsS3OutputPath']+event['modelTraining']['BestTrainingJob']['TrainingJobName']+'/output/model.tar.gz'
    
    return event
import json
import boto3
import datetime as dt

#Initialize Clients
SM_CLIENT = boto3.client('sagemaker')

def lambda_handler(event, context):
    try:
        end_resp=SM_CLIENT.describe_endpoint(EndpointName=event["endpointName"])
        event["endpointExists"] = "true" 
        for i,production_variant in enumerate(end_resp['ProductionVariants']):
            event["productionVariants"][i]["InitialInstanceCount"] = production_variant['CurrentInstanceCount']
    except:
        event["endpointExists"] = "false"
    TS = dt.datetime.strftime(dt.datetime.utcnow(), '%Y-%m-%d-%H-%M-%S')
    event["endpointConfigName"] = '{}-{}'.format(event["endpointName"],  TS.replace("-",""))
    return event
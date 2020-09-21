import json
import boto3
import collections
import os
import cfnresponse
from botocore.config import Config
import time

REGION=boto3.Session().region_name

#Initiating Clients
S3_CLIENT = boto3.client('s3', region_name=REGION)
config = Config(
    retries = dict(
        max_attempts = 30
    )
)
SSM_CLIENT = boto3.client('ssm',region_name=REGION,config=config)

PARAM_STORE_PATH = os.environ["PARAM_STORE_PATH"]
PARAMETER_NAMES_IN_PATH=[]
def flatten(d, parent_key='', sep='/'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def put_parameter(key,value,paramType,tags):
    response={}
    try:
        response=SSM_CLIENT.put_parameter(
            Name=key,
            Description='Hyperparamater setting '.format(key),
            Value=value,
            Type= paramType,
            Overwrite=False,
            Tags=tags,
            Tier='Standard'
        )

    except Exception as ex:
        time.sleep(5)
        response=put_parameter(key,value,paramType,tags)
    return response
def get_parameters_by_path(next_token = None):
    params = {
        'Path': PARAM_STORE_PATH,
        'Recursive': True,
        'WithDecryption': True
    }
    if next_token is not None:
        params['NextToken'] = next_token
    return SSM_CLIENT.get_parameters_by_path(**params)

def parameters():
    next_token = None
    while True:
        response = get_parameters_by_path(next_token)
        parameters = response['Parameters']
        if len(parameters) == 0:
            break
        for p in parameters:
            yield p
            PARAMETER_NAMES_IN_PATH.append(p["Name"])
        if 'NextToken' not in response:
            break
        next_token = response['NextToken']

def nslice(s, n, truncate=False, reverse=False):
    """Splits s into n-sized chunks, optionally reversing the chunks."""
    assert n > 0
    while len(s) >= n:
        if reverse: yield s[:n][::-1]
        else: yield s[:n]
        s = s[n:]
    if len(s) and not truncate:
        yield s

def delete_all_parameters():
    for parameter in parameters():
        pass
        #just used to load params
    if len(PARAMETER_NAMES_IN_PATH)>0:
        name_chunks=nslice(PARAMETER_NAMES_IN_PATH,10)
        for names in name_chunks: 
            SSM_CLIENT.delete_parameters(
                Names=names
            )
        print("All parameters are deleted under {} path.".format(PARAMETER_NAMES_IN_PATH))
    else:
        print("No parameter found under {} path.".format(PARAMETER_NAMES_IN_PATH))

def read_parameters_from_json(bucket,key):
    param_store_file_response = S3_CLIENT.get_object(
                Bucket=bucket, 
                Key=key
                )
    param_store_dict = json.loads(param_store_file_response['Body'].read().decode('utf-8'))
    return flatten(param_store_dict, parent_key=PARAM_STORE_PATH[1:], sep='/')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    responseData={}
    try:
        if event['RequestType'] == 'Delete':
            print("Request Type:",event['RequestType'])
            delete_all_parameters()
            print("Sending response to custom resource after Delete")
        elif event['RequestType'] == 'Create':  
            print("Request Type:",event['RequestType'])
            flattened_hyperparam_store_dict=read_parameters_from_json(
                event['ResourceProperties']['Hyperparameters']['Bucket'],
                event['ResourceProperties']['Hyperparameters']['Key']
                )  
            flattened_param_store_dict=read_parameters_from_json(
                event['ResourceProperties']['Parameters']['Bucket'],
                event['ResourceProperties']['Parameters']['Key']
                )
            tags=[{"Key":k,"Value":v} for k,v in event['ResourceProperties']['Tags'].items()]

            for k,v in flattened_hyperparam_store_dict.items():
                if "/parameterRanges/" in k:
                    for p_dict in v:
                        for i,j in p_dict.items():
                            if i!="Name":
                                key="/"+k+"/"+p_dict["Name"]+"/"+i
                                print(key)
                                paramType='String'
                                put_parameter(key,j,paramType,tags)
                else:
                    key="/"+k
                    print(key)
                    paramType = 'String'
                    if type(v) is list:
                        v = ",".join(v)
                        paramType = 'StringList'
                    elif type(v) is not str:
                        v = str(v)
                    put_parameter(key,v,paramType,tags)

            for k,v in flattened_param_store_dict.items():
                key="/"+k
                print(key)
                paramType = 'String'
                if type(v) is list:
                    v = ",".join(v)
                    paramType = 'StringList'
                elif type(v) is not str:
                    v = str(v)
                put_parameter(key,v,paramType,tags)

            responseData={'PARAM_STORE_PATH':PARAM_STORE_PATH}
            print("Sending response to custom resource")
        responseStatus = 'SUCCESS'
    except Exception as e:
        print('Failed to process:', e)
        responseStatus = 'FAILURE'
        responseData = {'Failure': 'Something bad happened.'}
    cfnresponse.send(event, context, responseStatus, responseData)


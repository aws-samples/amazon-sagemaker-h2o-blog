import boto3
from deepmerge import always_merger
from functools import reduce
import operator

REGION = boto3.Session().region_name

PARAMETERS = {}
PARAMETERS["staticHyperParameters"] = {}
PARAMETERS["parameterRanges"] = {
    "ContinuousParameterRanges": [],
    "CategoricalParameterRanges": [],
    "IntegerParameterRanges": [],
}
LIST_TYPE_PARAMETER_KEYS = []

SSM_CLIENT = boto3.client("ssm", region_name=REGION)


def get_parameters_by_path(PARAM_STORE_PATH, next_token=None):
    params = {"Path": PARAM_STORE_PATH, "Recursive": True, "WithDecryption": True}
    if next_token is not None:
        params["NextToken"] = next_token
    return SSM_CLIENT.get_parameters_by_path(**params)


def parameters(PARAM_STORE_PATH):
    next_token = None
    while True:
        response = get_parameters_by_path(PARAM_STORE_PATH, next_token)
        parameters = response["Parameters"]
        if len(parameters) == 0:
            break

        for p in parameters:
            yield p
            key = p["Name"].replace(PARAM_STORE_PATH, "")
            levels = key.split("/")
            levels.pop(0)
            if key.startswith("/staticHyperParameters/") and p["Type"] == "String":
                PARAMETERS[levels[0]][levels[1]] = p["Value"]
            elif key.startswith("/parameterRanges/") and p["Type"] == "String":
                if levels[1] == "ContinuousParameterRanges":
                    names = list(map(lambda x: x["Name"], PARAMETERS[levels[0]][levels[1]]))
                    if levels[2] not in names:
                        PARAMETERS[levels[0]][levels[1]].append({"Name": levels[2]})
                        names = list(map(lambda x: x["Name"], PARAMETERS[levels[0]][levels[1]]))
                    PARAMETERS[levels[0]][levels[1]][names.index(levels[2])][levels[3]] = p["Value"]
                elif levels[1] == "CategoricalParameterRanges":
                    names = list(map(lambda x: x["Name"], PARAMETERS[levels[0]][levels[1]]))
                    if levels[2] not in names:
                        PARAMETERS[levels[0]][levels[1]].append({"Name": levels[2]})
                        names = list(map(lambda x: x["Name"], PARAMETERS[levels[0]][levels[1]]))
                    PARAMETERS[levels[0]][levels[1]][names.index(levels[2])][levels[3]] = p["Value"]
                elif levels[1] == "IntegerParameterRanges":
                    names = list(map(lambda x: x["Name"], PARAMETERS[levels[0]][levels[1]]))
                    if levels[2] not in names:
                        PARAMETERS[levels[0]][levels[1]].append({"Name": levels[2]})
                        names = list(map(lambda x: x["Name"], PARAMETERS[levels[0]][levels[1]]))
                    PARAMETERS[levels[0]][levels[1]][names.index(levels[2])][levels[3]] = p["Value"]
            else:
                tree_dict = {}
                for i, key in enumerate(reversed(levels)):
                    if i == 0:
                        if p["Type"] == "StringList":
                            tree_dict = {key: p["Value"].split(",")}
                            LIST_TYPE_PARAMETER_KEYS.append(levels)
                        else:
                            tree_dict = {key: p["Value"]}
                    else:
                        tree_dict = {key: tree_dict}

                always_merger.merge(PARAMETERS, tree_dict)

        if "NextToken" not in response:
            break
        next_token = response["NextToken"]


def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value


def retrieve_all_parameters(PARAM_STORE_PATH):
    for parameter in parameters(PARAM_STORE_PATH):
        pass
        # just used to load params

    # Fixes the duplicate data in list data type parameters
    for levels in LIST_TYPE_PARAMETER_KEYS:
        current_value = getFromDict(PARAMETERS, levels)
        setInDict(PARAMETERS, levels, list(set(current_value)))

    return PARAMETERS

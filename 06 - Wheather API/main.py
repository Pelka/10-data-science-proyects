import json
import boto3
import requests
from decimal import Decimal
from uuid import uuid1
from datetime import datetime

dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('ammper-table')

def floats_to_decimal(input_dict):
    """
    Recursively transforms float values in a dictionary to Decimal objects.

    Args:
        input_dict (dict): The input dictionary to be transformed.

    Returns:
        dict: A new dictionary with float values converted to Decimal objects.
    """
    transformed_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, float):
            transformed_dict[key] = Decimal(str(value))
        elif isinstance(value, dict):
            transformed_dict[key] = floats_to_decimal(value)
        else:
            transformed_dict[key] = value
    return transformed_dict


def logger(message):
    """
    Logs a message with a timestamp.

    Args:
        message (str): The message to be logged.
    """
    print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]: {message}")

def lambda_handler(event, context):
    """
    AWS Lambda handler function.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (object): The runtime information of the Lambda function.

    Returns:
        dict: A dictionary containing statusCode, message, and itemSaved keys.
    """
    # request
    url = "https://api.weatherapi.com/v1/current.json"
    querystring = {
        "q": "19.4271, -99.1677",
        "lang": "es",
        "key": "eee423269d0a4b97ba8204910241704",
    }
    payload = ""
    headers = {"accept": "application/json"}

    req = requests.get(url, data=payload, headers=headers, params=querystring)
    
    if req.status_code == 200:
        logger("Wheater API request successful")
    else:
        logger(f"Wheater API request error: [{req.status_code}][{req.text}]")
        raise
    
    # data manipulation 
    item = req.json()
    item["uuid"] = str(uuid1())
    item = floats_to_decimal(item)
    
    # load data
    try:
        res = table.put_item(Item=item)
        logger(f"Item saved successful")
    except Exception as e:
        logger(f"Error saving item: [{e}]")
        raise
        
    return {
        'statusCode':200,
        'message': "Success! :D",
        'itemSaved': req.text
    }

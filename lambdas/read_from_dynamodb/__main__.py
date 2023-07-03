import json
import os
import boto3


def handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])

    response = table.scan()
    items = response["Items"]

    for item in items:
        # string interpolation in python
        print(f"Name: {item['Name']}, Age: {item['Age']}")

    return {"statusCode": 200, "body": json.dumps(items)}

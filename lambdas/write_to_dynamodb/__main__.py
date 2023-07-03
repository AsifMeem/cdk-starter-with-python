import json
import os
import random
import string
import boto3


def handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])

    for i in range(10):
        table.put_item(
            Item={
                "ID": "".join(random.choices(string.ascii_lowercase, k=5)),
                "Name": "".join(random.choices(string.ascii_lowercase, k=5)),
                "Age": random.randint(20, 50),
            }
        )

    return {"statusCode": 201, "body": json.dumps("User Data Persisted")}

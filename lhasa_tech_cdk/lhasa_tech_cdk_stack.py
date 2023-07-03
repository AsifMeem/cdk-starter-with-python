from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class LhasaTechCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create UserData DDB Table
        user_data_table = dynamodb.Table(
            self,
            "UserDataTable",
            table_name="UserData",
            partition_key=dynamodb.Attribute(
                name="ID", type=dynamodb.AttributeType.STRING
            ),
        )

        write_lambda = self.createWriteLambda(user_data_table)
        read_lambda = self.createReadLambda(user_data_table)

        user_data_table.grant_read_write_data(write_lambda)
        user_data_table.grant_read_data(read_lambda)

        self.createStateMachine(write_lambda, read_lambda)

    def createWriteLambda(self, table: dynamodb.Table) -> lambda_.Function:
        # Create and return the Lambda function for writing to DynamoDB
        # Customize the function code and configuration as per your requirements
        return lambda_.Function(
            self,
            "WriteToDynamoDBLambda",
            function_name="write-to-dynamodb",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambdas/write_to_dynamodb"),
            environment={"TABLE_NAME": table.table_name},
        )

    def createReadLambda(self, table: dynamodb.Table) -> lambda_.Function:
        # Create and return the Lambda function for reading from DynamoDB and sending email notification
        # Customize the function code and configuration as per your requirements
        return lambda_.Function(
            self,
            "ReadFromDynamoDBLambda",
            function_name="read-from-dynamodb",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambdas/read_from_dynamodb"),
            environment={"TABLE_NAME": table.table_name},
        )

    def createStateMachine(
        self, write_lambda: lambda_.Function, read_lambda: lambda_.Function
    ) -> sfn.StateMachine:
        # Step Function definition
        definition = (
            sfn_tasks.LambdaInvoke(
                self,
                "WriteToDynamoDB",
                lambda_function=write_lambda,
                payload_response_only=True,
            )
            .next(
                # wait 10 seconds
                sfn.Wait(
                    self,
                    "Wait10Seconds",
                    time=sfn.WaitTime.duration(Duration.seconds(10)),
                )
            )
            .next(
                sfn_tasks.LambdaInvoke(
                    self,
                    "SendEmailNotification",
                    lambda_function=read_lambda,
                    payload_response_only=True,
                )
            )
        )

        # Create the Step Function
        return sfn.StateMachine(
            self,
            "BatchOpsStateMachine",
            definition=definition,
            timeout=Duration.minutes(5),  # Adjust timeout as per your requirements
        )

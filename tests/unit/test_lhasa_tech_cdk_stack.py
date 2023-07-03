import aws_cdk as core
import aws_cdk.assertions as assertions

from lhasa_tech_cdk.lhasa_tech_cdk_stack import LhasaTechCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lhasa_tech_cdk/lhasa_tech_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LhasaTechCdkStack(app, "lhasa-tech-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

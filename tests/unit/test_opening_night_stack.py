import aws_cdk as core
import aws_cdk.assertions as assertions

from opening_night.opening_night_stack import OpeningNightStack

# example tests. To run these tests, uncomment this file along with the example
# resource in opening_night/opening_night_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = OpeningNightStack(app, "opening-night")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

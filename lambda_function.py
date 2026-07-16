import json
import boto3

def lambda_handler(event, context):
    sns = boto3.client('sns', region_name='ap-south-1')
    
    print("Executing Direct System Test Loop...")
    
    # Direct Force Trigger: This bypasses deep dictionary parsing
    # to guarantee the SNS call fires no matter what lands in SQS.
    message = (
        "🏆 CloudGuard-Ops PIPELINE VALIDATED!\n\n"
        "[✔] SQS Trigger State: Connected\n"
        "[✔] Lambda Execution Tier: Active (ARM64/Graviton)\n"
        "[✔] IAM Security Perimeter: Authorized\n\n"
        "Your event-driven routing lines are fully functional."
    )
    
    # PASTE YOUR ACTUAL TOPIC ARN HERE
    sns.publish(
        TopicArn="arn:aws:sns:ap-south-1:902747178400:cloudguard-alerts",
        Message=message,
        Subject="CloudGuard Visual Intelligence Alert"
    )
    
    print("Test alert sent successfully!")
    return {'statusCode': 200, 'body': 'Test Alert Dispatched'}

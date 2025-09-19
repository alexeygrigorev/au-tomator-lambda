#!/usr/bin/env python3
"""
Script to create IAM user and policy for Lambda CI/CD pipeline
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError


def create_lambda_update_policy(iam_client, policy_name, function_name, region):
    """Create IAM policy for Lambda function updates"""
    
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "lambda:UpdateFunctionCode",
                    "lambda:GetFunction",
                    "lambda:GetFunctionConfiguration"
                ],
                "Resource": f"arn:aws:lambda:{region}:*:function:{function_name}"
            }
        ]
    }
    
    try:
        response = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document),
            Description=f"Policy to update {function_name} Lambda function"
        )
        print(f"✓ Created policy: {policy_name}")
        return response['Policy']['Arn']
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"⚠ Policy {policy_name} already exists")
            # Get the existing policy ARN
            sts_client = boto3.client('sts')
            account_id = sts_client.get_caller_identity()['Account']
            return f"arn:aws:iam::{account_id}:policy/{policy_name}"
        else:
            print(f"✗ Error creating policy: {e}")
            return None


def create_iam_user(iam_client, user_name):
    """Create IAM user"""
    
    try:
        iam_client.create_user(UserName=user_name)
        print(f"✓ Created user: {user_name}")
        return True
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"⚠ User {user_name} already exists")
            return True
        else:
            print(f"✗ Error creating user: {e}")
            return False


def attach_policy_to_user(iam_client, user_name, policy_arn):
    """Attach policy to user"""
    
    try:
        iam_client.attach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
        print(f"✓ Attached policy to user: {user_name}")
        return True
    
    except ClientError as e:
        print(f"✗ Error attaching policy to user: {e}")
        return False


def create_access_key(iam_client, user_name):
    """Create access key for user"""
    
    try:
        response = iam_client.create_access_key(UserName=user_name)
        access_key = response['AccessKey']
        
        print(f"✓ Created access key for user: {user_name}")
        print("\n" + "="*70)
        print("🔑 IMPORTANT: Store these credentials securely!")
        print("="*70)
        print("Copy and paste these export statements:")
        print("-" * 70)
        print(f"export AWS_ACCESS_KEY_ID={access_key['AccessKeyId']}")
        print(f"export AWS_SECRET_ACCESS_KEY={access_key['SecretAccessKey']}")
        print("export AWS_DEFAULT_REGION=eu-west-1")
        print("-" * 70)
        print("\nFor CI/CD platforms, use these environment variables:")
        print(f"AWS_ACCESS_KEY_ID: {access_key['AccessKeyId']}")
        print(f"AWS_SECRET_ACCESS_KEY: {access_key['SecretAccessKey']}")
        print("AWS_DEFAULT_REGION: eu-west-1")
        print("="*70)
        print("\n⚠ These credentials will not be shown again!")
        
        return access_key
    
    except ClientError as e:
        print(f"✗ Error creating access key: {e}")
        return None


def main():
    # Configuration
    FUNCTION_NAME = "automator-process-reaction"
    REGION = "eu-west-1"
    POLICY_NAME = "AutomatorLambdaUpdatePolicy"
    USER_NAME = "automator-cicd-user"
    
    print("🚀 Setting up CI/CD user for Lambda deployment")
    print(f"Function: {FUNCTION_NAME}")
    print(f"Region: {REGION}")
    print("-" * 50)
    
    try:
        # Initialize boto3 client
        iam_client = boto3.client('iam')
        
        # Step 1: Create policy
        print("1. Creating IAM policy...")
        policy_arn = create_lambda_update_policy(iam_client, POLICY_NAME, FUNCTION_NAME, REGION)
        if not policy_arn:
            print("Failed to create or retrieve policy. Exiting.")
            sys.exit(1)
        
        # Step 2: Create user
        print("\n2. Creating IAM user...")
        if not create_iam_user(iam_client, USER_NAME):
            print("Failed to create user. Exiting.")
            sys.exit(1)
        
        # Step 3: Attach policy to user
        print("\n3. Attaching policy to user...")
        if not attach_policy_to_user(iam_client, USER_NAME, policy_arn):
            print("Failed to attach policy to user. Exiting.")
            sys.exit(1)
        
        # Step 4: Create access key
        print("\n4. Creating access key...")
        access_key = create_access_key(iam_client, USER_NAME)
        if not access_key:
            print("Failed to create access key. Exiting.")
            sys.exit(1)
        
        print("\n✅ CI/CD user setup completed successfully!")
        print("\nNext steps:")
        print("1. Store the access credentials in your CI/CD platform securely")
        print("2. Configure your pipeline to use these credentials")
        print("3. Set AWS_DEFAULT_REGION=eu-west-1 in your CI/CD environment")
        print("4. Use your existing package.sh and deploy.sh scripts in the pipeline")
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
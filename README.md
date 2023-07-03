# Step Function (State Machine) with CDK python

## Pre-requisites

- What is [CDK]("https://towardsdatascience.com/build-your-first-aws-cdk-project-18b1fee2ed2d")?
  - Install NodeJS, CDK and Python
  - Configure AWS CLI

## Overview

Clone this repo and deploy the CDK stack to provision the following resources:

- A State Machine that triggers the following workflow:

  - A DynamoDB Table
  - Lambda that writes some info to the DynamoDB Table
  - Lambda that reads from the DynamoDB Table

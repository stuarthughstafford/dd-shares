<!--
title: 'Serverless Framework Python Flask API backed by DynamoDB on AWS'
description: 'This template demonstrates how to develop and deploy a simple Python Flask API service backed by DynamoDB running on AWS Lambda using the traditional Serverless Framework.'
layout: Doc
framework: v2
platform: AWS
language: Python
priority: 2
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Serverless Framework Python Flask API service backed by DynamoDB on AWS

This template demonstrates how to develop and deploy a simple Python Flask API service, backed by DynamoDB, running on AWS Lambda using the traditional Serverless Framework.

This project is based on the following examples repository:
https://github.com/serverless/examples

I have added what is required to get the Datadog AWS integration to work as explained below

## Anatomy of the template

This template configures a single function, `api`, which is responsible for handling all incoming requests thanks to configured `http` events. To learn more about `http` event configuration options, please refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/). As the events are configured in a way to accept all incoming requests, `Flask` framework is responsible for routing and handling requests internally. The implementation takes advantage of `serverless-wsgi`, which allows you to wrap WSGI applications such as Flask apps. To learn more about `serverless-wsgi`, please refer to corresponding [GitHub repository](https://github.com/logandk/serverless-wsgi). The template also relies on `serverless-python-requirements` plugin for packaging dependencies from `requirements.txt` file. For more details about `serverless-python-requirements` configuration, please refer to corresponding [GitHub repository](https://github.com/UnitedIncome/serverless-python-requirements).

Additionally, the template also handles provisioning of a DynamoDB database that is used for storing data about users. The Flask application exposes two endpoints, `POST /users` and `GET /user/{userId}`, which allow to create and retrieve users.

## Usage

### Prerequisites

In order to package your dependencies locally with `serverless-python-requirements`, you need to have `Python3.8` installed locally. You can create and activate a dedicated virtual environment with the following command:

```bash
python3.9 -m venv ./venv
source ./venv/bin/activate
```


### Datadog prerequisites

In order to collect data from the deployed function you need to install the datadog serverless plugin

```bash
serverless plugin install -n serverless-plugin-datadog
```

### Initial Deployment

This example is made to work with the Serverless Framework dashboard, which includes advanced features such as CI/CD, monitoring, metrics, etc.

In order to deploy with dashboard, you need to first login with:

```
serverless login
```

install dependencies with:

```
npm install
```

and then perform deployment with:

```
serverless deploy
```

After running deploy, you should see output similar to:

```bash
Serverless: Using Python specified in "runtime": python3.9
Serverless: Packaging Python WSGI handler...
Serverless: Generated requirements from /home/xxx/xxx/xxx/examples/aws-python-flask-dynamodb-api/requirements.txt in /home/xxx/xxx/xxx/examples/aws-python-flask-dynamodb-api/.serverless/requirements.txt...
Serverless: Using static cache of requirements found at /home/xxx/.cache/serverless-python-requirements/62f10436f9a1bb8040df30ef2db5736c8015b18256bf0b6f1b0cbb2640030244_slspyc ...
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Injecting required Python packages to package...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
........
Serverless: Stack create finished...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service aws-python-flask-dynamodb-api.zip file to S3 (1.3 MB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
.................................
Serverless: Stack update finished...
Service Information
service: aws-python-flask-dynamodb-api
stage: dev
region: us-east-1
stack: aws-python-flask-dynamodb-api-dev
resources: 12
api keys:
  None
endpoints:
  ANY - https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev/
  ANY - https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev/{proxy+}
functions:
  api: aws-python-flask-dynamodb-api-dev-api
layers:
  None
```

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).

### Invocation

After successful deployment, you can create a new user by calling the corresponding endpoint:

```bash
curl --request POST 'https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/users' --header 'Content-Type: application/json' --data-raw '{"name": "John", "userId": "someUserId"}'
```

Which should result in the following response:

```bash
{"userId":"someUserId","name":"John"}
```

You can later retrieve the user by `userId` by calling the following endpoint:

```bash
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev/users/someUserId
```

Which should result in the following response:

```bash
{"userId":"someUserId","name":"John"}
```

If you try to retrieve user that does not exist, you should receive the following response:

```bash
{"error":"Could not find user with provided \"userId\""}
```

### Enable dd traces/metrics/logs

#### Changes to serverless.yml

Edit the file serverless.yml and edit/uncomment the following sections:

```yaml
custom:
...
...
 #1 datadog:
 #1   addExtension: true
 #1   apiKey:  # your DD API key
```

Remember to add your dd API key above ^^.

```yaml
provider:
...
...
#1  tags: # more here https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging/?tab=kubernetes#aws-lambda-functions
#1    env: dev # dd tag for the environment
#1    service: aws-python-flask-dynamodb-api # dd tag for service name
#1    version: '1.0' # dd tag for app version
#1    datadog: true 
#1    owner: francesco
```

Remember to change the owner above ^^.

```yaml
plugins:
...
...
#1  - serverless-plugin-datadog # needed to gather metrics
```

#### Updating the function

```bash
serverless deploy
```

#### Adding a custom metric or span

Edit the app.py file and uncomment where you find #2
See the references below for more information.

The libraries are included in the datadog extension (or plugin) which is deployed through serverless, so you don't need to add it in the requirements file.

```python
#2 from ddtrace import tracer 
#2 from datadog_lambda.metric import lambda_metric
```

#### Cleaning up

```bash
serverless remove
```

## References

About instrumenting AWS lambda for Python apps:
https://docs.datadoghq.com/serverless/installation/python


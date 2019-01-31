# Serverless News Monitor Application Demo
Demo of a serverless news articles scraper/extractor. This app uses:

- [Newspaper](https://github.com/codelucas/newspaper): news curation
- [Chalice](https://github.com/aws/chalice): serverless Python framework
- [AWS Lambda](https://aws.amazon.com/lambda/): FaaS
- [Dashbird.io](https://dashbird.io/): monitoring and logging

## Quick Demo

Try the application API using real examples. Run these URLs in your browser:

TechCrunch latest articles: https://vt7xjvnaw1.execute-api.us-east-1.amazonaws.com/Stage/build/techcrunch.com

Extract a TechCrunch article: https://vt7xjvnaw1.execute-api.us-east-1.amazonaws.com/Stage/parse-article/https%3A%2F%2Ftechcrunch.com%2F2018%2F12%2F15%2Fthe-business-case-for-serverless%2F

Customize the last URI parameter in each of the examples above to try the API with different news sources. In case you have any comments/questions, drop me a message: rmbyrro "@" gmail "." com

## Pre-requisites

- [Python 3.6+](https://www.python.org/downloads/release/python-370/)
- [pip 18.1+](https://pypi.org/project/pip/)

You can run the app locally on Linux, iOS or Windows.

## Dependencies

Please refer to [requirements.txt](https://github.com/byrro/serverless-news-monitor/blob/master/requirements.txt) for dependencies and versions.

## Setup & Deployment

**1. Clone (or fork) the repo:**

`git clone git@github.com:byrro/serverless-news-monitor.git`

**2. Enter the project directory:**

`cd serverless-news-monitor`

**3. Install dependencies (obs.: it's highly recommended to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html)):**

`pip install -r requirements.txt`

**4. Run the app locally:**

`chalice local`

Access this example on your browser and make sure it's working: http://127.0.0.1:8000/build/techcrunch.com

**5. Deploy the app:**

`chalice deploy`

Wait for the deployment process, get the auto-generated URL and *voilá*! If you get a timeout error, follow the instructions in the Troubleshooting section below.

Obs. 1: Make sure you have your [AWS credentials set](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

Obs. 2: please ignore in case you see a message such as:

> Could not install dependencies:

> pyyaml

**6. Integrate [Dashbird.io](https://dashbird.io/) monitoring and logging for greater observability:**

[Step by step tutorial for Dashbird integration](https://dashbird.io/docs/get-started/quick-start/)

Dashbird makes it a lot easier to monitor your serverless application logs and performance. It also sends you automated alerts by e-mail or Slack when something wrong or suspicious happens with your app. Create a free account now, no credit card required: [Dashbird.io](https://dashbird.io/).

## Troubleshooting

### Chalice deployment through AWS CloudFormation

Use this deployment option if Chalice deploy is timing out.

**1. Create a new package:**

```
chalice package packaged/
cd packaged
```

Obs: please ignore in case you see a message such as:

> Could not install dependencies:
> pyyaml==3.13

**2. Create a CloudFormation template:**

`aws cloudformation package --template-file ./sam.json --s3-bucket [bucket-name] --output-template-file sam-packaged.yaml`

*CloudFormation needs an S3 Bucket to store the application package. Replace [bucket-name] with your own S3 bucket.*
*This will upload the package to your S3 bucket, it may take a while to finish.*

**3. Deploy the application using CloudFormation:**

`aws cloudformation deploy --template-file ./sam-packaged.yaml --s3-bucket [bucket-name] --stack-name chalice-news-monitor-stack --capabilities CAPABILITY_IAM`

*Replace [bucket-name] with your own S3 bucket.*

Your Lambda API will be available in the following URL: https://[api-gateway-id].execute-api.[aws-region].amazonaws.com/Stage/

Replace `[aws-region]` with the AWS region where you deployed the app (e.g. 'us-east-2'). The `[api-gateway-id]` can be found in the CloudFormation stack using the AWS CLI command below:

`aws cloudformation list-stack-resources --stack-name chalice-news-monitor-stack`

Look for the item with `"LogicalResourceId": "RestAPI"` and check the `"PhysicalResourceId"` attribute - that's your API Gateway ID.

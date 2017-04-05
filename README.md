# boto3-cloudformation
CLI implementation that emulates basic aws cli functionality. As we do basic implementations for our "doers" we are going to open source the base implementations so others can benefit.

# create stack
Create a stack with a web based template. This is a "sunny day" implementation, will probably be improved in future versions.

The help:
```
$ python create-stack.py -h
usage: create-stack.py [-h] --name NAME --templateurl TEMPLATEURL --params
                       PARAMS --topicarn TOPICARN [--log LOG] [--tags TAGS]
                       [--config CONFIG]

arguments:
  -h, --help            show this help message and exit
  --name NAME           the name of the stack to create.
  --templateurl TEMPLATEURL
                        the url where the stack template can be fetched.
  --params PARAMS       the key value pairs for the parameters of the stack.
  --topicarn TOPICARN   the SNS topic arn for notifications to be sent to.
  --log LOG             which log level. DEBUG, INFO, WARNING, CRITICAL
  --tags TAGS           the tags to attach to the stack.
  --config CONFIG       the config file used for the application.
```

{
    'ParameterKey': 'string',
    'ParameterValue': 'string',
    'UsePreviousValue': True|False
}


And an example:

```
$ python create-stack.py  --name newstack01  --templateurl https://raw.githubusercontent.com/dronzebot/dronze-qlearn/master/cicd/cloudformation/ec2_instance_sg.json?token=AAY5LkQG0d0G4Uql5Y8T-74L2BuGjKfNks5Y7kTAwA%3D%3D --params "KeyName=dronze-oregon-dev&InstanceType=t2.small"   --tags "name=newstack01&roo=mar"    --topicarn arn:aws:sns:us-west-2:705212546939:dronze-qlearn-cf
INFO       2017-04-05 08:17:07,009 make_cloudformation_client           50  : using default config.
INFO       2017-04-05 08:17:07,041 load                                 628 : Found credentials in shared credentials file: ~/.aws/credentials
INFO       2017-04-05 08:17:07,675 _new_conn                            735 : Starting new HTTPS connection (1): cloudformation.us-west-2.amazonaws.com
INFO       2017-04-05 08:17:08,345 main                                 111 : succeed. response: {"StackId": "arn:aws:cloudformation:us-west-2:705212546939:stack/newstack01/fd7ccbf0-1a11-11e7-a878-503ac9316861", "ResponseMetadata": {"RetryAttempts": 0, "HTTPStatusCode": 200, "RequestId": "eeef8f29-1a12-11e7-8b60-5b681d5e1677", "HTTPHeaders": {"x-amzn-requestid": "eeef8f29-1a12-11e7-8b60-5b681d5e1677", "date": "Wed, 05 Apr 2017 15:17:08 GMT", "content-length": "380", "content-type": "text/xml"}}}
```

# delete stack
Delete an existing stack. Includes a simple parser to allow retained resources to be excluded as comma separated string.

The help:
```
python delete-stack.py -h
usage: delete-stack.py [-h] --name NAME [--retain RETAIN] [--log LOG]
                       [--config CONFIG]
arguments:
  -h, --help       show this help message and exit
  --name NAME      the name of the stack to create.
  --retain RETAIN  the names (comma separated) of the resources to retain.
  --log LOG        which log level. DEBUG, INFO, WARNING, CRITICAL
  --config CONFIG  the config file used for the application
```

And an example:

```
$ python delete-stack.py --name newstack01

INFO       2017-04-04 18:03:17,576 make_cloudformation_client           50  : using default config.
INFO       2017-04-04 18:03:17,677 load                                 628 : Found credentials in shared credentials file: ~/.aws/credentials
INFO       2017-04-04 18:03:18,187 _new_conn                            735 : Starting new HTTPS connection (1): cloudformation.us-west-2.amazonaws.com
CRITICAL   2017-04-04 18:03:18,961 main                                 58  : succeed. response: {"ResponseMetadata": {"RetryAttempts": 0, "HTTPStatusCode": 200, "RequestId": "a7e04f04-199b-11e7-8a78-11614ee92102", "HTTPHeaders": {"x-amzn-requestid": "a7e04f04-199b-11e7-8a78-11614ee92102", "date": "Wed, 05 Apr 2017 01:03:18 GMT", "content-length": "212", "content-type": "text/xml"}}}
```

# using a custom configuration file
I don’t pass configurations on the CLI, to me the args on the CLI are about runtime not config. We have a config file that has the static configs in it:

```
AWS_ACCESS_KEY_ID=[my_access_key]
AWS_SECRET_ACCESS_KEY=[my_secret_access]
AWS_REGION_NAME="us-west-2"
LOG_LEVEL="INFO"
```

Boto3 is capable of auto configuration, and it will behave like aws CLI and attempt to find configs from ~/.aws/credentials but if you want explicit configs that is available using the config option in the CLI. If you do this the debug level will default to INFO.

# boto3-cloudformation
CLI implementation that emulates basic aws cli functionality. As we do basic implementations for our "doers" we are going to open source the base implementations so others can benefit.


# create stack
Create a stack with a web based template. This is a "sunny day" implementation, will probably be improved in future versions.

The help:
```
$ python create-stack.py -h
usage: create-stack.py [-h] --config CONFIG --name NAME --templateurl
                       TEMPLATEURL --params PARAMS --topicarn TOPICARN
                       [--tags TAGS]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       the config file used for the application.
  --name NAME           the name of the stack to create.
  --templateurl TEMPLATEURL
                        the url where the stack template can be fetched.
  --params PARAMS       the key value pairs for the parameters of the stack.
  --topicarn TOPICARN   the SNS topic arn for notifications to be sent to.
  --tags TAGS           the tags to attach to the stack.
```

And an example:

```
python create-stack.py \
--config /Users/claytongraham/data/tmp/config/local/snswebhook.properties \
 --name newstack01 \
 --templateurl https://raw.githubusercontent.com/dronzebot/dronze-qlearn/feature-58/cicd/cloudformation/ec2_instance_sg.json?token=AAY5LsvQDJYFGjuNcLPKBprZP-3eo27Iks5Y7C3uwA%3D%3D \
  --params "KeyName=dronze-oregon-dev&InstanceType=t2.small" \
  --tags "name=newstack01&roo=mar" \
   --topicarn arn:aws:sns:us-west-2:705212546939:dronze-qlearn-cf
```

# delete stack
Delete an existing stack. Includes a simple parser to allow retained resources to be excluded as comma separated string.

The help:
```
python delete-stack.py -h
usage: delete-stack.py [-h] --config CONFIG --name NAME [--retain RETAIN]

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  the config file used for the application.
  --name NAME      the name of the stack to create.
  --retain RETAIN  the names (comma separated) of the resources to retain.
```

And an example:

```
python delete-stack.py \
--config /Users/claytongraham/data/tmp/config/local/snswebhook.properties \
--name newstack01
```

# boto3-cloudformation
cli implementation that emulates basic aws cli functionality


# create stack
create a stack with a web based template
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
delete an existing stack

```
python delete-stack.py \
--config /Users/claytongraham/data/tmp/config/local/snswebhook.properties \
--name newstack01
```

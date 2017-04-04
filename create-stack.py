#!/usr/bin/env python
# coding: utf-8

import os
import json
import logging
import argparse
import boto3
import urllib2
import botocore
import sys
import time
import signal

from urlparse import urlparse, parse_qs

# Parameters=[
#     {
#         'ParameterKey': 'string',
#         'ParameterValue': 'string',
#         'UsePreviousValue': False
#     },
# ],
def make_kv_from_args(params_as_querystring, name_prefix="", use_previous=None):

    nvs = parse_qs(params_as_querystring)

    #{'i': ['main'], 'enc': [' Hello '], 'mode': ['front'], 'sid': ['12ab']}
    kv_pairs = []
    for key in nvs:
        # print "key: %s , value: %s" % (key, nvs[key])
        kv = {
            "{0}Key".format(name_prefix):key,
            "{0}Value".format(name_prefix):nvs[key][0],
        }
        if use_previous != None:
            kv['UsePreviousValue'] = use_previous

        kv_pairs.append(kv)

    return kv_pairs

def get_json(url, data_obj=None):
    try:
        url_final = "{0}".format(url)
        if data_obj:
            querystring = urllib.urlencode(data_obj)
            url_final = "{0}?{1}".format(url,querystring)

        get_headers={'Content-Type': 'application/json'}
        req = urllib2.Request(url_final, headers=get_headers)
        response = urllib2.urlopen(req)
        json_response = response.read()
        return json.loads(json_response)
    except urllib2.HTTPError as e:
        print e
        return None

def load_config(config_file):
    config = {}
    with open(config_file, 'r') as f:
        for line in f:
            line = line.rstrip() #removes trailing whitespace and '\n' chars

            if "=" not in line: continue #skips blanks and comments w/o =
            if line.startswith("#"): continue #skips comments which contain =

            k, v = line.split("=", 1)
            config[k] = v.replace("\"","")
    return config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True,
                       help='the config file used for the application.')
    parser.add_argument('--name', type=str, required=True,
                       help='the name of the stack to create.')
    parser.add_argument('--templateurl', type=str, required=True,
                       help='the url where the stack template can be fetched.')
    parser.add_argument('--params', type=str, required=True,
                       help='the key value pairs for the parameters of the stack.')
    parser.add_argument('--topicarn', type=str, required=True,
                       help='the SNS topic arn for notifications to be sent to.')
    parser.add_argument('--tags', type=str, required=False,
                       help='the tags to attach to the stack.')

    args = parser.parse_args()

    #load the app config
    config = load_config(args.config)

    client = boto3.client('cloudformation',
        config["AWS_REGION_NAME"],
        aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"])

    template_object = get_json(args.templateurl)

    params = make_kv_from_args(args.params, "Parameter", False)
    tags = make_kv_from_args(args.tags)

    response = client.create_stack(
        StackName=args.name,
        TemplateBody=json.dumps(template_object),
        Parameters=params,
        DisableRollback=False,
        TimeoutInMinutes=2,
        NotificationARNs=[args.topicarn],
        Tags=tags
    )

    if 'ResponseMetadata' in response and \
        response['ResponseMetadata']['HTTPStatusCode'] == 200
        print "succeed."
    else:
        print "there was a problem. response:{0}".format(json.dumps(response))


if __name__ == '__main__':
    main()

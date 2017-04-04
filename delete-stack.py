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
    parser.add_argument('--retain', type=str, required=False,
                       help='the names (comma deliminated) of the reesources to retain.')

    args = parser.parse_args()

    #load the app config
    config = load_config(args.config)

    client = boto3.client('cloudformation',
        config["AWS_REGION_NAME"],
        aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"])

    retained_resources = []

    if args.retain and len(args.retain)>0:
        retained_respources = args.retain.split(",")

    response = client.delete_stack(
        StackName=args.name,
        RetainResources=retained_resources
    )

    if 'ResponseMetadata' in response and \
        response['ResponseMetadata']['HTTPStatusCode'] == 200
        print "succeed."
    else:
        print "there was a problem. response:{0}".format(json.dumps(response))


if __name__ == '__main__':
    main()

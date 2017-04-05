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
from utils import make_cloudformation_client, load_config, get_log_level

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True,
                       help='the name of the stack to create.')
    parser.add_argument('--retain', type=str, required=False,
                       help='the names (comma separated) of the resources to retain.')
    parser.add_argument('--log', type=str, default="INFO", required=False,
                       help='which log level. DEBUG, INFO, WARNING, CRITICAL')
    parser.add_argument('--config', type=str, required=False,
                       help='the config file used for the application.')

    args = parser.parse_args()

    # init LOGGER
    logging.basicConfig(level=get_log_level(args.log), format=LOG_FORMAT)

    #load the client using app config or default
    client = make_cloudformation_client(args.config)

    try:
        retained_resources = []

        if args.retain and len(args.retain)>0:
            retained_respources = args.retain.split(",")

        response = client.delete_stack(
            StackName=args.name,
            RetainResources=retained_resources
        )

        # we expect a response, if its missing on non 200 then show response
        if 'ResponseMetadata' in response and \
            response['ResponseMetadata']['HTTPStatusCode'] < 300:
            logging.info("succeed. response: {0}".format(json.dumps(response)))
        else:
            logging.critical("There was an Unexpected error. response: {0}".format(json.dumps(response)))

    except ValueError as e:
        logging.critical("Value error caught: {0}".format(e))
    except:
        # catch any failure
        logging.critical("Unexpected error: {0}".format(sys.exc_info()[0]))


if __name__ == '__main__':
    main()

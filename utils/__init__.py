#!/usr/bin/env python
# coding: utf-8
import logging
import boto3

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

def get_log_level(level_string):
    levels = {
        "DEBUG":logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "CRITICAL":logging.CRITICAL
    }
    return levels[level_string]

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

def make_cloudformation_client(config=None):
    """
    this method will attempt to make a boto3 client
    it manages the choice for a custom config
    """
    #load the app config
    client = None
    if config != None:
        logging.info("using custom config.")
        config = load_config(args.config)
        client = boto3.client('cloudformation',
            config["AWS_REGION_NAME"],
            aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"])
    else:
        # we dont have a configuration, lets use the
        # standard configuration fallback
        logging.info("using default config.")
        client = boto3.client('cloudformation')

    if not client:
        raise ValueError('Not able to initialize boto3 client with configuration.')
    else:
        return client

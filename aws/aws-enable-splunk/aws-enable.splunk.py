#!/usr/bin/env python

# AWS enable splunk // for Schibsted
#
# Copyright (c) 2015 - Albert Puigsech Galicia (albert.puigsech@schibsted.com / albert@puigsech.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
import argparse
import configparser
from boto import *


def parse_options(argv):
	parser = argparse.ArgumentParser(description='AWS enable Splunk')
	parser.add_argument('-c', '--config', type=argparse.FileType('r'), default='~/.aws/config', help='Configuration file')
	parser.add_argument('-s', '--set', nargs=2, default=[], action='append')
	return parser.parse_args(argv[1:])
 
 
def parse_config(fh):
	config = configparser.RawConfigParser(allow_no_value=True)
	config.read_file(fh)
	return config


def get_config(opt):
	conf = parse_config(opt.config)
	for s in opt.set:
		section, key, value = s[0].split('.', 1) + [s[1]]
		conf.set(section, key, value)
	return conf		


def conf_s3(conf):
	try:
		aws = s3.connect_to_region(
			conf.get('auth', 'region'),
			aws_access_key_id=conf.get('auth', 'access-key'),
			aws_secret_access_key=conf.get('auth', 'secret-key')
		)

		aws.create_bucket(conf.get('audit', 'bucket'), location=conf.get('auth', 'region'))
	except Exception as e:
		print e
		exit(1)	


def conf_iam(conf):
	try:
		aws = s3.connect_to_region(
			conf.get('auth', 'region'),
			aws_access_key_id=conf.get('auth', 'access-key'),
			aws_secret_access_key=conf.get('auth', 'secret-key')
		)

		user_name = conf.get('audit', 'user')
		group_name = conf.get('audit', 'group')

		aws.create_user(user_name)
		aws.create_user(group_name)
		aws.add_user_to_group(group_name, user_name)
	except Exception as e:
		print e
		exit(1)	
	

def conf_cloudtrail(conf):
	try:
		aws = cloudtrail.connect_to_region(
			conf.get('auth', 'region'),
			aws_access_key_id=conf.get('auth', 'access-key'),
			aws_secret_access_key=conf.get('auth', 'secret-key')
		)

		aws.create_trail(name='audit', s3_bucket_name=conf.get('audit', 'bucket'))
	except Exception as e:
		print e
		exit(1)	


def main(argv):
	conf = get_config(parse_options(argv))

	print "s3"
	conf_s3(conf)
	print "ct"
	conf_cloudtrail(conf)
	print "iam"
	conf_iam(conf)



if __name__ == "__main__":
        main(sys.argv)
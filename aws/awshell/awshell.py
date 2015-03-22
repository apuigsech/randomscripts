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
import yaml
from boto import *


def parse_options(argv):
	parser = argparse.ArgumentParser(description='AWS enable Splunk')
	parser.add_argument('-c', '--config', type=argparse.FileType('r'), default='~/.aws/config', help='Configuration file')
	parser.add_argument('-s', '--set', nargs=2, default=[], action='append', help='Overlay set for configuration')
	parser.add_argument('action', nargs='+', type=argparse.FileType('r'), help='Action files')
	return parser.parse_args(argv[1:])
 
 
def parse_conf(fh):
	conf = configparser.RawConfigParser(allow_no_value=True)
	conf.read_file(fh)
	return conf


def overlay_conf(conf, opt):
	for s in opt.set:
		section, key, value = s[0].split('.', 1) + [s[1]]
		conf.set(section, key, value)
	return conf


def parse_act(fh):
	return yaml.load(fh)


def execute_act(act):
	try:
		for app in act.keys():
			getattr(sys.modules[__name__], "execute_act_%s" % app)(act[app])
	except Exception as e:
		print e
		return None
	

def execute_act_iam(act):
	aws = connect_aws('iam')


def connect_aws(app):
	global opt
	try:
		aws = getattr(sys.modules[__name__], 's3').connect_to_region(
			opt.get('auth', 'region'),
			aws_access_key_id=opt.get('auth', 'access-key'),
			aws_secret_access_key=opt.get('auth', 'secret-key')
		)

		aws.create_bucket(conf.get('audit', 'bucket'), location=conf.get('auth', 'region'))
	except Exception as e:
		print e
		exit(1)	


def main(argv):
	global opt 
	opt = parse_options(argv)
	conf = parse_conf(opt.config)
	conf = overlay_conf(conf, opt)

	for action in opt.action:
		execute_act(parse_act(action))


if __name__ == "__main__":
	main(sys.argv)
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
import boto.iam


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


def main(argv):
	conf = get_config(parse_options(argv))

	try:
		iam = boto.iam.connect_to_region(
			conf.get('auth', 'region'),
			aws_access_key_id=conf.get('auth', 'access-key'),
			aws_secret_access_key=conf.get('auth', 'secret-key')
		)
	except Exception as e:
		print e
		exit(1)

	try:
		iam.create_user(conf.get('splunk', 'username'))
	except Exception as e:
		print e
		exit(1)


if __name__ == "__main__":
        main(sys.argv)
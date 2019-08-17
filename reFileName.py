# -*- coding: UTF-8 -*-
#
# frendyxzc@126.com
# 2018.03.27

import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rootdir', type=str, default='.',
                       help='Root Directory such as: /Users/frendy/Desktop/images')
    parser.add_argument('--suffix', type=str, default='',
                       help=u'suffix')
    parser.add_argument('--format', type=str, default='',
                       help=u'format')
    args = parser.parse_args()
    return args


if __name__=='__main__':
    args = parse_args()
    
    suffix = args.suffix
    format = args.format

	for file in os.listdir('.'):
	    if file[-2: ] == 'py':
	        continue
	    name = file.replace(' ', '').split('.')[0]
	    new_name = name + suffix + format
	    os.rename(file, new_name)

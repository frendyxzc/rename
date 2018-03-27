# -*- coding: UTF-8 -*-
#
# frendyxzc@126.com
# 2018.03.27

import os
import re
import shutil
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rootdir', type=str, default='.',
                       help='Root Directory such as: /Users/frendy/Desktop/project/alarm/v100/Clock')
    parser.add_argument('--src', type=str, default='',
                       help=u'Origin such as: com.frendy.origin')
    parser.add_argument('--dst', type=str, default='',
                       help=u'Target such as: com.frendy.target')
    args = parser.parse_args()
    return args

#list files
def listFiles(dirPath):
    fileList=[]

    for root,dirs,files in os.walk(dirPath):
        for fileObj in files:
            fileList.append(os.path.join(root,fileObj))

    return fileList


def _refactor_file(fileObj, src, dst):
    f = open(fileObj,'r+')
    all_the_lines=f.readlines()
    f.seek(0)
    f.truncate()

    for line in all_the_lines:
        f.write(line.replace(src, dst))    

    f.close()


def _refactor(fileDir, src, dst):
    fileList = listFiles(fileDir)

    for fileObj in fileList:
        _refactor_file(fileObj, src, dst)


def refactor(rootDir, src, dst):
	_refactor(rootDir + "/app/src/main/java", src, dst)
	_refactor(rootDir + "/app/src/main/res", src, dst)
	_refactor_file(rootDir + "/app/src/main/AndroidManifest.xml", src, dst)
	_refactor_file(rootDir + "/app/proguard-rules.pro", src, dst)


if __name__=='__main__':
    args = parse_args()
    
    src = args.rootdir + "/app/src/main/java/" + args.src.replace('.', '/')
    dst = args.rootdir + "/app/src/main/java/" + args.dst.replace('.', '/')
    shutil.copytree(src, dst)
    #shutil.rmtree(src)

    refactor(args.rootdir, args.src, args.dst)

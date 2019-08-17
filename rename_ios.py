# -*- coding: UTF-8 -*-
#
# frendyxzc@126.com
# 2019.08.17

import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rootdir', type=str, default='.',
                        help='Root Directory such as: /Users/frendy/Desktop/iOS/rename/Lunar_iOS')
    parser.add_argument('--project', type=str, default='.',
                        help='Root Directory such as: Lunar')
    parser.add_argument('--src', type=str, default='',
                        help=u'Origin such as: origin')
    parser.add_argument('--dst', type=str, default='',
                        help=u'Target such as: target')
    args = parser.parse_args()
    return args


def getFileSuffix(file):
    return os.path.splitext(file)[-1]

def getFileName(file):
    return file.split("/")[-1].replace(getFileSuffix(file), '')

def getFilePath(file):
    return os.path.dirname(file)


# list files
def listFiles(dirPath):
    fileList = []

    for root, dirs, files in os.walk(dirPath):
        for fileObj in files:
            if getFileSuffix(fileObj) == '.m' or getFileSuffix(fileObj) == '.h':
                fileList.append(os.path.join(root, fileObj))

    return fileList


def listXibFiles(dirPath):
    fileList = []

    for root, dirs, files in os.walk(dirPath):
        for fileObj in files:
            if getFileSuffix(fileObj) == '.xib':
                fileList.append(os.path.join(root, fileObj))

    return fileList


def _refactor_file(fileObj, src, dst):
    f = open(fileObj, 'r+')
    all_the_lines = f.readlines()
    f.seek(0)
    f.truncate()

    for line in all_the_lines:
        f.write(line.replace(src, dst))

    f.close()


def _refactor(rootDir, project, src, dst):
    filePath = rootDir + '/' + project
    fileList = listFiles(filePath)

    listLen = len(fileList)
    total = listLen * listLen
    cnt = 0

    fileMap = {}

    for fileObj in fileList:
        path = getFilePath(fileObj)
        name = getFileName(fileObj)
        suffix = getFileSuffix(fileObj)

        if src in name:
            newName = name.replace(src, dst)
            newObj = path + '/' + newName + suffix

            xcodeproj = rootDir + '/' + project + '.xcodeproj/project.pbxproj'
            _refactor_file(xcodeproj, name + suffix, newName + suffix)

            for _fileObj in fileList:
                if os.path.exists(_fileObj):
                    _refactor_file(_fileObj, name, newName)
                else:
                    _path = getFilePath(_fileObj)
                    _name = getFileName(_fileObj)
                    _suffix = getFileSuffix(_fileObj)

                    if fileMap.has_key(_name + _suffix):
                        _filePath = _path + '/' + fileMap[_name + _suffix]
                        _refactor_file(_filePath, name, newName)

                cnt += 1
                print 'Process 1: %d / %d\r' % (cnt, total)

            fileMap[name + suffix] = newName + suffix

            os.rename(fileObj, newObj)

        else:
            cnt += listLen
            print 'Process 1: %d / %d\r' % (cnt, total)


    ### check again
    refactor2(rootDir, project, src, dst, fileMap)
    refactor3(rootDir, project, src, dst, fileMap)


def refactor1(rootDir, project, src, dst):
    _refactor(rootDir, project, src, dst)

def refactor2(rootDir, project, src, dst, fileMap):
    filePath1 = rootDir + '/' + project
    filePath2 = rootDir + '/' + 'Notification'

    fileList = listFiles(filePath1)
    fileList.extend(listFiles(filePath2))

    listLen = len(fileList)
    total = listLen * len(fileMap)
    cnt = 0

    for fileObj in fileList:
        for value in fileMap.values():
            newName = value.replace(getFileSuffix(value), '')
            oldName = newName.replace(dst, src)

            if os.path.exists(fileObj):
                _refactor_file(fileObj, oldName, newName)
            else:
                _path = getFilePath(fileObj)
                _name = getFileName(fileObj)
                _suffix = getFileSuffix(fileObj)

                if fileMap.has_key(_name + _suffix):
                    _filePath = _path + '/' + fileMap[_name + _suffix]
                    _refactor_file(_filePath, oldName, newName)

            cnt += 1
            print 'Process 2: %d / %d\r' % (cnt, total)


def refactor3(rootDir, project, src, dst, fileMap):
    filePath1 = rootDir + '/' + project
    filePath2 = rootDir + '/' + 'Notification'

    fileList = listXibFiles(filePath1)
    fileList.extend(listXibFiles(filePath2))

    listLen = len(fileList)
    total = listLen * len(fileMap)
    cnt = 0

    for fileObj in fileList:
        path = getFilePath(fileObj)
        name = getFileName(fileObj)
        suffix = getFileSuffix(fileObj)

        newName = name.replace(src, dst)

        if (newName + '.h') in fileMap.values() or (newName + '.m') in fileMap.values():
            newObj = path + '/' + (name + suffix)

            os.rename(fileObj, newObj)

            cnt += 1
            print 'Process 3: %d / %d\r' % (cnt, total)


if __name__ == '__main__':
    args = parse_args()

    refactor1(args.rootdir, args.project, args.src, args.dst)
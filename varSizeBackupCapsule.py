import sys
import os
import time
import shutil
import argparse
import re

def main():
  global sortedPathList
  global basket
  global pathList
  excArgParser = argparse.ArgumentParser(prog='varSizeBackupCapsule', description='Create Time-Capsule Backup of user defined size for a directory',conflict_handler='resolve')
  excArgParser.add_argument('-excMode', default='auto', type=str, choices=['debug','manual','auto'])
  excArgParser.add_argument('-configFile', default = 'varSizeBackupConfig.txt', type=str)
  excArgs = excArgParser.parse_args()
  if excArgs.excMode == 'auto':   #auto mode, auto operation(create backup when basket full)
          excAuto = True                  # display nothing
          dspInfo = False
  elif excArgs.excMode == 'manual':       #manual mode, manual operation, display minimum
          excAuto = False
          dspInfo = False
  elif excArgs.excMode == 'debug':        #debug mode, manual operation, display all info
          excAuto = False
          dspInfo = True
  else:   #User input gibberish for excMode parameter, default to manual mode
          excAuto = False
          dspInfo = False
  if excAuto:
      try:
        argFile = open(excArgs.configFile, 'r')
      except:
        print('Faile to open backup config file, check file and its name') if dspInfo==True else None
        sys.exit()
      srcPath = argFile.readline().strip()
      dstPath = argFile.readline().strip()
      backupSize = argFile.readline().strip()
      fileName = argFile.readline()
      argFile.close()
  else:
      srcPath = input("Enter a Directory: ")
      dstPath = input("Enter a Destination Directory (root): ")
      backupSize = input("The size of the back up increment (Byte): ")
  currentDir = os.getcwd()
  if not os.path.isdir(srcPath):
      print(srcPath," is not a valid directory. Exit") if dspInfo == True else None
      sys.exit()
  else:
      print (srcPath, " is the backup directory") if dspInfo == True else None
  if not os.path.isdir(dstPath):
      os.makedirs(dstPath,exist_ok=True)
  totalSize = listDir(srcPath)
  sortedPathList = sorted(pathList)	#sort the file list according to their modification time earliest to latest
  if excAuto == False:
      fileName = input("Enter the path/name to the metadata file: ")
  inFile = open(fileName,'r')
  outFile = open(fileName,'a')
  dateStr = inFile.readline()
  inFile.close()
  headDate = float(dateStr)
  print (time.ctime(headDate))
  for date, path, size in sortedPathList:
      print (time.ctime(date),path) if dspInfo == True else None
  print ('Total Directory Size (Byte): ',totalSize/1024/1024/1024) if dspInfo == True else None
  print ('+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+') if dspInfo == True else None
  fillTheBasket(int(backupSize),srcPath,dstPath,headDate,excAuto,dspInfo)
  for date, path in basket:
    metaStr = time.ctime(date)+' '+path
    print (metaStr) if dspInfo == True else None
    metaStr = str(date)+' '+metaStr+'\n'
    outFile.write(metaStr)
  outFile.write(str(date))
  outFile.close()
  newDstPath = nextMetaFileName(dstPath)
  newMetaFileName = nextMetaFileName(fileName)
  nextMetaFile = open(newMetaFileName, 'w')
  nextMetaFile.write(str(date)+'\n')
  nextMetaFile.close()
  argFileUpdate = open('varSizeBackupConfig.txt','w')
  argFileUpdate.write(srcPath+'\n')
  argFileUpdate.write(newDstPath+'\n')
  argFileUpdate.write(backupSize+'\n')
  argFileUpdate.write(newMetaFileName+'\n')
  argFileUpdate.close()

pathList = []
sortedPathList = []
basket = [];
def listDir(path):
  global pathList
  dirList = os.listdir(path)
  totalDirSize = 0
  for element in dirList:
    if os.path.isfile(os.path.join(path,element)):
        fileInfo = os.stat(os.path.join(path,element))
        totalDirSize += fileInfo.st_size
        pathList.append([fileInfo.st_mtime,os.path.join(path,element),fileInfo.st_size])
    else:   # For directory item that is a folder, recursion to drill deeper
        totalDirSize += listDir(os.path.join(path,element))
  return totalDirSize
		
def fillTheBasket(capacity,srcDir,dstDir,lastTailDate,autoMode,dspMode):
  global basket
  basketSize = 0
  basketFull = False
  for date, path, size in sortedPathList:
      if date <= lastTailDate:
          continue
      basketSize += size
      if basketSize >= capacity:
          basketSize -= size
          basketFull = True
          break
      else:
          basket.append([date,path])
  print('Final Basket Size (GB): ',basketSize/1024/1024/1024,'||Basket Full? ', basketFull)
  prcdCmd = basketFull if autoMode == True else input("Preceed to build backup folder? (y/n)")=="y"
  if prcdCmd:
      pass
  else:
      sys.exit()
  for date, srcPath in basket:
      path, fileName = os.path.split(srcPath)
      dstPath = path.replace(srcDir,dstDir)	#replace old root directory with new root directory
      os.makedirs(dstPath,exist_ok=True)	#try to make the destination directory if it doesn't already exist
      dstPath = os.path.join(dstPath,fileName)
      print (srcPath,dstPath) if dspMode==True else None
      shutil.copy2(srcPath,dstPath)
  return date

def nextMetaFileName(metaFileName):
    numericalComponents = re.findall(r'\d+', metaFileName)
    newMetaNumStr = str(int(numericalComponents[0])+1)
    newMetaFileName = metaFileName.replace(numericalComponents[0],newMetaNumStr,1)
    return newMetaFileName

main()

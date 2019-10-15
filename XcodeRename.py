#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by luo.h on 2018/7/4
# software: PyCharm
# 功能:修改Xcode名称，混淆SDK，可以适用于含有多个xcodeproj文件工程

import os, sys, re
import click

old_name= 'Game_Framework'  				 	# 需要修改的类名或前缀 （需替换）
new_name= 'NewGameFramework'		      		# 新的类名或前缀 （需替换）
project_path="/Users/apple10/FrameworkDemo"     #工程路径



suf_set_text = ('appiconset','.bundle',".h",".m",".mm",".xib",'.storyboard',".pch",'.framework')
suf_set_rename = ('xcodeproj','appiconset', 'plist','.bundle',".h",".m",".mm",".xib",'.storyboard',".pch",'.framework','.zip')
suf_set_pbxproj=('pbxproj', 'xcworkspace', 'xcscheme', 'xcshareddata', 'xcuserdata','xcuserdatad')

def updateFileContentText(full_path, old_str, new_str):
	(filepath, tempfilename) = os.path.split(full_path)
	(filename, extension) = os.path.splitext(tempfilename)
	if extension.endswith(suf_set_pbxproj) == False:
		return
	if extension.endswith(".zip") == True:
		return
			
	all_text=ReadFile(full_path)	
	print("updateContent-filePath✅: " + full_path)  # 输出文件路径信息
	content = re.sub(r'(%s)(?!\+|\s|\/)' % (old_str), new_str, all_text)
#	content = re.sub(r'(?<=\")(%s)(?=\")' % (old_str), new_str, all_text)
	if content != all_text:
		WriteFile(full_path,content)
		click.secho('更新文件内容' + full_path,fg="green")

# 遍历文件，在文件中更换新类名的引用
def start_AllClassRef_rename():
	for (root, dirs, files) in os.walk(project_path):
		for file_name in files:
			if file_name.endswith(suf_set_text):
				file_Path=os.path.join(root, file_name)
				fileText_0=ReadFile(file_Path)
				for key in needModifyDic:
					if key in fileText_0:
						print('—–fileName——-' + file_name)
						oldText=ReadFile(file_Path)
						print(key + ' ——> ' + needModifyDic[key])
						newtext=oldText.replace(key, needModifyDic[key])
						WriteFile(file_Path, newtext)
						
						
def fileExInfo(file_path):
	(filepath,tempfilename) = os.path.split(file_path);		 #filepath=文件目录 tempfilename=文件名包含扩展名
	(shotname,extension) = os.path.splitext(tempfilename);   #shotname=文件名   extension=文件扩展名
	return filepath,tempfilename,shotname,extension
		

# 文件重命名函数，返回新的文件名
def file_rename(file_path):
	root_path,root_name,filename,extension=fileExInfo(file_path)
	newfilename=filename.replace(old_name, new_name)
	new_path = os.path.join(root_path,newfilename+ extension)    # 拼接新路径
	os.renames(file_path, new_path)             # 文件重命名
	return newfilename
	
def start_file_rename(pre_str,pre_to_str):
	modifyDic = {}
	for (root, dirs, files) in os.walk(project_path):
		root_path,root_name,filename,extension=fileExInfo(root)
		#修改文件-先修改文件以防文件夹目录错误
		for file_name in files:
			file_path=os.path.join(root, file_name)
			if file_name.startswith((pre_str,)) and file_name.endswith(suf_set_rename):
				print("file_name:\n"+file_name)
				old_name = os.path.splitext(file_name)[0]
				new_name = file_rename(os.path.join(root, file_name))
				modifyDic[old_name] = new_name
					
		#修改文件夹		
		if root_name.startswith(pre_str) and root_name.endswith(suf_set_rename):
			print("root_name:\n"+root_name)
			old_name = os.path.splitext(root_name)[0]
			new_name = file_rename(os.path.join(root_path, root_name))
			modifyDic[old_name] = new_name
	print(modifyDic)
	return modifyDic
	
	
def scanXcodeprojPath(some_dir):
	some_dir = some_dir.rstrip(os.path.sep)
	assert os.path.isdir(some_dir)
	for root, dirs, filenames in os.walk(some_dir):
		for file_name in filenames:  # 输出文件信息
			filePath = os.path.join(root, file_name)
			updateFileContentText(filePath,old_name, new_name)


#文本方式读取文件
def ReadFile(filePath):
	print("file✅:"+filePath)
	with open(filePath,'r') as file_obj:
		data = file_obj.read()
		file_obj.close()
	return data
	
#文本方式写入文件
def WriteFile(filePath,data):
	file_obj = open(filePath,'w')    
	file_obj.write(data)
	file_obj.close()

			
def find_Specifiedfolders(rootDirname,folderName):
	xcodeprojPaths=[]
	for root, dirs, files in os.walk(rootDirname):
		for dirpath in dirs:
			if dirpath.endswith(folderName):
				folderNamepath=os.path.join(root, dirpath)
				xcodeprojPaths.append(folderNamepath)
			else:
				pass
	return  xcodeprojPaths
				

## 替换配置文件中的类名
def start_pbxpro_rename(modifyDic):	
	# 项目project.pbxproj文件路径 需要更新配置文件中的类名 （找到自己的项目project.pbxproj路径）
	xcodeproj_paths=find_Specifiedfolders(project_path,".xcodeproj")
	for pbxpro_path in xcodeproj_paths:
		scanXcodeprojPath(pbxpro_path)


def testDemo():
	global needModifyDic
	#1、修改文件名
	needModifyDic=start_file_rename(old_name,new_name)

	#2、修改文本文件
	start_AllClassRef_rename()
	
	#3、修改pbxproj配置文件
	start_pbxpro_rename(needModifyDic)
	
	
if __name__ == '__main__':
#    main()
	 testDemo()
	
	
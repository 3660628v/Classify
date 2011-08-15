#coding=utf-8
import web
import web.webapi
import os,shutil
from datetime import date
from model.video import *
from model.member import *
from model.node   import *
from config import *
import json

class UploadError:
	def GET(self):
		type = 'toolarge'
		a={}
		a["stauts"]=False
		a["img"]   = '文件太大!'
		if 'type' in web.input():
			type = web.input().type
		if type == 'notimge':
			a["img"] = '文件格式错误!'
		return json.dumps(a)

class UploadVideo:
	def POST(self):
		member 		= get_member_by_name("")
		node		= get_node_by_url_name("")
		video		= add_a_new_video(node,member,web.input())
		return video
		
class UploadImage:
	def mv_uploadfile_to_tmppath(self):
		if not 'origin_image_path' in web.input():
			return (False,None)
		if not 'origin_image_md5' in web.input():
			return (False,None)
		if not 'origin_image_content_type' in web.input():
			return (False,None)
		# 临时目录
		
		img_tmp_path = path_setting.html_document_root + path_setting.tmp_img_root_dir	+ '/' + date.today().isoformat()
		# 临时文件
		img_tmp_name = web.input().origin_image_md5+'.'+web.input().origin_image_content_type.split('/')[1]
		img_tmp_file = img_tmp_path + '/' + img_tmp_name 
		img_tmp_uri  = path_setting.tmp_img_root_dir + '/' +  date.today().isoformat()  + '/' + img_tmp_name
		print img_tmp_path
		print img_tmp_file
		try:
			os.mkdir(img_tmp_path)
		except OSError,a:
			print a
			pass
		try:
			shutil.move(web.input().origin_image_path,img_tmp_file)
		except IOError,a:
			print a
			return (False,None)
		return (True,img_tmp_uri)
		
	def is_image(self):
		if not 'origin_image_content_type' in web.input():
			return(False,None)	

		print web.input().origin_image_content_type
		a = ['image/gif','image/jpg','image/jpeg','image/png']
		error = "请上传图片文件"
		print error
		if web.input().origin_image_content_type.split('/')[0] == 'image': 
			return (True,None)
		else:
			return (False,error)
	def POST(self):
		print web.input()
		redirect_path = '/demo/uploadfile.html'
		(status,err) = self.is_image()
		a	     = {}
		if status == False:
			a["status"]	=     False
			a["img"]	=     err
			raise web.webapi.HTTPError('400', {},json.dumps(a))
		(status,err) = self.mv_uploadfile_to_tmppath()
		if status == False:
			a["status"]	=     False
			a["img"]	=     "上传失败"
			raise web.webapi.HTTPError('400', {},json.dumps(a))
		a["status"]	=	True
		a["img"]	=	err
		return json.dumps(a)

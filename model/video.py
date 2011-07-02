# coding=utf-8
from model import *
from node  import *
from member import *
from default import *
import bson.objectid
import datetime
import config
import os,shutil

def process_tag(tags):
	return tags

def video_verify(location):
	##'file_content_type': u'video/mp4"'
	## if md5 is same return False
	return True
def video_time(video):
	return True

def video_image(video):
	## 在正确的目录下生成缩略图
	image_file_name = config.video_setting.image_path+'/'+video.video_md5 +".jpg"
	cmd = "/usr/bin/ffmpeg -y -i " + video.location + " -ss "+str(video.image_time)+" -s 160x90 -vframes 1 -an -sameq -f image2 "+image_file_name + "1>/var/tmp/tt.txt 2>/var/tmp/tt.txt"
	re	=	os.system(cmd)
	if re !=0 :
		video.fail_reason = u"video image process fail!";
		return False
	video.image = image_file_name
	return True;

def video_move(video):
	video_name = video.video_md5
	video_name =  config.video_setting.video_path+'/'+video_name;
	shutil.move(video.location,video_name)
	video.location = video_name;
	return True;

def process_video(video):
	if video.status != video_status_wait_process:
 		return
	if not video.location  or video.location.strip() == '':
		video.fail_reason = u"video location is null";
		return 
	if not video_verify(video.location):
		video.fail_reason = u"video verify fail"
		return
	if not video_time(video):
		video.fail_reason = u"video cal time fail"
		return
	if not video_image(video):
		video.fail_reason = u"video produce image error"
		return
	if not video_move(video):
		video.fail_reason = u"video move fail"
		return
	video.status = video_status_wait_published

	return

	
def str_to_unicode(video):
	video.title  	= unicode(video.title)
	video.content	= unicode(video.content)
	video.tags	= unicode(video.tags)
	video.image	= unicode(video.image)
	video.location  = unicode(video.location)

	
	
def add_a_new_video(node,member,webinput):
	video = connection.Video();
	video.title		=	webinput.title
	video.content   	=       webinput.content
	video.content_length	=	len(video.content)
	video.node_url		=	node.url
	video.node_name		=	node.name
	video.node_ref		=	node._id
	video.author		=	member.name
	video.author_ref	=	member._id
	video.location		=	webinput.file_path
	video.tags		=	process_tag(webinput.tags)
	video.video_md5		=	webinput.file_md5
## 这个过程应该放在后台任务
	process_video(video)
	str_to_unicode(video)
	video.save()
	return video

class video_test:
	def __init__(self):
		self.location 		= '/var/tmp/upload_video/2/0000000002'
		self.image_time		= 5
		self.video_md5		= 'xxrrrdddssss'

if __name__ == '__main__':
	a = video_test ()
	if video_image(a):
		print "ok"
		print a.image
		print a.location
		#video_move(a)
		print a.location
	

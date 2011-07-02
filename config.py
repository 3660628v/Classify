#coding=utf-8
from pymongo import Connection

##
version			= ('0','1','0')
##
debug			= True
##数据库配置
mongodb_host 		= "127.0.0.1"
mongodb_port 		= 27017
## 数据库名称
if debug:
	classify_database	= "shitao_debug"
else:
	classify_database	= "shitao"
class collection_name():
	pass;

collection_name.Topic		= 'topic'
collection_name.Reply		= 'reply'
collection_name.Node		= 'node'
collection_name.Member		= 'member'
collection_name.Video		= 'video'


### 模板相对的路径都是以view/template为前缀的
## 桌面模板 
template_desktop_path		= "desktop/"

class template():
	pass;
## 
template.chevron = u'<span class="chevron">&nbsp;›&nbsp;</span>' 
template.add_a_reply_now 	= u'现在添加一条回复'
template.reply		 	= u'回复'
template.till		 	= u'直到'
template.send		 	= u'发送'
template.create_new_topic 	= u"创建新主题"
template.total_topics 		= u'主题总数'
template.create			= u'创建'




class site():
	pass

## 网站名称
site.title			= u"视淘"
site.use_topic_types		= False

class video_setting():
	pass

####目录权限也可以通过，把webserver和uwsgi的用户组设为同一个解决
#这个必须要有写权限,上级目录必须要有执行权限
video_setting.image_path	= '/srv/www/shitao.com/public_html/static_file/video_img/'
## 这个目录最终要放在不可下载目录下,这个必须是绝对路径
#这个必须要有写权限,上级目录必须要有执行权限
video_setting.video_path	= '/srv/www/shitao.com/upload_video/'



if __name__ == "__main__":
	print site.title
	print a.b

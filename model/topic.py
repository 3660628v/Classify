# coding=utf-8
from model import *
from node  import *
from member import *
import bson.objectid
import datetime
import config

def add_new_topic(node,member,title,video,content):
	topic	= connection.Topic()
	topic.title		=	title
	topic.content		= 	content
	topic.content_length	= 	len(topic.content)
	topic.author		= 	member.name
	topic.author_ref	=	member._id
	topic.video.where	=	video
	topic.node_url		=	node.url
	topic.node_name		=	node.name
	topic.node_ref		=	node._id
	topic.save()
	return topic

def add_a_new_topic(node,member,webinput):
	topic			=	connection.Topic()
	topic.title		=	webinput.title
	topic.content		=	webinput.content
	topic.content_length	=	len(webinput.content)
	topic.author		=	member.get_dbref()
	topic.node		=	node.get_dbref()
	topic.save()
	inc_topic_num(node,1)
	return topic

def remove_a_topic(node,topic):
	connection[config.classify_database][config.collection_name.Topic].remove({'_id':bson.objectid.ObjectId(topic._id)})
	inc_topic_num(node,-1)
	return
	


def add_new_reply_to_topic(topic_id,reply_time,reply_author):
	## 这里必须这样用
	## connection.Topic不好使
	connection[config.classify_database][config.collection_name.Topic].update(
		{'_id':topic_id}, 
		{ '$inc':{"reply_num":1} ,
		  '$set':{"last_reply_by":reply_author,"last_reply_time":reply_time}
		
		} 
	)



def find_topic_by_id(topic_id):
	return connection.Topic.find_one({'_id':bson.objectid.ObjectId(topic_id)})

def hit_topic_by_topic_id(topic_id):
	connection[config.classify_database][config.collection_name.Topic].update(
		{'_id':bson.objectid.ObjectId(topic_id)},
		{ '$inc':{"hits":1}}
	)

def find_all_node_topic_by_node_url_name(node_url_name):
	return connection.Topic.fetch({"node_url":node_url_name}).sort([('last_reply_time',-1)])
	
	

	
if __name__=='__main__':
	#add_new_reply_to_topic(bson.objectid.ObjectId('4ddc49c0decbef09c3000000'),datetime.datetime.now(),u"mgw")
	#for reply in get_reply_by_topic_id('4ddc49c0decbef09c3000000'):
	#	print reply
	#print find_topic_by_id('4ddc49c0decbef09c3000000')
	#hit_topic_by_topic_id('4ddc49c0decbef09c3000000')
	#topic=find_topic_by_id('4ddc49c0decbef09c3000000')
	#print topic
	#print type(topic.hits)
	for i in find_all_node_topic_by_node_url_name("begin"):
		print i.last_reply_time

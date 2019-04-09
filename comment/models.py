import threading #引入多线程的库
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render

class SendMail(threading.Thread): #使用多线程异步发送邮件，简单，实现快
	def __init__(self, subject, text, email, fail_silently=False):
		self.subject = subject
		self.text = text
		self.email = email
		self.fail_silently = fail_silently
		threading.Thread.__init__(self)
	def run(self):
		send_mail(
			self.subject, 
			self.text, 
			settings.EMAIL_HOST_USER, 
			[self.email], 
			fail_silently=self.fail_silently,
			html_message= self.text
		)


# Create your models here.
class Comment(models.Model):
		content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
		object_id = models.PositiveIntegerField()
		content_object = GenericForeignKey('content_type', 'object_id')

		text = models.TextField()
		comment_time = models.DateTimeField(auto_now_add=True)
		user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)#这条评论是谁写的

		root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)#获取一个评论下的所有评论
		parent = models.ForeignKey('self',related_name='parent_comment', null=True, on_delete=models.CASCADE)
		reply_to = models.ForeignKey(User,related_name="replies", null=True, on_delete=models.CASCADE)#回复谁

		def send_mail(self):
			#发送邮件通知
			if self.parent is None:
				#评论我的博客
				subject = '有人评论你的博客'
				email = self.content_object.get_email()
			else:
				#回复评论
				subject = '有人回复你的评论'
				email = self.reply_to.email
			if email != '': 
				context = {}
				context['comment_text'] = self.text
				context['url'] = self.content_object.get_url()
				text = render(None, 'comment/send_mail.html', context).content.decode('utf-8')
				send_mail = SendMail(subject, text, email)
				send_mail.start() #启用多线程
				

		def __str__(self):
			return self.text
		class Meta:
			ordering = ['comment_time']


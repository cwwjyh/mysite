from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class LikeCount(models.Model):#创建点赞的总数
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	liked_num = models.IntegerField(default=0)#记录已点赞的数量，设置默认值为0

#谁对哪个对象进行点赞
class LikeRecord(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	user = models.ForeignKey(User, on_delete=models.CASCADE)#这条评论是谁点的赞
	liked_time = models.DateTimeField(auto_now_add=True)#获取点赞的日期

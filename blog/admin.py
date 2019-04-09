from django.contrib import admin
from.models import BlogType, Blog

@admin.register(BlogType)  #admin后台管理blogType的界面
class BlogTypeAdmin(admin.ModelAdmin):
	list_display = ('id','type_name')

@admin.register(Blog) #admin后台管理blog的界面
class BlogAdmin(admin.ModelAdmin):
	list_display = ('id','title','blog_type','author','get_read_num','created_time','last_updated_time')
'''
@admin.register(ReadNum) #admin后台管理的界面
class ReadNumAdmin(admin.ModelAdmin):
	list_display = ('read_num','blog')
'''
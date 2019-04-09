from django.contrib import admin
from .models import ReadNum, ReadDetail

@admin.register(ReadNum) #admin后台管理的界面
class ReadNumAdmin(admin.ModelAdmin):
	list_display = ('read_num','content_object')

@admin.register(ReadDetail) #admin后台管理的界面
class ReadDetailAdmin(admin.ModelAdmin):
	list_display = ('date','read_num','content_object')

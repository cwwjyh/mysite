from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator  #导入分页器
from django.conf import settings
from django.db.models import Count #views.py处理请求的页面
from django.contrib.contenttypes.models import ContentType
from.models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read
from user.forms import LoginForm


def get_blog_list_common_date(request, blogs_all_list):
	paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) #每2篇进行换行（实例化：具体如何分页）
	page_num = request.GET.get('page', 1) #获取页码参数（GET请求）
	page_of_blogs = paginator.get_page(page_num) #如果输入的是不合法字符默认显示第一页
	currentr_page_num = page_of_blogs.number #获取当前页面
	#获取当前页面，前后各2页的页码范围
	page_range = list(range(max(currentr_page_num -2, 1), currentr_page_num))+ \
				 list(range(currentr_page_num,min(currentr_page_num +2, paginator.num_pages) +1))
	#加上省略页码标记
	if page_range[0] - 1 >=2:
		page_range.insert(0,'...')
	if paginator.num_pages - page_range[-1] >=2:
		page_range.append('...')
	#加上首页和尾页
	if page_range[0]!=1:
		page_range.insert(0, 1)
	if page_range[-1]!=paginator.num_pages:
		page_range.append(paginator.num_pages)



	#获取日期归档对应的博客数量
	blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
	blog_dates_dict={}
	for blog_date in blog_dates:
		blog_count = Blog.objects.filter(created_time__year=blog_date.year,
										created_time__month=blog_date.month).count()
		blog_dates_dict[blog_date] = blog_count


	context = {}
	context['blogs'] = page_of_blogs.object_list
	context['page_of_blogs'] = page_of_blogs
	context['page_range'] = page_range
	context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
	context['blog_dates'] = blog_dates_dict  #传入参数
	return context

def blog_list(request): #访问blog列表，请求获得对应的变量
	blogs_all_list = Blog.objects.all()  #views.py处理请求
	context = get_blog_list_common_date(request, blogs_all_list)
	return render(request,'blog/blog_list.html',context)  #输出结果导向

def blogs_with_type(request, blog_type_pk):

	blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
	blogs_all_list = Blog.objects.filter(blog_type=blog_type)
	context = get_blog_list_common_date(request, blogs_all_list)
	context['blog_type'] = blog_type  #传入blog_type变量
	return render(request,'blog/blogs_with_type.html', context)

def blogs_with_date(request, year,month):

	blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
	context = get_blog_list_common_date(request, blogs_all_list)
	context['blogs_with_date'] = '%s年%s月' % (year, month)
	return render(request,'blog/blogs_with_date.html', context)

def blog_detail(request, blog_pk):  #显示具体的blog界面
	blog = get_object_or_404(Blog, pk=blog_pk)  #pk是主键
	read_cookie_key = read_statistics_once_read(request, blog)
	
	context = {}
	context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()#当前打开博客时间的前一天；__gt是两个英文的下划线，少了出错
	context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()#当前打开博客时间的后一天
	context['blog'] = blog #当前打开的博客_p

	response =  render(request, 'blog/blog_detail.html',context)
	response.set_cookie(read_cookie_key, 'true' )#阅读cookie标记
	return response
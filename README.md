# DatabaseSystemForE-commerce
Our project for Database Concept course (2018). 
Instructor: Prof. Yin. Team members: Siqi Jiang, Kunshen Liu, Daren Chao

### 新建对象

	Person.objects.create(name=name,age=age)

	p = Person(name="WZ", age=23)
	p.save()

	p = Person(name="TWZ")
	p.age = 23
	p.save()

	Person.objects.get_or_create(name="WZT", age=23)
	这种方法是防止重复很好的方法，但是速度要相对慢些
	返回一个元组，第一个为Person对象，第二个为True或False, 新建时返回的是True, 已经存在时返回False

### 获取对象

	Person.objects.all() # 查询所有
	Person.objects.all()[:10] 切片操作，获取10个人，不支持负索引，切片可以节约内存，不支持负索引，后面有相应解决办法，第7条
	Person.objects.get(name="WeizhongTu") # 名称为 WeizhongTu 的一条，多条会报错
 
	get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter
	Person.objects.filter(name="abc") # 等于Person.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人
	Person.objects.filter(name__iexact="abc") # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件
 
	Person.objects.filter(name__contains="abc") # 名称中包含 "abc"的人
	Person.objects.filter(name__icontains="abc") #名称中包含 "abc"，且abc不区分大小写
 
	Person.objects.filter(name__regex="^abc") # 正则表达式查询
	Person.objects.filter(name__iregex="^abc")# 正则表达式不区分大小写
 
	filter是找出满足条件的，当然也有排除符合某条件的
	Person.objects.exclude(name__contains="WZ") # 排除包含 WZ 的Person对象
	Person.objects.filter(name__contains="abc").exclude(age=23) # 找出名称含有abc, 但是排除年龄是23岁的

	values可以返回类似字典格式的结果
	Author.objects.values('name', 'qq')

### 删除对象

	Person.objects.filter(name__contains="abc").delete() # 删除 名称中包含 "abc"的人
 
	如果写成 
	people = Person.objects.filter(name__contains="abc")
	people.delete()
	效果也是一样的，Django实际只执行一条 SQL 语句。

### 更新对象

	Person.objects.filter(name__contains="abc").update(name='xxx') # 名称中包含 "abc"的人 都改成 xxx

	twz = Author.objects.get(name="WeizhongTu")
	twz.name="WeizhongTu"
	twz.email="tuweizhong@163.com"
	twz.save()  # 最后不要忘了保存！！！

### 查询操作

	Author.objects.all().order_by('name')
	Author.objects.all().order_by('-name') # 在 column name 前加一个负号，可以实现倒序

	Person.objects.all().reverse()[:2] # 最后两条
	Person.objects.all().reverse()[0] # 最后一条

	qs = qs1 | qs2 | qs3 # 合并

	qs = qs.distinct() # 去重方法

	tags = Tag.objects.all().extra(select={'tag_name': 'name'}) # 别名
	tags[0].tag_name 

	Article.objects.all().defer('content') # 排除不需要的字段
	Author.objects.all().only('name') # 仅选择需要的字段

	 Author.objects.raw('select name from blog_author limit 1') # 嵌入原生SQL

### 聚合操作

	from django.db.models import Count, Avg, Sum
	Article.objects.all().values('author_id').annotate(count=Count('author')).values('author_id', 'count')
	Article.objects.all().values('author_id').annotate(avg_score=Avg('score')).values('author_id', 'avg_score')
	Article.objects.all().values('author__name').annotate(sum_score=Sum('score')).values('author__name', 'sum_score')

### 连接操作

	针对一对一或者多对一关系，使用 select_related 简化查询，其实使用了 JOIN 操作
	articles = Article.objects.all().select_related('author')[:10]
	
	针对一对多或者多对多关系，使用 prefetch_related 简化查询，也是使用了 JOIN 操作
	articles = Article.objects.all().prefetch_related('tags')[:10]

### 数据导入导出

	python manage.py loaddata blog_dump.json # 导入
	python manage.py dumpdata [appname] > appname_data.json # 导出

## 用户注册系统

这里我们使用了 Django 自带的标准权限管理系统 auth 模块,可以提供用户身份认证, 用户组和权限管理。

其关系模式定义为：

	CREATE TABLE "auth_user" (
	    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	    "password" varchar(128) NOT NULL, "last_login" datetime NULL, 
	    "is_superuser" bool NOT NULL, 
	    "first_name" varchar(30) NOT NULL, 
	    "last_name" varchar(30) NOT NULL,
	    "email" varchar(254) NOT NULL, 
	    "is_staff" bool NOT NULL, 
	    "is_active" bool NOT NULL,
	    "date_joined" datetime NOT NULL,
	    "username" varchar(30) NOT NULL UNIQUE
	)

创建用户：

	from django.contrib.auth.models import User

	user = User.objects.create_user(username, email, password)
	user.save()

认证用户：

	from django.contrib.auth import authenticate, login

	user = authenticate(username=username, password=password)
	if user is not None and user.is_active:
		login(request, user)	
		
修改密码：

	from django.contrib.auth import authenticate
	
	user = authenticate(username=username, password=password)
	if user is not None and user.is_active:
		user.set_password(new_password)
    	user.save()

退出登录：

	from django.contrib.auth import logout
	
	def logout_view(request):
    	logout(request)

权限判断：

	from django.contrib.auth.decorators import login_required

	@login_required(login_url='/accounts/login/')
	def my_view(request):
	    ...
	
	# 或者使用
	if req.user.is_authenticated:
		...


## 使用 Profile 扩展 User 模块

在 models.py 中加入 UserProfile 类：

	class UserProfile(models.Model):
    	user = models.OneToOneField(User)
		...

修改 setting.py 中的值：

	AUTH_PROFILE_MODULE = 'profiles.UserProfile'

最后可以这样使用 UserProfile：

	User.objects.all()[0].userprofile

## 使用 forms 组件

类似于 models，包含许多的 fields

自定义验证规则：

	from django.core.validators import RegexValidator

	class MyForm(Form):
    	user = fields.CharField(
	        validators=[RegexValidator(r'^[0-9]+$', '请输入数字'), RegexValidator(r'^159[0-9]+$', '数字必须以159开头')],
	    )

## 注

1. 由于{% csrf_token %}的存在，容易发生 Forbidden (403) 错误，解决方法是：

	在 setting.py 中找到中间件 MIDDLEWARE 删去其中的 'django.middleware.csrf.CsrfViewMiddleware'


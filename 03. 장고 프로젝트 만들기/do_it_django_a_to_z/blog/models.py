from django.db import models
from django.contrib.auth.models import User
import os

# 카테고리 모델 직접 구현
class Category(models.Model) :
    # 각 카테고리의 이름을 담는 필드, unique = True로 설정하면 동일한 name의 카테고리는 생성 불가능
    name = models.CharField(max_length = 50, unique = True)
    # 읽기 쉬운 텍스트로 고유 url을 만들고 싶을 때 사용하는 필드, allow_unicode = True면 한글로도 만들 수 있음
    slug = models.SlugField(max_length = 200, unique = True, allow_unicode = True)
    
    def __str__(self) :
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
    
    class Meta :
        verbose_name_plural = 'Categories'

# 태그 모델
class Tag(models.Model) :
    name = models.CharField(max_length = 50, unique = True)
    slug = models.SlugField(max_length = 200, unique = True, allow_unicode = True)
    
    def __str__(self) :
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

# Create your models here.
class Post(models.Model) :
    title = models.CharField(max_length = 30)
    hook_text = models.CharField(max_length = 100, blank = True)
    content = models.TextField()
    
    head_imag = models.ImageField(upload_to = 'blog/images/%Y/%m/%d/', blank = True)
    file_upload = models.FileField(upload_to = 'blog/files/%Y/%m/%d/', blank = True)
    
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    
    author = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    
    category = models.ForeignKey(Category, null = True, blank = True, on_delete = models.SET_NULL)

    tag = models.ManyToManyField(Tag, blank = True)
    
    def __str__(self) :
        return f'[{self.pk}]{self.title} :: {self.author}'
    
    def get_absolute_url(self) :
        return f'/blog/{self.pk}/'
    
    def get_file_name(self) :
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self) :
        return self.get_file_name().split('.')[-1]
from django.contrib import admin
from blog.models import Category, Post, PostImage, PostFile
# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostFile)
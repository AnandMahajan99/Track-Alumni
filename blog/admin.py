from django.contrib import admin
from .models import BlogPost, PostComment, Category

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(PostComment)
admin.site.register(Category)
# admin.site.register(SubCategory)

from django.db import models
from django.urls import reverse
from django.utils import timezone
from track_alumni.models import AlumniDetails
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    Category_name = models.CharField(max_length=100, unique=True)
    Thumbnail = models.ImageField(upload_to="blog/images/category/")
    Text = models.TextField()

    class Meta:
        ordering = ('Category_name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.Category_name

# class SubCategory(models.Model):
#     Category = models.ForeignKey(Category, related_name='sub_category', on_delete=models.CASCADE)
#     Sub_category_name = models.CharField(max_length=100)
#     Thumbnail = models.ImageField(upload_to="blog/images/subcategory/")
#     Text = models.TextField()
#
#     def __str__(self):
#         return self.Sub_category_name

class BlogPost(models.Model):
    Blogpost_id = models.AutoField(primary_key=True)
    Author = models.ForeignKey(AlumniDetails, on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, related_name='category_post', on_delete=models.CASCADE)
    Title = models.CharField(max_length=200)
    Body = RichTextField(blank=True, null=True)
    # Sub_category = models.ForeignKey(SubCategory, related_name='sub_category_post', on_delete=models.CASCADE)
    # Thumbnail = models.ImageField(upload_to="blog/images/post/", default="")
    # body = RichTextField(blank=True, null=True)
    # Heading  = models.CharField(max_length=200)
    # Slug = models.SlugField(max_length=200, unique=True)
    # Heading_text = models.TextField(max_length=5000)
    # Sub_heading1  = models.CharField(max_length=200, null=True, blank=True, default="")
    # Sub_heading1_text  = models.TextField(null=True, blank=True, default="")
    # Sub_heading2  = models.CharField(max_length=200,null=True, blank=True, default="")
    # Sub_heading2_text  = models.TextField(null=True, blank=True, default="")
    Created_datetime = models.DateTimeField(default=timezone.now)
    Published_datetime = models.DateTimeField(blank=True,null=True)

    class Meta:
        ordering = ('Created_datetime',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def publish(self):
        self.Published_datetime = timezone.now()
        print(self.Published_datetime)
        self.save()

    def get_absolute_url(self):
        return reverse("draft_list")

    def comment(self):
        return self.postcomments.all()

    def __str__(self):
        return str(self.Author)

class PostComment(models.Model):
    Post = models.ForeignKey(BlogPost, related_name='postcomments', on_delete=models.CASCADE)
    Comment_author = models.ForeignKey(AlumniDetails, on_delete=models.CASCADE)
    Text = models.TextField()
    Created_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Text

    class Meta:
        ordering = ('Created_datetime',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

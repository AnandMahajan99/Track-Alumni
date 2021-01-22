from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator

# Create your models here.

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

# student details present on college/university database
class StudentDetails(models.Model):
    Enrollment_no = models.CharField(max_length=30, primary_key=True)
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    Phone = models.CharField(max_length=10, unique=True, validators=[RegexValidator('^[6-9]{1}[0-9]{9}$','Enter a valid mobile number')])
    EmailId = models.EmailField(max_length=100)
    _12th_marks = models.FloatField()
    CGPA = models.FloatField()
    aadharno = models.CharField(max_length=12, unique=True, validators=[RegexValidator('^[0-9]{12}$','Enter Valid aadhar number')])

    def __str__(self):
        return self.Enrollment_no

# alumni details that join us
class AlumniDetails(models.Model):
    Enrollment_no = models.OneToOneField(StudentDetails, on_delete=models.CASCADE, primary_key=True)
    EmailId = models.EmailField(max_length=100, unique=True)
    Password = models.CharField(max_length=256)
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Phone = models.CharField(max_length=15, unique=True, validators=[RegexValidator('^[6-9]{1}[0-9]{9}$','Enter a valid mobile number')])
    #FullAddress = models.CharField(max_length=200)
    JoiningDateTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.EmailId

# Groups created details
class Group(models.Model):
    GroupId = models.AutoField(primary_key=True)
    Group_Name = models.CharField(max_length=200)
    Created_by = models.ForeignKey(AlumniDetails, on_delete=models.CASCADE)
    GroupCreateDateTime = models.DateTimeField(default=timezone.now)

    def post(self):
        p = self.posts.all()
        return self.posts.order_by('-PostCreateDateTime')

    def members(self):
        return self.member.all()

    def __str__(self):
        return self.Group_Name

# members of the group
class GroupMember(models.Model):
    GroupId = models.ForeignKey(Group, related_name='member', on_delete=models.CASCADE)
    MemberId = models.ForeignKey(AlumniDetails, related_name='memberid', on_delete=models.CASCADE)

    def __str__(self):
        return self.GroupId.Group_Name

# group's post
class Post(models.Model):
    PostId = models.AutoField(primary_key=True)
    HeadingText = models.CharField(max_length=200)
    Thumbnail = models.ImageField(upload_to="track_alumni/images/", default="")
    Created_by = models.ForeignKey(AlumniDetails, on_delete=models.CASCADE)
    GroupId  = models.ForeignKey(Group,  related_name='posts', on_delete=models.CASCADE)
    PostCreateDateTime = models.DateTimeField(default=timezone.now)
    #Comments = models.ForeignKey(Comment, on_delete=CASCADE)

    def comments(self):
        return self.comments.all()

    def __str__(self):
        return self.HeadingText

# comments on grouppost
class Comment(models.Model):
    CommentId = models.AutoField(primary_key=True)
    PostId = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    Comment = models.TextField()
    Created_by = models.ForeignKey(AlumniDetails, on_delete=models.CASCADE)
    DateTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Comment


class Request(models.Model):
    RequestId = models.AutoField(primary_key=True)
    AlumniId = models.ForeignKey(AlumniDetails, related_name='request_to', on_delete=models.CASCADE)
    SendBy = models.ForeignKey(AlumniDetails, related_name='request_by', on_delete=models.CASCADE)
    GroupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    DateTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.SendBy)

# contact us details
class Contact(models.Model):
    Text = models.TextField()
    Name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=100)
    Subject = models.CharField(max_length=100)
    DateTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Text

# posts on main page
class AdminPost(models.Model):
    PostId = models.AutoField(primary_key=True)
    Created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    Heading = models.CharField(max_length=200)
    Thumbnail = models.ImageField(upload_to="track_alumni/images/")
    Text = models.TextField()
    CreatedDateTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Text

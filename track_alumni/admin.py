from django.contrib import admin
from django.contrib.auth.models import Group
# from track_alumni.forms import ContactForm
admin.site.unregister(Group)

from  track_alumni.models import StudentDetails, AlumniDetails, Group, GroupMember, Post, Comment, Contact, Request, AdminPost

admin.site.site_title = 'Reunion'
admin.site.site_header = 'Reunion Administration'

@admin.register(AlumniDetails)
class AlumniDetailsAdmin(admin.ModelAdmin):
    list_display = ('Enrollment_no','First_Name','Last_Name','EmailId')


class PostAdmin(admin.ModelAdmin):
    list_display = ('HeadingText','GroupId','Created_by')
    list_filter = ('Created_by',)

class StudentDetailsAdmin(admin.ModelAdmin):
    list_display = ('Enrollment_no','First_Name','Last_Name','EmailId')
    radio_fields = {'Gender':admin.VERTICAL}

class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('GroupId','MemberId')
    list_filter = ('GroupId',)
    search_fields = ('GroupId__Group_Name','MemberId__EmailId')

# Register your models here.
# admin.site.register(AlumniDetails)
admin.site.register(AdminPost)
admin.site.register(StudentDetails, StudentDetailsAdmin)
admin.site.register(Group)
admin.site.register(GroupMember, GroupMemberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Request)

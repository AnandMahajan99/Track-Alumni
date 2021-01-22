from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import send_mail
import bcrypt
from .models import StudentDetails, AlumniDetails, Group, Post, Comment, GroupMember, Contact, Request, AdminPost
from Major import settings


# Create your views here.

def index(request):
    p = 'Anand@1234'
    passwd = p.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd,bcrypt.gensalt())
    print(salt)
    print(hashed)
    # print(bcrypt.hashpw(b'anand',hashed))
    # if bcrypt.checkpw(passwd,hashed):
    #     print('match')
    # else:
    #     print('not match')
    post = AdminPost.objects.all().order_by('-CreatedDateTime')
    return render(request, 'track_alumni/index.html', {'post': post})

def register(request):
    if request.method=="POST":
        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        email = request.POST.get('email','')
        passwd = request.POST.get('password','')
        password = passwd.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password,salt)
        cpassword = request.POST.get('cpassword','')
        # address = request.POST.get('address','')
        # city = request.POST.get('city','')
        # state = request.POST.get('state','')
        phone = request.POST.get('phone','')
        enrollno = request.POST.get('enrollno','')
        aadharno = request.POST.get('aadhar','')
        # marks12th = request.POST.get('12marks','')
        # cgpa = request.POST.get('cgpa','')
        if AlumniDetails.objects.filter(Enrollment_no=enrollno):
            messages.info(request, 'Alumni with this information already exist')
        elif StudentDetails.objects.filter(Enrollment_no=enrollno, aadharno=aadharno):
            details = AlumniDetails(
                Enrollment_no_id = enrollno,
                EmailId = email,
                Password = hashed,
                First_Name = fname,
                Last_Name = lname,
                Phone = phone,
                #FullAddress = address+city+state
            )
            details.save()
            # print('2')
            # subject = 'Greetings'
            # msg = 'Thanks '+fname+' '+lname+' for Registering on our Website'
            # response = send_mail(subject, msg, settings.EMAIL_HOST_USER, [email])
            # if response == 1:
            #     print('Mail Sent Successfully')
            # else:
            #     print('Mail could not Sent')

            messages.info(request, 'You are Successfully Registered')
            return redirect("login")
        else:
            messages.info(request, 'Entered Information is not matching with any Student Details')
            # print('3')
        return redirect("register")
    return render(request, 'track_alumni/register.html')

def login(request):
    msg = ''
    if request.method=='POST':
        userid = request.POST.get('userid','')
        password = request.POST.get('pass','').encode('utf-8')
        try:
            user = AlumniDetails.objects.get(EmailId=userid)
            db_password = user.Password[2:len(user.Password)-1]

            if str(bcrypt.hashpw(password, db_password.encode('utf-8'))) == user.Password:
                print('hello')
                request.session['user'] = str(user.Enrollment_no)
                request.session['username'] = user.First_Name+ ' '+user.Last_Name
                request.session.get_expire_at_browser_close()
                messages.success(request, 'Login Successfull', extra_tags='login_success')
            return redirect('/')
        except ObjectDoesNotExist :
            msg = 'Login Unsuccessfull'
    return render(request,'track_alumni/login.html',{'msg': msg})

def logout(request):
    if 'user' in request.session:
        del request.session['user']
        request.session.flush()
        return redirect('/')
    msg = {'msg':'User Does\'nt Logged in'}
    return render(request, 'track_alumni/index.html',msg)

def post(request):
    if 'user' in request.session:
        group = []
        id = str(request.session['user'])
        i = Post.objects.filter()
        for p in GroupMember.objects.filter(MemberId=id):
            post = p.GroupId.post()
            group.append([post])
        params = {'group': group}
        return render(request, 'track_alumni/post.html', params)
    return redirect('/login/')

def group(request):
    if 'user' in request.session:
        id = str(request.session['user'])
        group = GroupMember.objects.filter(MemberId=id).order_by('GroupId__Group_Name')
        params = {'group': group,'id':id}
        return render(request, 'track_alumni/group.html', params)
    return redirect('/login/')

def groupview(request,id):
    if 'user' in request.session:
        name = ''
        if get_object_or_404(GroupMember, GroupId=id, MemberId=request.session['user']):
            pass
        if get_object_or_404(Group, GroupId=id):
            #g = Group.objects.get(GroupId=id)
            #print(g.post())
            posts = Post.objects.filter(GroupId=id).order_by('-PostCreateDateTime')
            member = GroupMember.objects.filter(GroupId=id)
            for i in member:
                name = i.GroupId.Group_Name
                break
            params = {'posts':posts,'name':name ,'id':id,'members':member}
            return render(request, 'track_alumni/grouppost.html',params)
    return redirect('/login/')

def comment(request,id):
    if 'user' in request.session:
        post = ''
        # try:
        #     post = Post.objects.get(PostId=id)
        # except ObjectDoesNotExist:
        #     return redirect('/')
        post = get_object_or_404(Post, PostId=id)
        if request.method == 'POST':
            userid = str(request.session['user'])
            comment = request.POST.get('comment','')
            print(comment)
            newcomment  = Comment(
                Comment = comment,
                PostId_id = id,
                Created_by_id = userid
            )
            newcomment.save()
        return render(request, 'track_alumni/comment.html',{'post':post})
    return redirect('/')

def create_new_group(request):
    if 'user' in request.session:
        id = str(request.session['user'])
        if request.method == 'POST':
            groupname = request.POST.get('groupname','')
            if Group.objects.filter(Group_Name=groupname, Created_by_id=id):
                print('Group With this name Created By You Already Exist')
            else:
                group = Group(
                    Group_Name = groupname,
                    Created_by_id = id
                )
                group.save()

                groupid = Group.objects.get(Group_Name=groupname, Created_by_id=id)
                groupmember = GroupMember(
                    GroupId_id = groupid.GroupId,
                    MemberId_id = id
                )
                groupmember.save()
                messages.success(request, 'Group Created Successfully', extra_tags='create_group_success')
                return redirect('add_member', gid=groupid.GroupId)
        messages.info(request, 'Group Already Exist', extra_tags='warn')
        return redirect('group')
    return redirect('login')

def delete_group(request, gid):
    if 'user' in request.session:
        id = str(request.session['user'])
        group = get_object_or_404(Group, GroupId=gid, Created_by_id=id)
        group.delete()
        messages.info(request,'Group Deleted Successfully', extra_tags='delete')
        return redirect('group')
    return redirect('/')

def add_group_member(request, gid):
    if 'user' in request.session:
        group = Group.objects.get(GroupId=gid)
        existing_members = []
        temp = list(group.members())
        for item in temp:
            existing_members.append(item.MemberId_id)
        req_already_send = []
        temp = list(Request.objects.filter(GroupId_id=gid))
        for item in temp:
            req_already_send.append(item.AlumniId_id)
        alumni = AlumniDetails.objects.all().exclude(Enrollment_no__in = existing_members + req_already_send)
        return render(request, 'track_alumni/add_group_member.html', {'group':group,'alumni':alumni})
    return redirect('/')

def delete_group_member(request):
    if 'user' in request.session:
        pass
    return redirect('/')

def exit_group(request, gid):
    if 'user' in request.session:
        group_member = get_object_or_404(GroupMember, GroupId_id=gid, MemberId_id=request.session['user'])
        group_member.delete()
        return redirect('group')
    return redirect('/')

def create_new_post(request,gid):
    if 'user' in request.session:
        id = request.session['user']
        if request.method == 'POST':
            Heading = request.POST.get('head','')
            Thumb = request.FILES.get('thumb','')
            post = Post(
                HeadingText = Heading,
                Thumbnail = Thumb,
                GroupId_id = gid,
                Created_by_id = id
            )
            post.save()
            messages.info(request, "Your Post is created")
            return redirect('groupview', id=gid)
        return render(request, 'track_alumni/post_form.html',{'gid':gid})
    return redirect('/')

def send_request(request,gid,id):
    if 'user' in request.session:
        req = Request(
            AlumniId_id = id,
            SendBy_id = request.session['user'],
            GroupId_id = gid
        )
        req.save()
        return redirect('add_member', gid=gid)
    return redirect('/')

def request_and_notifications(request):
    if 'user' in request.session:
        req = Request.objects.filter(AlumniId=request.session['user'])
        return render(request, 'track_alumni/request_and_notifications.html',{'req':req})
    return request('/')

def approve_join_group_request(request,rid):
    if 'user' in request.session:
        req = get_object_or_404(Request, RequestId=rid, AlumniId_id=request.session['user'])
        add_member = GroupMember(
            GroupId_id = req.GroupId_id,
            MemberId_id = req.AlumniId_id
        )
        add_member.save()
        req.delete()
        return redirect('request_and_notifications')
    return redirect('/')

def delete_join_group_request(request,rid):
    if 'user' in request.session:
        req = get_object_or_404(Request, RequestId=rid, AlumniId_id=request.session['user'])
        req.delete()
        return redirect('request_and_notifications')
    return redirect('/')

def view_profile(request):
    if 'user' in request.session:
        groups_created = Group.objects.filter(Created_by_id=request.session['user']).count()
        groups_joined = GroupMember.objects.filter(MemberId_id=request.session['user']).count()
        post = Post.objects.filter(Created_by_id=request.session['user']).count()
        return render(request, 'track_alumni/view_profile.html',{'groups_created':groups_created, 'groups_joined':groups_joined, 'post':post})
    return redirect('/')

def about(request):
    return render(request, 'track_alumni/about.html')

def contact(request):
    if request.method == 'POST':
        text = request.POST['message']
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']

        contact = Contact(
            Text = text,
            Name = name,
            Email = email,
            Subject = subject
        )
        contact.save()
        return HttpResponse('Hello')
    return render(request, 'track_alumni/contact.html')









# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/comment_form.html', {'form':form})
#
# def newpost(request,id):
#     return redirect('/')



# try:
        #     group = Group.objects.get(GroupId=gid, Created_by_id=id)
        #     group.delete()
        #     messages.info(request,'Group Deleted Successfully', extra_tags='delete')
        # except ObjectDoesNotExist:
        #     messages.warning(request,'Either Group Does Not Exist OR You Are Not Admin', extra_tags='warn')



#
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.core.mail import send_mail
# from email_project import settings
#
# # Create your views here.
#
# def index(request):
#     return render(request, 'emailapp/index.html')
#
# def mail(request):
#     subject = 'Greetings'
#     msg = 'Thanks for Registering'
#     to = 'mahajan.anand27@gmail.com'
#     response = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
#     if response == 1:
#         msg = 'Mail Sent'
#     else:
#         msg = 'Mail Not Sent'
#     return render(request, 'emailapp/success.html',{'msg':msg})

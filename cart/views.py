from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .models import *
from django.contrib.auth.hashers import check_password
from django.db.models import Count
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404


def home(request,n): 
    if request.user.is_authenticated:
        pp = projects.objects.all()
        pp = pp.annotate(like_count=Count('likes'))
        p = pp.order_by('-like_count')
        # com=comments.objects.filter(parent=None)
        # print(com)
        new=projects.objects.order_by('-date')
        na = new.annotate(like_count=Count('likes'))
        # na = new.order_by('-like_count')
        pr={'projs':p,'na':na}
        return render(request,'home.html',pr)
    else:
        return redirect('/')

def login_page(request):
    if request.method=='POST':
        n=request.POST.get('name')
        p=request.POST.get('pass')
        user=authenticate(username=n,password=p)
        if user is not None:
            login(request,user)
            messages.success(request,'Logedin successfully.')
            return redirect(f'/home/{n}')
        else:
            messages.info(request,'Invalid credentials.')
            return redirect('/login')

    return render(request,'login.html') 

def email(request):   
    if request.method=='POST':
        n1=str(request.POST.get('n1'))
        n2=str(request.POST.get('n2'))
        n3=str(request.POST.get('n3'))
        n4=str(request.POST.get('n4'))
        n5=str(request.POST.get('n5'))
        n6=str(request.POST.get('n6'))
        n=request.POST.get('n')
        e=request.POST.get('e')
        p=request.POST.get('p')
        otp=request.POST.get('otp')
        uotp=n1+n2+n3+n4+n5+n6
        # print(uotp,n,e,p,otp,uotp,end=" ")
        if otp==uotp:
            user=User.objects.create_user(username=n,email=e,password=p)
            user.save()
            u=full_user.objects.create(s=n,college=".",sem=".",photo="user_imgs/user.png",bio=".",github=".")
            u.save()
            login(request,user)            
            messages.success(request,'Logedin successfully.')
            return redirect(f'/home/{request.user}')
        else: 
            messages.success(request,'Invalid OTP.')              
            return redirect('/login') 
    return render(request,'email.html')    

def signin_page(request):
    if request.user.is_authenticated:    
        return redirect(f'/home/{request.user}')
    else:
        if  request.method=='POST':
            n=request.POST.get('name')
            e=request.POST.get('email')
            # b=request.POST.get('bio')
            p=request.POST.get('pass')
            cp=request.POST.get('cpass')
            sub_string="2GI"

            if p!=cp:
                messages.info(request,'password does not match')
                return redirect('/')
                
            elif User.objects.filter(username=n).exists():
                messages.info(request,'Username already taken')
                return redirect('/')
            
            elif User.objects.filter(email=e).exists():
                messages.info(request,'Email already taken')
                return redirect('/')
            elif sub_string not in e:
                messages.info(request,'Please use college email address')
                return redirect('/')
            
            else:
                otp=random.randint(100000,999999)
                subject = 'OTP for creating an account in ProjectVerse.'
                message = f'Hi {n}, thank you for registering in ProjectVerse. Your one time password is {otp}.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [e]
                send_mail( subject, message, email_from, recipient_list )

                messages.success(request,'An OTP is sent to your regestered email.')
                d={'name':n,'email':e,'password':p,'otp':otp}
                return render(request,'email.html',d)
        # print('doneeee')                
        return render(request,'signin.html')

def logout_page(request):
    logout(request)
    messages.success(request,'Loged out successfully.')
    return redirect('/login')



def add(request,n):
    if request.user.is_authenticated:    
        if request.method=='POST':
            pname=request.POST.get('pname')
            desc=request.POST.get('desc')
            domain=request.POST.get('dom')
            stack=request.POST.get('ts')
            guide=request.POST.get('guide')
            team_mems=request.POST.get('team_mems')
            team_usn=request.POST.get('team_usn')
            indus=request.POST.get('indus')
            usn=request.POST.get('usn')
            link=request.POST.get('link')
            # print(team_mems,team_usn,indus,usn,sep="--")
            strr=team_mems +"--"+ team_usn +"--"+ indus +"--"+ usn +"--"+ guide
            # print(str)
            image=request.FILES.get('img')
            na=request.user
            na=str(na)
            p=projects.objects.create(pname=pname,desc=desc,domain=domain,stack=stack,link=link,image=image,info=strr,stud=na)
            p.save()
            messages.success(request,'Project created successfully.')
            return redirect(f'/user_projects/{request.user}')
        else:    
            return render(request,'add.html')
    else:
        return redirect('/')    
def search(request):
    if request.method =='POST':
        s=request.POST.get('search')
        pr={'s':s}
        if len(s)<25:
            c=s[0:1]
            n=s[1:]
            if c == '@':
                profile=full_user.objects.none()
                pp=full_user.objects.filter(s__icontains=n)
                print(pp)
                if pp.count()!=0:
                    prof=pp[0].s
                    print(pp[0])
                    print(prof)
                    profile=pp[0]
                    p=projects.objects.filter(stud__icontains=prof)   
                else:
                    print("not found")
                    p=projects.objects.none()
                # pr['projs']=p
            elif c=='#':
                p=projects.objects.filter(pname__icontains=n)
                profile=full_user.objects.none()
                # pr['projs']=p
            else:
                # p1=projects.objects.filter(pname__icontains=s)
                profile=full_user.objects.none()
                p1=projects.objects.filter(desc__icontains=s)
                p2=projects.objects.filter(stack__icontains=s)
                p3=projects.objects.filter(domain__icontains=s)
                p=p1.union(p2,p3)       
        else:
            p=projects.objects.none()
    pr['projs']=p
    # print(profile.sem)                                  
    pr['profile']=profile                                  
    return render(request,'search.html',pr)

def project(request,n,p):
    # if request.user.is_authenticated:
    #     prr = get_object_or_404(projects, pname=p)
    #     wl=prr.likes.values('username')
    #     inf=prr.info
    #     inf_list=inf.split('--')
    #     guide=inf_list[4]
    #     typ="s"
    #     if inf_list[0] == '.':
    #         org=inf_list[2]
    #         usn=inf_list[3]
    #         typ='g'
    #     else:
    #         org=inf_list[0]
    #         usn=inf_list[1]    
    #     # print(pr)
    #     list=[]
    #     for i in wl:
    #         list.append(i['username'])
    #     ss=prr.stack
    #     stud=prr.stud
    #     rporjs=projects.objects.filter(stud=stud)
    #     l=ss.split(',')
    #     res=rporjs.exclude(pname=p)
    #     owner=full_user.objects.get(s=stud)
    #     com=comments.objects.filter(post=prr,parent=None)
    #     rep=comments.objects.filter(post=prr).exclude(parent=None)
    #     repdict={}
    #     for r in rep:
    #         if r.parent.id not in repdict.keys():
    #             repdict[r.parent.id]=[r]
    #         else:
    #             repdict[r.parent.id].append(r)
    #     pr={'projs':prr,'stacks':l,'rprojs':res,'owner':owner,'comments':com,'replies':repdict,'wl':list,'t':typ,'org':org,'usn':usn,'guide':guide}
    #     liked=False
    #     if prr.likes.filter(id=request.user.id).exists():
    #         liked = True
    #     pr['number_of_likes'] = prr.number_of_likes()
    #     pr['post_is_liked'] = liked         
    #     return render(request,'project.html',pr)
    # else:
    #     return redirect('/')
    if request.user.is_authenticated:    
        prr = get_object_or_404(projects, pname=p)
        wl = prr.likes.values('username')
        inf = prr.info
        inf_list = inf.split('--')
        guide = inf_list[4]
        typ = "s"
        if inf_list[0] == '.':
            org = inf_list[2]
            usn = inf_list[3]
            typ = 'g'
        else:
            org = inf_list[0]
            usn = inf_list[1]    
        list = []
        for i in wl[:10]:
            list.append(i['username'])

        ss = prr.stack
        stud = prr.stud
        rporjs = projects.objects.filter(stud=stud)
        l = ss.split(',')
        res = rporjs.exclude(pname=p)
        owner = full_user.objects.get(s=stud)
        com = comments.objects.filter(post=prr,parent=None)
        rep = comments.objects.filter(post=prr).exclude(parent=None)
        repdict = {}
        repcount = {}
        for r in rep:
            if r.parent.id not in repdict.keys():
                repdict[r.parent.id] = [r]
                repcount[r.parent.id] = 1
            else:
                repdict[r.parent.id].append(r)
                repcount[r.parent.id] += 1
        pr = {'projs':prr,'stacks':l,'rprojs':res,'owner':owner,'comments':com,'replies':repdict,'reply_count':repcount,'wl':list,'t':typ,'org':org,'usn':usn,'guide':guide}
        liked = False
        if prr.likes.filter(id=request.user.id).exists():
            liked = True
        pr['number_of_likes'] = prr.number_of_likes()
        pr['post_is_liked'] = liked         
        return render(request,'project.html',pr)
    else:
        return redirect('/')    

def user_projects(request,n):
    if request.user.is_authenticated:    

        if request.method == 'POST':
            bio=request.POST.get('bio')
            college=request.POST.get('c')
            sem=request.POST.get('sem')
            link=request.POST.get('link')
            photo=request.FILES.get('photo')
            u=full_user.objects.get(s=request.user)
            u.sem=sem
            u.college=college
            if photo and u.photo=="user_imgs/user.png":
                u.photo=photo
            elif photo and u.photo!="user_imgs/user.png":
                u.photo.delete()
                u.photo=photo
            else:
                if u.photo!='user_imgs/user.png':
                    u.photo.delete()
                u.photo='user_imgs/user.png'    
            u.bio=bio
            u.github=link
            u.save()
        p=projects.objects.filter(stud=str(request.user))
        uu=full_user.objects.get(s=str(request.user))
        projecs={'projs':p,'n':uu}
        return render(request,'user_projects.html',projecs)
    else:
        return redirect('/')

def manage_project(request,id):
    prr=projects.objects.get(id=id,stud=request.user)
    ss=prr.stack
    # stud=prr.stud
    rporjs=projects.objects.filter(stud=request.user)
    l=ss.split(',')
    # res=rporjs.exclude(id=id)
    owner=full_user.objects.get(s=request.user)
    pr={'projs':prr,'stacks':l,'rprojs':rporjs,'owner':owner}
    return render(request,'manae_project.html',pr)

def delete_project(request,id):
    if request.method == 'POST':
        p=request.POST.get('p')
        sir_p=request.POST.get('sir_p')
        user=User.objects.get(username=request.user)
        cp=user.password
        sp="gitPROJECTHUB"
        if check_password(p,cp) and sir_p==sp:
            dp=projects.objects.filter(stud=request.user)
            dp.get(id=id).delete()
            messages.success(request,'Project deleted successfully')
            return redirect(f'/user_projects/{request.user}')
        else:
            messages.info(request,'Invalid Password')
            return redirect(f'/manage_project/{id}')


def edit_project(request,id):
    if request.method == 'POST':
        pname=request.POST.get('pname')
        desc=request.POST.get('desc')
        domain=request.POST.get('dom')
        stack=request.POST.get('ts')
        link=request.POST.get('link')
        image=request.FILES.get('img')
        p=projects.objects.get(stud=request.user,id=id)
        p.pname=pname
        p.desc=desc
        p.domain=domain
        p.stack=stack
        p.link=link
        p.image.delete()
        p.image=image
        p.save()
        messages.success(request,'Project updated successfully')
        return redirect(f'/manage_project/{id}')
    pp=projects.objects.get(id=id,stud=request.user)
    send={'p':pp}
    return render(request,'edit_proj.html',send)

def post_c(request,id,n):
    if request.method == 'POST':
        comment=request.POST.get('comment')
        parentsno=request.POST.get('parentsno')
        u=full_user.objects.get(s=request.user)
        post=projects.objects.get(id=id)
        p=post.pname
        if parentsno=="":
            comments.objects.create(comment=comment,user=u,post=post)
            messages.success(request,"Comment posted successfully")

        else:
            parent=comments.objects.get(id=parentsno)
            comments.objects.create(comment=comment,user=u,post=post,parent=parent)
            messages.success(request,"Reply posted successfully")
        return redirect(f'/project/{request.user}/{p}')

def like_me(request):
    if request.method=="POST":
        pid=request.POST.get('proj_id')
    p=projects.objects.get(id=pid)
    pn=p.pname
    if p.likes.filter(id=request.user.id).exists():
        p.likes.remove(request.user)
        messages.success(request,"Post unliked successfully")
        return redirect(f'/project/{request.user}/{pn}')
    else:
        p.likes.add(request.user)
        messages.success(request,"Post liked successfully")
        return redirect(f'/project/{request.user}/{pn}') 
def change_password(request):
    if request.method=="POST":
        fm=PasswordChangeForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Password reset successfully")
            return redirect(f'/home/{request.user}')
    else: 
        fm=PasswordChangeForm(user=request.user)
    return render(request,'change_password.html',{'fm':fm})


def error_404(request, exception):
    # print(hh)
    return render(request, '404.html', status=404)

def error_500(request, exception):
    # print(hh)
    return render(request, '404.html', status=404)






# ?? please add if request.user to all the defs 

    
                   





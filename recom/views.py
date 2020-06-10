from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.views.generic.edit import CreateView, DeleteView

from recom import models as recom_models


# main page
def index(request):
    """index page"""
    ctx = {
    }

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user

        return render(request, 'index.html', ctx)
    else:
        return redirect('login')


# 채용정보 보여주기
def job_list(request):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')


    notice_list = recom_models.Notice.objects.raw('SELECT * FROM notice')


    list_elem_cnt = len(list(notice_list))
    page_cnt = int(list_elem_cnt / 24)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(notice_list, page_cnt)
    try:
        notices = paginator.page(page)
    except PageNotAnInteger:
        notices = paginator.page(1)
    except EmptyPage:
        notices = paginator.page(paginator.num_pages)

    ctx['notices'] = notices

    return render(request, 'job_list.html', ctx)

def calc_salary(sal):
    sal_str = ""

    ten_thousand = sal / 10000
    if ten_thousand / 10000 > 1:
        hund_million = ten_thousand / 10000
        sal_str = str(hund_million)
        sal_str += " 억"

    sal_str += str(round(ten_thousand))
    sal_str += " 만원"

    return sal_str

def job_detail(request, pk):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')

    try:
        notice = get_object_or_404(recom_models.Notice, pk=pk)
    except Notice.DoesNotExist:
        return HttpResponse("채용공고가 없습니다.")


    min_sal = int(notice.min_sal)
    max_sal = int(notice.max_sal)

    if max_sal is not None:
        max_sal_str = calc_salary(max_sal)
    else:
        max_sal_str = "정보없음"

    min_sal_str = calc_salary(min_sal)


    ctx['notice'] = notice
    salary_str = "연봉타입 : "
    salary_str += str(notice.sal_tp_nm)
    salary_str += '\n'
    salary_str += "최대연봉 : " + max_sal_str
    salary_str += '\n'
    salary_str += "최소연봉 : " + min_sal_str

    ctx['salary_str'] = salary_str

    # print(salary_str)

    return render(request, 'job_detail.html', ctx)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

import sys
import requests
import base64
import json
import logging
import pymysql
def interest(request):
    ctx = {}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')

    userid = User.objects.get(username=username).id
    
    ctx['user'] = User.objects.get(username=username)

    if recom_models.User.objects.filter(user_id=userid).exists():
        ctx['debug'] = 'Exists'
    else:
        ctx['debug'] = 'Does not exist'
        recom_models.User.objects.create(user_id=userid)

    dbuser = recom_models.User.objects.get(user_id=userid)
    

    host = "project.catth3zniejo.ap-northeast-2.rds.amazonaws.com"
    port = 3306
    username = "admin"
    password = "tkdghkd1!"
    database = "JobRecommendSystem"

    conn = pymysql.connect(host, user=username, passwd=password, db=database, \
    port=port, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    user_id = userid

    user_info = {}
    user_info.update(user_id = user_id)

    '''edu level'''
    if recom_models.UserSpec.objects.filter(user=dbuser).exists():
        query = "SET @spec_id = (SELECT user_spec_id FROM user AS u JOIN user_spec AS s ON u.user_id = s.user_id WHERE user_spec_id = {});".format(user_id)
        cursor.execute(query)
        query = "SELECT edu_level FROM user_spec WHERE user_spec_id = @spec_id;"
        cursor.execute(query)
        edu_level = cursor.fetchall()[0][0]
        ctx['edu'] = edu_level
        ctx['userspecexists'] = True

        dbuserspec = recom_models.UserSpec.objects.get(user=dbuser)

        if recom_models.UserCareer.objects.filter(user_spec=dbuserspec):

            '''career'''
            query1 = "SET @c_id = (SELECT career_id FROM user_career WHERE user_spec_id = @spec_id); "
            query2 = "SELECT career FROM career WHERE career_id = @c_id;"
            cursor.execute(query1)
            cursor.execute(query2)
            career = cursor.fetchall()[0][0]

            '''license'''
            query1 = "SELECT COUNT(*) FROM user_license WHERE user_spec_id = @spec_id;"
            cursor.execute(query1)
            num_license = cursor.fetchall()[0][0]
            query2 = "SELECT license_id FROM user_license WHERE user_spec_id = @spec_id;"
            cursor.execute(query2)
            license = list(cursor.fetchall())
            license_lst = []
            for i in range(num_license):
                query = "SELECT license FROM license WHERE license_id = {};".format(license[i][0])
                cursor.execute(query)
                license_lst.append(cursor.fetchall()[0][0])

            ctx['career'] = career
            ctx['license'] = license_lst
            ctx['usercarexists'] = True
        
        else:
            ctx['usercarexists'] = False
    else:
        ctx['userspecexists'] = False

    ctx['basic'] = recom_models.User.objects.get(user_id=userid)
    
    
    return render(request, 'interest.html', ctx)




from .forms import UserCareerForm
from django.contrib import messages
def CareerUpdate(request, pk):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        ctx['username'] = request.user.username
    else:
        return redirect('loginpage')

    post = recom_models.UserCareer.objects.get(user_spec_id=pk)

    if request.method == "GET":
        form = UserCareerForm(instance=post)
    elif request.method == "POST":
        form = UserCareerForm(request.POST, instance=post)
        if form.is_valid():
            # print(form.cleaned_data)
            post.career = (form.cleaned_data['career'])

            post.save()

            messages.success(request, '수정 성공.', extra_tags='alert')
            return redirect('interest')
        else:
            messages.warning(request, '모든 내용이 정확하게 입력되었는지 확인해주세요.', extra_tags='alert')

    ctx['form'] = form

    return render(request, 'edit_basic.html', ctx)


from django.views.generic.edit import UpdateView 
  
class BasicUpdate(UpdateView): 
    model = recom_models.User

    template_name = 'edit_basic.html'
  
    # specify the fields 
    
    fields = [ 
        "name", 
        "age",
        "region",
        "holiday_tp_nm",
        "min_sal"
    ] 
    
    success_url ="/"

class EduLevelUpdate(UpdateView):
    model = recom_models.UserSpec

    template_name = 'edit_edu.html'

    fields = [
        "edu_level"
    ]

    success_url = "/"

class EduLevelAdd(CreateView): 
    model = recom_models.UserSpec 
  
    template_name = 'add_edu.html'
  
    fields = ['edu_level'] 

    def form_valid(self, form):
        obj = form.save(commit=False)
        userid = User.objects.get(username=self.request.user.username).id
        obj.user_id = userid
        obj.user_spec_id = userid
        obj.save()

class CareerAdd(CreateView): 
    model = recom_models.UserCareer 
    template_name = 'add_career.html'
    fields = ['career'] 

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = recom_models.User.objects.get(user=self.request.user.id)
        userspec = recom_models.UserSpec.objects.get(user=user).user_spec_id
        obj.user_spec_id = userspec
        obj.save()

class LicenseAdd(CreateView):
    model = recom_models.UserLicense
    template_name = 'add_license.html'
    fields = ['license'] 

    def form_valid(self, form):
        obj = form.save(commit=False)
        userid = User.objects.get(username=self.request.user.username).id
        obj.user_id = userid
        obj.user_spec_id = userid
        obj.save()

class LicenseDelete(DeleteView):
    model = recom_models.UserLicense
    template_name = 'delete_license.html'
    
    success_url = '/'

    

def personal(request):
    ctx = {}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user

    username = 'Tom'
    info = recom_models.User.objects.filter(name=username)
    if info.exists():
        ctx['name'] = info
        loc = getattr(recom_models.User.objects.get(name=username), "location")
        day = getattr(recom_models.User.objects.get(name=username), "holiday_tp_nm")


    list = recom_models.Company.objects.raw('SELECT c.company_id, c.company, c.basic_addr, n.title, n.sal_tp_nm, n.max_sal, n.min_sal, n.holiday_tp_nm, n.min_edubg, n.career FROM company AS c JOIN notice AS n ON c.company_id = n.company_id JOIN user AS u ON c.region_id = (SELECT region_id FROM region WHERE %s = region) WHERE n.min_sal > 25000000 AND n.holiday_tp_nm = %s', [loc, day])
    ctx['list'] = list

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')


    return render(request, 'personalized.html', ctx)

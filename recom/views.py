from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect

from django.views.generic.edit import CreateView, DeleteView

from recom import models as recom_models
from datetime import datetime
from random import sample


# main page
def index(request):
    ctx = {
    }

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')

    notice_list = recom_models.Notice.objects.all()
    notice_cnt = notice_list.count()
    rand_ids = sample(range(1, notice_cnt), 4)
    rand_notice_list = recom_models.Notice.objects.filter(notice_id__in=rand_ids)

    ctx['notices'] = rand_notice_list


    # image list
    img_list = ["https://image.flaticon.com/icons/svg/65/65053.svg"]
    img_list.append("https://media.istockphoto.com/vectors/hiring-and-employees-icons-job-related-images-showing-hiring-vector-id1226249188")
    img_list.append("https://image.flaticon.com/icons/svg/942/942800.svg")
    img_list.append("https://image.flaticon.com/icons/svg/942/942799.svg")

    ctx['img_list'] = img_list

    return render(request, 'index.html', ctx)


def search(request):
    ctx = {
    }

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')


    # objects to be added to the filtering
    region_list = recom_models.Region.objects.all()
    category_list = recom_models.JobsCd.objects.raw('SELECT DISTINCT(jobs_cd) FROM notice')

    ctx['region_list'] = region_list
    ctx['category_list'] = category_list


    if request.method == 'POST':
        category = request.POST['category']
        region = request.POST['region']
        salary = request.POST['salary']

        if salary != "":
            salary_int = int(salary) * 10000



        if category != "None" and region != "None" and salary != "":
            notice_list = recom_models.Notice.objects.filter(jobs_cd__job_name = category, company__region__region = region, min_sal__gte=salary_int)

        elif category == "None" and region != "None" and salary != "":
            notice_list = recom_models.Notice.objects.filter(company__region__region = region, min_sal__gte=salary_int)

        elif region == "None" and category != "None" and salary != "":
            notice_list = recom_models.Notice.objects.filter(jobs_cd__job_name = category, min_sal__gte=salary_int)

        elif salary == "" and region != "None" and category != "None":
            notice_list = recom_models.Notice.objects.filter(jobs_cd__job_name = category, company__region__region = region)

        elif category != "None":
            notice_list = recom_models.Notice.objects.filter(company__region__region = region)

        elif region != "None":
            notice_list = recom_models.Notice.objects.filter(company__region__region = region)

        elif salary != "":
            notice_list = recom_models.Notice.objects.filter(min_sal__gte=salary_int)

        elif category == "None" and region == "None" and salary == "":
            notice_list = recom_models.Notice.objects.all()

        ctx['notices'] = notice_list

        return render(request, 'search.html', ctx)
    else:
        return render(request, 'search.html', ctx)




    return render(request, 'search.html', ctx)


# 채용정보 보여주기
def job_list(request):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')


    region_list = recom_models.Region.objects.all()
    category_list = recom_models.JobsCd.objects.raw('SELECT DISTINCT(jobs_cd) FROM notice')

    ctx['region_list'] = region_list
    ctx['category_list'] = category_list

    if request.method == 'POST':
        category = request.POST['category']
        region = request.POST['region']
        salary = request.POST['salary']


        if salary != "":
            salary_int = int(salary) * 10000



        if category != "None" and region != "None" and salary != "":
            notice_list = recom_models.Notice.objects.filter(jobs_cd__job_name = category, company__region__region = region, min_sal__gte=salary_int)

        elif category == "None" and region != "None" and salary != "":
            notice_list = recom_models.Notice.objects.filter(company__region__region = region, min_sal__gte=salary_int)

        elif region == "None" and category != "None" and salary != "":
            notice_list = recom_models.Notice.objects.filter(jobs_cd__job_name = category, min_sal__gte=salary_int)

        elif salary == "" and region != "None" and category != "None":
            notice_list = recom_models.Notice.objects.filter(jobs_cd__job_name = category, company__region__region = region)

        elif category != "None":
            notice_list = recom_models.Notice.objects.filter(company__region__region = region)

        elif region != "None":
            notice_list = recom_models.Notice.objects.filter(company__region__region = region)

        elif salary != "":
            notice_list = recom_models.Notice.objects.filter(min_sal__gte=salary_int)

        elif category == "None" and region == "None" and salary == "":
            notice_list = recom_models.Notice.objects.all()

    else:
        notice_list = recom_models.Notice.objects.raw('SELECT * FROM notice')


    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(notice_list, 20)
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
    authuser = recom_models.AuthUser.objects.get(username=username)
    dbuser = recom_models.User.objects.get(user=authuser)

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

    # 연봉정보 합치기
    salary_str = "연봉타입 : "
    salary_str += str(notice.sal_tp_nm)
    salary_str += ',\n'
    salary_str += "최대 : " + max_sal_str
    salary_str += ',\n'
    salary_str += "최소 : " + min_sal_str

    ctx['salary_str'] = salary_str

    # 회사주소 합치기
    # <h5 class="info-text">{{notice.company.basic_addr}}</h5>
    # <h5 class="info-text">{{notice.company.detail_addr}}</h5>

    company_addr = notice.company.basic_addr + " " + notice.company.detail_addr
    ctx['company_addr'] = company_addr


    search = recom_models.Favorite.objects.filter(user=dbuser, notice=notice)
    if search.exists():
        ctx['favorite'] = True
    else:
        ctx['favorite'] = False

    # print(salary_str)

    return render(request, 'job_detail.html', ctx)

def add_favorite(request, pk):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')
    authuser = recom_models.AuthUser.objects.get(username=username)
    dbuser = recom_models.User.objects.get(user=authuser)
    notice = recom_models.Notice.objects.get(notice_id=pk)

    recom_models.Favorite.objects.create(user=dbuser, notice=notice, applieddate=datetime.now())

    return redirect(job_detail, pk)

def delete_favorite(request, pk):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')
    authuser = recom_models.AuthUser.objects.get(username=username)
    dbuser = recom_models.User.objects.get(user=authuser)
    notice = recom_models.Notice.objects.get(notice_id=pk)

    fav = recom_models.Favorite.objects.get(user=dbuser, notice=notice)
    fav.delete()

    return redirect(job_detail, pk)

def favorite(request):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')
    userid = User.objects.get(username=username).id

    notices = recom_models.Notice.objects.raw('select * from favorite join notice on favorite.notice_id = notice.notice_id where user_id = %s', [userid])
    ctx['notices'] = notices

    return render(request, 'favorite.html', ctx)

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

            query = "SELECT user_license_id FROM user_license WHERE user_spec_id = @spec_id;"
            cursor.execute(query)
            temp_lst = list(cursor.fetchall())

            idx_lst = []
            for i in range(num_license):
                idx_lst.append(temp_lst[i][0])
            license_lst = list(zip(idx_lst, license_lst))

            ctx['career'] = career
            ctx['license'] = license_lst
            ctx['usercarexists'] = True

        else:
            ctx['usercarexists'] = False

    else:
        ctx['userspecexists'] = False

    if recom_models.UserLicense.objects.all():
        ctx['licenseid'] = (recom_models.UserLicense.objects.all().latest('user_license_id').user_license_id) + 1
    else:
        ctx['licenseid'] = 1
    ctx['basic'] = recom_models.User.objects.get(user_id=userid)
    basic = recom_models.User.objects.raw('select * from user join region on user.region_id = region.region_id where user_id = %s', [userid])
    print(basic)

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

    success_url ="/recom/interest/"

class EduLevelUpdate(UpdateView):
    model = recom_models.UserSpec

    template_name = 'edit_edu.html'

    fields = [
        "edu_level"
    ]

    success_url = "/recom/interest/"

class EduLevelAdd(CreateView):
    model = recom_models.UserSpec

    template_name = 'add_edu.html'

    fields = ['edu_level']

    success_url = '/recom/interest/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        userid = User.objects.get(username=self.request.user.username).id
        obj.user_id = userid
        obj.user_spec_id = userid
        obj.save()

    def post(self, request, pk):
        super(EduLevelAdd, self).post(request)
        return redirect('interest')

class CareerAdd(CreateView):
    model = recom_models.UserCareer
    template_name = 'add_career.html'
    fields = ['career']

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = recom_models.User.objects.get(user=self.request.user.id)
        userspec = recom_models.UserSpec.objects.get(user=user).user_spec_id
        obj.user_spec_id = userspec
        obj.user_career_id = self.request.user.id
        obj.save()

    def post(self, request, pk):
        super(CareerAdd, self).post(request)
        return redirect('interest')


class LicenseAdd(CreateView):
    model = recom_models.UserLicense
    template_name = 'add_license.html'
    fields = ['license']

    def form_valid(self, form):
        obj = form.save(commit=False)
        userid = User.objects.get(username=self.request.user.username).id
        if recom_models.UserLicense.objects.filter(user_spec_id=userid).exists():
            licenseid = recom_models.UserLicense.objects.filter(user_spec_id=userid).latest('user_license_id').user_license_id + 1
        else:
            licenseid = 1
        obj.user_spec_id = userid
        obj.user_license_id = licenseid
        obj.save()

    def post(self, request):
        super(LicenseAdd, self).post(request)
        return redirect('interest')

class LicenseTypeAdd(CreateView):
    model = recom_models.License
    template_name = 'add_lictype.html'
    fields = ['license']

    def form_valid(self, form):
        obj = form.save(commit=False)
        userid = User.objects.get(username=self.request.user.username).id
        if recom_models.License.objects.all().exists():
            licenseid = recom_models.License.objects.all().latest('license_id').license_id + 1
        else:
            licenseid = 1
        obj.license_id = licenseid
        obj.save()

    def post(self, request):
        super(LicenseTypeAdd, self).post(request)
        return redirect('add_license')

class LicenseDelete(DeleteView):
    model = recom_models.UserLicense
    template_name = 'delete_license.html'

    success_url = '/recom/interest/'


# input : user_id
# output : rcmd_lst
def recommend(id):
    host = "project.catth3zniejo.ap-northeast-2.rds.amazonaws.com"
    port = 3306
    username = "admin"
    password = "tkdghkd1!"
    database = "JobRecommendSystem"

    conn = pymysql.connect(host, user=username, passwd=password, db=database, \
    port=port, use_unicode=True, charset='utf8')
    cursor = conn.cursor()

    # @region_id = user의 '지역정보'
    q1 = "SET @region_id = (SELECT region_id FROM user WHERE user_id = {});".format(id)
    # @career = user의 '경력정보'
    q2 = "SET @career = (SELECT career FROM career WHERE career_id = (SELECT career_id FROM user_career WHERE user_spec_id = (SELECT user_spec_id FROM user_spec WHERE user_id = {})));".format(id)
    # @favorite = user의 '찜한정보'
    q3 = "SET @favorite = (SELECT notice_id FROM favorite WHERE user_id ={});".format(id)

    q1_check = "SELECT @region_id;"
    q2_check = "SELECT @career;"
    q3_check = "SELECT @favorite;"
    q4_check = "SELECT edu_level FROM user_spec WHERE user_id = {};".format(id)

    cursor.execute(q1)
    cursor.execute(q2)
    cursor.execute(q3)

    q1, q2, q3, q4 = ('','','','')
    cursor.execute(q1_check)
    if cursor.fetchone()[0] != None:
        q1 = 'WHERE region_id = @region_id'

    cursor.execute(q2_check)
    if cursor.fetchone()[0] != None:
        q2 = 'WHERE career = @career'

    cursor.execute(q3_check)
    if cursor.fetchone()[0] != None:
        q3 = 'WHERE notice_id = @favorite'

    cursor.execute(q4_check)
    if cursor.fetchone() != None:
        q4 = 'JOIN (SELECT edu_level FROM edu_level WHERE edu_level_id <= (SELECT edu_level_id FROM edu_level WHERE edu_level = (SELECT edu_level FROM user_spec WHERE user_id = {}))) AS e ON fv.min_edubg = e.edu_level'.format(id)

    q5 = "SELECT company, title, career, min_edubg, notice_id FROM (SELECT fv.company_id, fv.title, fv.career, fv.min_edubg, fv.notice_id FROM (SELECT company_id, title, career, min_edubg, notice_id FROM notice AS n JOIN (SELECT company_id AS c_id FROM company {}) AS c ON c_id = n.company_id {} UNION SELECT company_id, title, career, min_edubg, notice_id FROM notice {}) AS fv {}) AS lst JOIN company AS c ON c.company_id = lst.company_id;".format(q1, q2, q3, q4)


    cursor.execute(q5)
    rcmd_lst = cursor.fetchall()

    return rcmd_lst



def personal(request):
    ctx = {}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user

    # username = 'Tom'
    # info = recom_models.User.objects.filter(name=username)
    # if info.exists():
    #     ctx['name'] = info
    #     loc = getattr(recom_models.User.objects.get(name=username), "location")
    #     day = getattr(recom_models.User.objects.get(name=username), "holiday_tp_nm")
    #
    #
    #     list = recom_models.Company.objects.raw('SELECT c.company_id, c.company, c.basic_addr, n.title, n.sal_tp_nm, n.max_sal, n.min_sal, n.holiday_tp_nm, n.min_edubg, n.career FROM company AS c JOIN notice AS n ON c.company_id = n.company_id JOIN user AS u ON c.region_id = (SELECT region_id FROM region WHERE %s = region) WHERE n.min_sal > 25000000 AND n.holiday_tp_nm = %s', [loc, day])
    #     ctx['list'] = list

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')


    notice_list = recommend(user.pk)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(notice_list, 20)

    try:
        notices = paginator.page(page) # 여기서 에러!
    except PageNotAnInteger:
        notices = paginator.page(1)
    except EmptyPage:
        notices = paginator.page(paginator.num_pages)


    if notice_list is not None:
        ctx['list'] = notices


    return render(request, 'personalized.html', ctx)

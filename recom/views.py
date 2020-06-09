from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User

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

def job_detail(request):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')



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

    host = "project.catth3zniejo.ap-northeast-2.rds.amazonaws.com"
    port = 3306
    username = "admin"
    password = "tkdghkd1!"
    database = "JobRecommendSystem"

    conn = pymysql.connect(host, user=username, passwd=password, db=database, \
    port=port, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    user_id = 1

    user_info = {}
    user_info.update(user_id = user_id)

    query = "SET @spec_id = (SELECT user_spec_id FROM user AS u JOIN user_spec AS s ON u.user_id = s.user_id WHERE user_spec_id = {});".format(user_id)
    cursor.execute(query)
    query = "SELECT edu_level FROM user_spec WHERE user_spec_id = @spec_id;"
    cursor.execute(query)
    edu_level = cursor.fetchall()[0][0]

    query1 = "SET @c_id = (SELECT career_id FROM user_career WHERE user_spec_id = @spec_id); "
    query2 = "SELECT career FROM career WHERE career_id = @c_id;"
    cursor.execute(query1)
    cursor.execute(query2)
    career = cursor.fetchall()[0][0]

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

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')

    userid = User.objects.get(username=username).id

    if recom_models.User.objects.filter(user_id=userid).exists():
        ctx['debug'] = 'Exists'
    else:
        ctx['debug'] = 'Does not exist'
        recom_models.User.objects.create(user_id=User.objects.get(username=username).id)
    
    ctx['basic'] = recom_models.User.objects.get(user_id=userid)
    ctx['edu'] = edu_level
    ctx['career'] = career
    ctx['license'] = license_lst
    return render(request, 'interest.html', ctx)

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

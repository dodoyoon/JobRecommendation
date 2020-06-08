from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def interest(request):
    ctx = {}

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        ctx['userobj'] = user
    else:
        return redirect('login')


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

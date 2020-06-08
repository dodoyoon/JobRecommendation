from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from recom import models as recom_models

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


def job_list(request):
    ctx={}

    list = recom_models.Notice.objects.raw('SELECT * FROM notice')
    ctx['list'] = list

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

    return render(request, 'personalized.html', ctx)
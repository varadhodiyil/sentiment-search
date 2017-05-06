from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from sentiment_search.business.resources import *
from django.core.files.storage import FileSystemStorage
from sentiment_search.resources import *
import json
import os
# Create your views here.

def profile(request):
    if not request.session.has_key("business_id"):
        return HttpResponseRedirect("login")
    entity_id = request.session['business_id'] # Saved in Session
    if request.method == "POST":
        uploaded_file_url=""
        if "logo" in request.FILES:
            name = request.POST.get("name")
            logo = request.FILES["logo"]
            address=request.POST.get("address")
            path = handle_uploaded_file(logo.name,logo)
            url = upload_to_google_storage(path,entity_id,logo,"business")
            resp = edit_profile(id_=entity_id,name=name,logo=url,address=address)
            os.unlink(path)
            response = dict()
            response['status'] =True
        return HttpResponse(resp)
    else:
        return render(request, 'business/dashboard.html')

def data_day(request):
    
    if not request.session.has_key("business_id"):
        return HttpResponseRedirect("login")
    entity = request.session['business_id']
    resp = dict()
    date = request.GET.get("date")
    if date:
        resp['data'] = get_data_date(date,entity=entity)
    else:
        resp['data'] = get_data_date(entity=entity)
    return HttpResponse(json.dumps(resp,default=str),content_type='application/json')


def report(request):
    if not request.session.has_key("business_id"):
        return HttpResponseRedirect("login")
    entity = request.session['business_id']
    since = request.GET.get("since")
    data = get_report(entity,since=since)

    return HttpResponse(json.dumps(data,default=str),content_type='application/json')


def getInvalidParams():
    result = dict()
    result['status'] = False
    result['message'] = "Invalid Params"
    return result

def register(request):
    if  request.session.has_key("business_id"):
        return HttpResponseRedirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            response = get_register(username , password) 
        else:
            response = getInvalidParams()
        if response['status']:
            request.session['business_username'] = username
            request.session['business_id'] = response['id']
            return HttpResponseRedirect("dashboard")
        else:
            return HttpResponse(json.dumps(response),content_type='application/json')
    else:
        return render(request, 'business/register.html')
        

def login(request):
    if  request.session.has_key("business_id"):
        return HttpResponseRedirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            response = get_login( username , password) 
        else:
            response = getInvalidParams()
        if response['status']:
            request.session['business_username'] = username
            request.session['business_id'] = response['id']
            return HttpResponseRedirect("")
        else:
            return HttpResponse(json.dumps(response),content_type='application/json')
    else:
        return render(request, 'business/login.html')

def logout(request):
    if  request.session.has_key("business_id"):
        id_= request.session['business_id']
        update_logs(id_, "BusinessLogout", "Logged out ")
    request.session.flush()
    return HttpResponseRedirect("login")


def get_session(request):
    result = dict()
    if  request.session.has_key("user_id"):
        id_= request.session['user_id']
        data = get_session_user(id_)
        result = data
        result['status'] = True
    else:
        data = dict()
        data['status'] = False
        data['Message'] = "Unauthorized"
    return HttpResponse(json.dumps(data),content_type='application/json')
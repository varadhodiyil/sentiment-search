from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from sentiment_search.users.resources import *
import json
import os
from sentiment_search.resources import *
# Create your views here.


def profile(request):
    if not request.session.has_key("user_id"):
        return HttpResponseRedirect("login")
    user_id = request.session['user_id'] # Saved in Session
    if request.method == "POST":
        uploaded_file_url=""
        if "logo" in request.FILES:
            name = request.POST.get("name")
            dp = request.FILES["logo"]
            address=request.POST.get("address")
            path = handle_uploaded_file(dp.name,dp)
            url = upload_to_google_storage(path,user_id,dp)
            resp = edit_profile(id_=user_id,name=name,display_picture=url,address=address)
            os.unlink(path)
            response = dict()
            response['status'] =True
        return HttpResponse(resp)
    else:
        return render(request, 'users/dashboard.html')

def report(request):
    # if not request.session.has_key("business_id"):
    #     return HttpResponseRedirect("login")
    # entity = request.session['business_id']
    # since = request.GET.get("since")
    # data = get_report(entity,since=since)
    
    # return HttpResponse(json.dumps(data,default=str),content_type='application/json')
    pass


def getInvalidParams():
    result = dict()
    result['status'] = False
    result['message'] = "Invalid Params"
    return result

def register(request):
    if  request.session.has_key("user_id"):
        return HttpResponseRedirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            response = get_register(username , password) 
        else:
            response = getInvalidParams()
        if response['status']:
            request.session['user_name'] = username
            request.session['user_id'] = response['id']
            return HttpResponseRedirect("dashboard")
        else:
            return HttpResponse(json.dumps(response),content_type='application/json')
    else:
        return render(request, 'business/register.html')
        

def login(request):
    if  request.session.has_key("user_id"):
        return HttpResponseRedirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            response = get_login( username , password) 
        else:
            response = getInvalidParams()
        if response['status']:
            request.session['user_name'] = username
            request.session['user_id'] = response['id']
            return HttpResponseRedirect("")
        else:
            return HttpResponse(json.dumps(response),content_type='application/json')
    else:
        return render(request, 'users/login.html')

def logout(request):
    if  request.session.has_key("user_id"):
        id_= request.session['user_id']
        update_logs(id_, "UserLogout", "Logged out ")   
    request.session.flush()
    return HttpResponseRedirect("login")

def get_session(request):
    result = dict()
    if  request.session.has_key("user_id"):
        id_= request.session['user_id']
        data = get_user_session(id_)
        result = data
        result['status'] = True
    else:
        data = dict()
        data['status'] = False
        data['Message'] = "Unauthorized"
    return HttpResponse(json.dumps(data),content_type='application/json')
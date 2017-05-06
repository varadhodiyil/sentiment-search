from sentiment_search.business.models import Business ,TopicData,TopicKeys , Logs
from hashlib import sha1
import os
from datetime import datetime ,time
from django.db.models import Count
from sentiment_search.resources import update_logs

def edit_profile(id_="",name=None, logo=None, address=None):
    if name:
        data = Business.objects.filter(id=id_)
        for toSave in data:
            toSave.name=name
            toSave.logo=logo
            toSave.address=address
            toSave.save()
            update_logs(id_, "Profile", "Updated Profile")
        return id_
    return False


def get_data_date(req_date=datetime.now(),entity=""):
    results=list()
    data_query=TopicData.objects.using("sentiment_search").filter(created_at__startswith=req_date, \
            topic_key=TopicKeys.objects.filter(key_val=entity).values_list("id")).values("id","data_entry",
            "sentiment_x","sentiment_y","created_by","platform","likes_fav")
    print data_query.query
    for d in data_query:
        results.append(d)
    return results

def get_report(entity=None,limit=20,since=datetime.now().date()):
    results=dict()
    since = datetime.strptime(since, '%Y-%m-%d')
    since = datetime.combine(since, time.max)  
    if entity:
        data = TopicData.objects.using("sentiment_search").extra(select={'day': 'date( created_at )'}).values('day').\
                filter(topic_key=TopicKeys.objects.filter(key_val=entity).values_list("id"),created_at__lte=since). \
                annotate(available=Count('id')).order_by("-created_at").\
                values("available","day")[:limit]
        print data.query
        result = list()
        for d in data:
            result.append(d)
        results['date_report'] = result
    return results

def get_register(username,password):
    response=dict()
    count = Business.objects.filter(username=username).count()
    if count ==0:
        password = sha1(password).hexdigest()
        id_ = sha1(username).hexdigest()
        Business(username=username,password=password,id=id_).save()
        desc = "A new Business User Created With userName %s"%username
        update_logs(id_, "BusinessRegistration", desc)
        response['status']=True
        response['message']="User Created"
        response['id'] = id_
    else:
        response['status']=False
        response['message']="User Already Exists"
    return response


def get_login(username,password):
    password = sha1(password).hexdigest()
    response=dict()
    data = Business.objects.filter(username=username,password=password).values("id","username")
    if len(data) > 0 :
         response['status'] = True
         response['message'] = "Logged In"
         desc = "UserLogged into System"
         id_ = data[len(data)-1]['id']
         response['id'] = id_
         update_logs(id_, "BusinessLogin", desc)
    else:
        response['status'] = False
        response['message'] = "Invalid Credentials"
    return response

def get_session_user(user_id):
    result = list()
    data = Business.objects.filter(id=user_id).values("id","username","logo") 
    for d in data:
        result = d
    return result
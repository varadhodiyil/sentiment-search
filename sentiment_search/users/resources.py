from sentiment_search.business.models import Logs
from hashlib import sha1
from sentiment_search.users.models import Users
from sentiment_search.resources import update_logs

def edit_profile(id_="",name=None, display_picture=None, address=None):
    if name:
        data = Users.objects.filter(id=id_)
        for toSave in data:
            toSave.name=name
            toSave.display_picture=display_picture
            toSave.address=address
            toSave.save()
            update_logs(id_, "Profile", "Updated Profile")
        return id_
    return False

def get_register(username,password):
    response=dict()
    count = Users.objects.filter(username=username).count()
    if count == 0:
        password = sha1(password).hexdigest()
        id_ = sha1(username).hexdigest()
        Users(username=username,password=password,id=id_).save()
        desc = "A new Business User Created With userName %s"%username
        update_logs(id_, "UserRegistration", desc)
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
    data = Users.objects.filter(username=username,password=password).values("id","username")
    if len(data) > 0 :
         response['status'] = True
         response['message'] = "Logged In"
         desc = "UserLogged into System"
         id_ = data[len(data)-1]['id']
         response['id'] = id_
         update_logs(id_, "UserLogin", desc)
    else:
        response['status'] = False
        response['message'] = "Invalid Credentials"
    return response

def get_user_session(user_id):
    result = list()
    data = Users.objects.filter(id=user_id).values("id","username","display_picture") 
    for d in data:
        result = d
    return result

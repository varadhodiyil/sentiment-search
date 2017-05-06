from sentiment_search.business.models import Logs
from GoogleStorage.Google_Storage import GoogleStorage
import os

GS = GoogleStorage()
GS.setBucketName("sentiment-search")


def handle_uploaded_file(name,file):
    base = os.path.dirname(__file__)
    path = os.path.join(base,"temp",name)
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    return path

def upload_to_google_storage(path,entity_id,file_name,type="users"):
    return GS.upload_object(path,predefinedAcl="publicRead",
                name="uploads/%s/%s/profile/%s" % (type,entity_id,file_name))


def update_logs(user_id,event,description):
    Logs(user_id=user_id,event=event,description=description).save()

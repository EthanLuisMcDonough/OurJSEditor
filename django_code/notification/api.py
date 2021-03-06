# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from ourjseditor import api
from models import Notif

# /notif/NOTIFIC_ID
@api.standardAPIErrors("PATCH")
@api.login_required
def notif(request, notif_id):
    notif = Notif.objects.get(notif_id=notif_id)

    if (request.method == "PATCH"):
        data = json.loads(request.body)
        read = data["isRead"] #true or false

        if request.user != notif.target_user:
            return api.error("Not authorized", status=401)

        if (read != True and read != False):
            return api.error("Invalid type for key \"isRead\"")

        notif.is_read = read
        notif.save()

        return api.succeed()

# /notifs
@api.standardAPIErrors("GET")
@api.login_required
def notif_list(request):
    notifs = Notif.objects.filter(target_user=request.user).order_by("-created")
    notifs = map(lambda n: n.to_dict(), notifs)

    return api.succeed({ "notifs": notifs })

# /notifs/count
@api.standardAPIErrors("GET")
@api.login_required
def notif_count(request):
    return api.succeed({
        "notifCount": Notif.objects.filter(target_user=request.user, is_read=False).count()
    })

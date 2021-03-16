from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import datetime
import json

from .models import Software, Package

def RegisterStatus(request, mac, Type):
    today = datetime.today()
    if Software.objects.filter(mac=mac, type=Type).exists():
        dc = {'status': True, 'message': Software.objects.get(mac=mac, type=Type).message}
    else:
        dc = {'status': False}
    if Package.objects.filter(soft__mac=mac, from_dt__lte=today.date(), to_dt__gte=today.date()).exists():
        dc['expiry'] = False
    else:
        dc['expiry'] = True
    return JsonResponse(dc)

def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data

@csrf_exempt
def Register(request):
    if request.method == 'POST':
        data = request.POST
        try:
            data = querydict_to_dict(data)
            sf = Software(**data)
            sf.save()
            return JsonResponse({'status': True, 'message': 'your software successfully registered'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': True, 'message': str(e)})

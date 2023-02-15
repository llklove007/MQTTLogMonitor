from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from . import models


# Create your views here.
def index(request):
    writer_qs = models.Log.objects.values("writer").distinct()
    list_writer = []
    for a in writer_qs:
        list_writer.append(a['writer'])
    return render(request, "index.html", {"writer": list_writer})


def GetData(request):
    get_msg = request.GET
    page = int(get_msg['page'])
    limit = int(get_msg['limit'])
    limitbegin = (page - 1) * limit
    limitend = page * limit
    time1 = get_msg['time1']
    time2 = get_msg['time2']
    writer = get_msg['writer']
    content = get_msg['content']

    kwargs = {
    }
    if writer:
        kwargs['writer'] = writer
    if content:
        kwargs['content__contains'] = content
    if time1 and time2:
        datetime1 = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
        datetime2 = datetime.strptime(time2, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
        kwargs['date_time__range'] = [datetime1, datetime2]
    if time1 and not time2:
        datetime1 = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
        kwargs['date_time__gte'] = datetime1
    if time2 and not time1:
        datetime2 = datetime.strptime(time2, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
        kwargs['date_time__lte'] = datetime2

    count_i = models.Log.objects.filter(**kwargs).count()

    qs = models.Log.objects.filter(**kwargs).order_by('-date_time')[limitbegin:limitend].values()
    list_qs = []
    for a in qs:
        a['date_time'] = a['date_time'].strftime('%Y-%m-%d %H:%M:%S')
        list_qs.append(a)

    return JsonResponse({
        "code": 0,
        "msg": "",
        "count": count_i,
        "data": list_qs})

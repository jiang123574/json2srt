import json
import os

from django.http import StreamingHttpResponse
from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, 'index.html')


def dz(x):
    ms = int(x % 1000)
    m, s = divmod(x/1000, 60)
    h, m = divmod(m, 60)
    return h, m, s, ms


def json2srt():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    res = json.load(open(os.path.join(base_dir, 'uploads', 'draft.json'), encoding="utf-8"))
    if res.get("platform").get("os") == "macOS":
        y = 1
    else:
        y = 1000
    zm = {}
    for i in res.get("materials").get("texts"):
        zm[i.get("id")] = i.get("content")
    x = 1
    fo = open(os.path.join(base_dir, 'uploads', "zm.srt"), "w")
    for s in res.get("tracks"):
        if s.get("subType") == "sub_sticker_text" or s.get("type") == "text":
            for i in s.get("segments"):
                start = i.get("target_timerange").get("start") / y
                end = i.get("target_timerange").get("start") / y + i.get("target_timerange").get("duration") / y
                sjz = "{0}:{1}:{2},{3} --> {4}:{5}:{6},{7}"
                h, m, s, ms = dz(start)
                h2, m2, s2, ms2 = dz(end)
                fo.write(str(x) + "\n")
                fo.write(sjz.format(h, m, s, ms, h2, m2, s2, ms2) + "\n")
                fo.write(zm[i.get("material_id")] + "\n")
                fo.write("\n")
                x += 1


def upload(request):
    if request.method == "POST":
        myFile = request.FILES.get("json2srt", None)

        if not myFile:
            return HttpResponse("no files")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        destination = open(os.path.join(base_dir, 'uploads', "draft.json"), 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        json2srt()
        return file_down(request)


def file_down(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'uploads', "zm.srt")
    if not os.path.isfile(file_path):  # 判断下载文件是否存在
        return HttpResponse(file_path)

    def file_iterator(file_path, chunk_size=1024):
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    try:
        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
        response = StreamingHttpResponse(file_iterator(file_path))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = 'attachment;filename="zm.srt"'
    except:
        return HttpResponse("文件不存在")
    return response

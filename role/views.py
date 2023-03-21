import time

from django.http import HttpResponse
from django.shortcuts import render
from file_upl_sav.svg_html import save_html, save_svg
from file_use.file_use import handle_uploaded_file
from textanalyzer.role_analyzer import open_file_txt, RoleAnalyzer
from image_use.image_converter import change_background
from redis_meth.redis_use import set_key, get_key

import PIL.Image as image
from test_conv import cloud_converter

role_analyzer = RoleAnalyzer()


def role_sent_view(request):
    if 'upl_role' in request.POST:
        upl_file = request.FILES.get('document_role', False)
        if upl_file:
            data_file = upload_file(request, upl_file=upl_file)
            return render(request, 'role/role_sent.html', {'data_file': data_file})
    if 'analyze_role' in request.POST:
        start_time = time.time()
        text_area = request.POST['text_area_role']
        update_data_area = role_analyzer.display(text_area)
        print("--- %s seconds ---" % (time.time() - start_time))
        save_text(request)
        save_html(update_data_area)
        save_svg(update_data_area)
        return render(request, 'role/role_sent.html',
                      {'html_upload': "/static/upload/role.html", 'data_file': get_key('text')})
    if 'save_svg' in request.POST:
        if cloud_converter():
            return download_file()
    return render(request, 'role/role_sent.html', {'data_file': get_key('text')})


def upload_file(request, upl_file):
    handle_uploaded_file(upl_file, 'role/static/upload/')
    path_to_file = "role/static/upload/" + upl_file.name
    return open_file_txt(path_to_file)


def download_file():
    change_background()
    im = image.open("role/static/saved/role.png")
    response = HttpResponse(content_type='image/png')
    im.save(response, 'png')
    response['Content-Disposition'] = 'attachment; filename={0}'.format("role.png")
    return response


def save_text(request):
    text_area = request.POST['text_area_role']
    set_key('text', text_area)

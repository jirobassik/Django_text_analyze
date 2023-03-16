import time

from django.http import HttpResponse
from django.shortcuts import render

from file_upl_sav.svg_html import save_html, save_svg
from file_use.file_use import handle_uploaded_file
from textanalyzer.role_analyzer import open_file_txt, RoleAnalyzer
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import PIL.Image as image

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
        save_html(update_data_area)
        save_svg(update_data_area)
        return render(request, 'role/role_sent.html',
                      {'html_upload': "/static/upload/role.html", 'text_info': text_area})
    if 'save_svg' in request.POST:
        drawing = svg2rlg("role/static/upload/role.svg")
        renderPM.drawToFile(drawing, "role/static/saved/role.png", fmt="PNG")
        return download_file()
    return render(request, 'role/role_sent.html')


def upload_file(request, upl_file):
    handle_uploaded_file(upl_file, 'role/static/upload/')
    path_to_file = "role/static/upload/" + upl_file.name
    return open_file_txt(path_to_file)


def download_file():
    im = image.open("role/static/saved/role.png")
    response = HttpResponse(content_type='image/png')
    im.save(response, 'png')
    response['Content-Disposition'] = 'attachment; filename={0}'.format("Export.png")
    return response

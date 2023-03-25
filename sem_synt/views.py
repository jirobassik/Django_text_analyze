from django.http import HttpResponse
from django.shortcuts import render

from utilities.file_use.file_use import handle_uploaded_file
from utilities.textanalyzer.role_analyzer import open_file_txt
from utilities.textanalyzer.sem_synt_analyzer import SemSyntAnalyzer
from utilities.redis_meth.redis_use import get_key, set_key
import PIL.Image as image

sem_synt_analyzer = SemSyntAnalyzer()
def sem_synt(request):
    if 'upl_sem_synt' in request.POST:
        upl_file = request.FILES.get('document_sem_synt', False)
        if upl_file:
            data_file = upload_file(request, upl_file=upl_file)
            return render(request, 'sem_synt/sem_synt.html', {'text_area_sem': data_file})
    if 'analyze_sem_synt' in request.POST:
        text_area_sem_synt = request.POST['text_area_sem_synt']
        set_key('sem_synt', text_area_sem_synt)
        sem_synt_analyzer.tree_(text_area_sem_synt)
        return render(request, 'sem_synt/sem_synt.html',
                      {'html_sem_synt': "/static/upload/tree.html",
                       'text_area_sem': get_key('sem_synt'),
                       'upload_sem': True})
    if 'save_sem_synt' in request.POST:
        return download_file()
    return render(request, 'sem_synt/sem_synt.html', {'text_area_sem': get_key('sem_synt')})


def download_file():
    im = image.open("sem_synt/static/upload/tree.png")
    response = HttpResponse(content_type='image/png')
    im.save(response, 'png')
    response['Content-Disposition'] = 'attachment; filename={0}'.format("tree.png")
    return response

def upload_file(request, upl_file):
    handle_uploaded_file(upl_file, 'role/static/upload/')
    path_to_file = "role/static/upload/" + upl_file.name
    return open_file_txt(path_to_file)

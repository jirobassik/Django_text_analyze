from django.http import HttpResponse
from django.shortcuts import render
from textanalyzer.sem_synt_analyzer import SemSyntAnalyzer
from redis_meth.redis_use import get_key, set_key
import PIL.Image as image

sem_synt_analyzer = SemSyntAnalyzer()
def sem_synt(request):
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

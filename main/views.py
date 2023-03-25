import os
import mimetypes
import time

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from utilities.file_use.file_use import handle_uploaded_file
from utilities.textanalyzer.text_analyzer import TextAnalyzer, open_file_txt
from .models import OwnerModel
from .forms import ObjectForm
from utilities.table_work.table_work import clear_tb, add_data_tb
from utilities.file_upl_sav.csv_work import csv_creater, csv_reader
from django.contrib.postgres.search import SearchVector
from utilities.redis_meth.redis_use import get_key, set_key

text_analyze = TextAnalyzer()


def delete_object(request, id):
    member = OwnerModel.objects.get(id=id)
    member.delete()
    return HttpResponseRedirect(reverse('main'))


class ObjectCreate(CreateView):
    form_class = ObjectForm
    template_name = 'main/add_lexem.html'


class ObjectUpdate(UpdateView):
    model = OwnerModel
    template_name = 'main/add_lexem.html'
    form_class = ObjectForm


def view(request):
    main_objs = OwnerModel.objects.order_by('lexemm')
    bool_search = False
    if 'upl' in request.POST:
        upl_file = request.FILES.get('document', False)
        if upl_file:
            data_file = upload_file(request, upl_file=upl_file)
            return render(request, 'main/main.html', {'data_file': data_file})
    if 'analyze' in request.POST:
        start_time = time.time()
        update_data_area = analyze(request)
        save_text(request)
        print("--- %s seconds ---" % (time.time() - start_time))
        return render(request, 'main/main.html', {'update_data': main_objs, 'data_file': update_data_area})
    if 'upl_csv' in request.POST:
        try:
            main_objs = upload_csv(request)
        except ValueError:
            return render(request, 'main/main.html', {'update_data': main_objs, 'error': True, 'search': True})
    if 'save_csv' in request.POST:
        csv_creater()
        return download_file()
    if 'search' in request.POST:
        main_objs, bool_search, update_data_area = search_post(request)
    return render(request, 'main/main.html',
                  {'update_data': main_objs, 'search': bool_search, 'data_file': get_key('text')})

def search_post(request):
    search = request.POST['search_data']
    update_data_area = request.POST['text_area']
    main_objs = OwnerModel.objects.annotate(
        search=SearchVector("lexemm", "morph", "role", )).filter(
        search=search)
    return main_objs, True, update_data_area

def upload_csv(request):
    upl_csv = request.FILES.get('csv_upl', False)
    str_upl_csv = str(upl_csv)
    if upl_csv:
        handle_uploaded_file(upl_csv, 'main/static/upload/')
        csv_reader(str_upl_csv)
        return OwnerModel.objects.order_by('lexemm')


def upload_file(request, upl_file):
    handle_uploaded_file(upl_file, 'main/static/upload/')
    path_to_file = "main/static/upload/" + upl_file.name
    return open_file_txt(path_to_file)


def analyze(request):
    clear_tb()
    update_data_area = request.POST['text_area']
    list_punct = text_analyze.get_text_punctation(update_data_area)
    add_data_tb(list_punct)
    return update_data_area


def download_file():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'data.csv'
    filepath = BASE_DIR + '/main/static/saved/' + filename
    path = open(filepath, 'r', encoding="utf-8", newline='')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def save_text(request):
    text_area = request.POST['text_area']
    set_key('text', text_area)

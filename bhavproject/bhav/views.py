from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
import mimetypes
from .services import BhavScraper
from bhavproject.settings import CSV_DATA_PATH
import os
from django.http import HttpResponse
from django.views.static import serve
# Create your views here.

class Search(APIView):

    def get(self, request, format=None):
        name = request.query_params.get('name')
        objs = []
        if name is not None:
            key = str(name.upper())+"*"
            objs_list = cache.keys(key)
            obj_data = cache.get_many(objs_list)
            for key_name in objs_list:
                objs.append(obj_data[key_name])

            return Response(objs)
        else:
            key = "*"
            objs_list = cache.keys(key)[:9]
            obj_data = cache.get_many(objs_list)
            for key_name in objs_list:
                objs.append(obj_data[key_name])

            return Response(objs)
        return Response("Search parameter missing.",400)

def download_file(request):
    # fill these variables with real values
    bhav_scraper = BhavScraper()
    _file_name = bhav_scraper.bhav_file_name
    filepath = os.path.join(CSV_DATA_PATH,_file_name)
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
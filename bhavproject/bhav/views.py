from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
import mimetypes
from .services import BhavScraper
from bhavproject.settings import CSV_DATA_PATH
import os, glob
from django.http import HttpResponse
from django.views.static import serve
from bhav.utils import get_latest_file
# Create your views here.

class Search(APIView):
    '''
        Filter the redis cache and returns the result.
        If the query parameter name is not passed, returns first 9 results.
    '''
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
        key = "*"
        objs_list = cache.keys(key)[:9]
        obj_data = cache.get_many(objs_list)
        for key_name in objs_list:
            objs.append(obj_data[key_name])

        return Response(objs)

def download_file(request):
    '''
        Returns the latest bhavcopy file which was downloaded from bse website
        Endpoint from which the zip file is downloaded >
            https://www.bseindia.com/download/BhavCopy/Equity/EQ240421_CSV.zip

    '''

    filepath = get_latest_file()
    if os.path.exists(filepath):
        return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

    err_msg = f"File {_file_name} does not exist. Please try again later. "
    return HttpResponse(err_msg,404)
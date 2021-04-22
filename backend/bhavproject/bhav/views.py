from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
# Create your views here.

class Search(APIView):

    def get(self, request, format=None):
        name = request.query_params.get('name')
        if name is not None:
            key = str(name)+"*"
            objs_list = cache.keys(key)
            obj_data = cache.get_many(objs_list)
            return Response(obj_data)
        return Response("Search parameter missing.",400)
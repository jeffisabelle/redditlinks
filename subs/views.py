import json

from django.http import JsonResponse
from django.views.generic.base import View


class SubredditList(View):
    def get(self, request, *args, **kwargs):
        data = {}
        with open("static/js/data/subreddits.json") as f:
            data["subreddits"] = json.loads(f.read())
        return JsonResponse(data)

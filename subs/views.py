import json

from django.conf import settings
from django.http import JsonResponse
from django.views.generic.base import View


class SubredditList(View):
    def get(self, request, *args, **kwargs):
        data = {}
        base = settings.BASE_DIR
        relative = "/static/js/data/subreddits.json"
        f_path = base + relative
        with open(f_path, "r") as f:
            data["subreddits"] = json.loads(f.read())
        return JsonResponse(data)

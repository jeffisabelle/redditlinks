from django.views.generic.base import TemplateView


class ToWeekly(TemplateView):
    """
    todo: implement a base class for member settings
    that fetches member/token from the GET parameters,
    and returns the member object to the subclass.
    """
    template_name = 'members/toweekly.html'

    def get_context_data(self, **kwargs):
        context = super(ToWeekly, self).get_context_data(**kwargs)
        print self.request.GET
        return context

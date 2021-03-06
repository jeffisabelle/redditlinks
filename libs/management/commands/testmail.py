from members.models import Member

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from libs.maillib import MailLib


class Command(BaseCommand):
    def sendmail(self, to_email):
        from_mail = 'Reddit.cool <no-reply@reddit.cool>'
        title = "Test Email for Deliverability"
        text_content = """
        This is just an example mail.
        """
        send_mail(title, text_content, from_mail, to_email)

    def get_members(self):
        member_filter = {
            "is_active": True,
            "email": "muhitosan@gmail.com"
        }
        return Member.objects.filter(**member_filter)

    def handle(self, *args, **options):
        print('sending emails..')

        members = self.get_members()

        ml = MailLib()
        for member in members:
            print('sending mail to: %s' % member)
            ml.process(member)

        print('done..')
        return 'mails-sent'

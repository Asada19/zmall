from celery import shared_task
from django.contrib.auth import get_user_model
from advertisement.models import Advertisement
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from config.celery import app
from core.management.commands.parse import Command

User = get_user_model()
parse = Command()


@app.task
def send_notification():
    subject, from_email = 'Notification', 'livencor@gmail.com'
    advertisements = Advertisement.objects.all()[:10]
    html_content = render_to_string('notification/notification.html', {'advertisement': advertisements})
    text_content = strip_tags(html_content)
    for user in User.objects.all():
        msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
        msg.attach_alternative(html_content, "text/html")
        send_mail(
            subject=subject,
            message=None,
            html_message=html_content,
            from_email=from_email,
            recipient_list=[
                user.email
            ],
            fail_silently=True,
        )


@app.task
def start_parse():
    parse.handle()


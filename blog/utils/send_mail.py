
from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'arun.singh1@oodlestechnologies.com',
    ['avisingh10.as@gmail.com'],
    fail_silently=False,
)
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from NewsPaper.celery import 
from .models import Post


def send_notification(preview, pk, title, subscribers):
    html_context = render_to_string(
        'post_created_email.thml',
        {
            'text': preview,
            'link': f'{setings.SITE_URL}/news/{pk}'
        }        
        )
    
    msg = EmailMultiAlternatives(
        subjects=title,
        body='',
        from_email=setings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=Post.postCategory)
def notify_abiut_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()
            
        subscribers = [s.mail for s in subscribers]
        
        send_notification(instance.preview(), instance.pk, instance.title, subscribers)
        action.delay()       
from django import forms
from ecards.models import Send
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from postmark.django_backend import EmailBackend
from django.conf import settings

class SendForm(forms.ModelForm):
    message = forms.CharField(max_length=1024, widget=forms.Textarea())
    class Meta:
        model = Send
        exclude = ('ip', 'card')

PostmarkBackend = EmailBackend(apikey=settings.POSTMARK_API_KEY)

def send_card(request, card):
    card_url = 'http://%s/media/images/ecard/%s.jpg' % (request.META['HTTP_HOST'], card)
    card_page_url = 'http://%s/valentines/ecards/%s/' % (request.META['HTTP_HOST'], card)
    if request.method == 'POST':
        form = SendForm(request.POST)
        if form.is_valid():
            send = form.save(commit=False)
            send.ip = request.META['REMOTE_ADDR']
            send.card = card
            send.save()
            
            subject = '%s sent you an e-card' % send.sender_name
            context = {'message': send.message, 'sender_name': send.sender_name, 'card_url': card_url, 'card_page_url': card_page_url}
            text_content = render_to_string('ecards/email.txt', context)
            html_content = render_to_string('ecards/email.html', context)
            
            msg = EmailMultiAlternatives(subject, text_content, settings.ECARD_FROM, [send.recipient_address], connection=PostmarkBackend)
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            
            return HttpResponseRedirect('../thanks/')
    else:
        form = SendForm()
    
    return direct_to_template(request, 'ecards/address.html', extra_context={'form': form, 'card_url': card_url})

def choose_card(request):
    return direct_to_template(request, 'ecards/choose.html')

def thanks(request):
    return direct_to_template(request, 'ecards/thanks.html')

def ecard(request, card):
    card_url = '/media/images/ecards/%s.jpg' % card
    return direct_to_template(request, 'ecards/card.html', extra_context={'card_url': card_url})
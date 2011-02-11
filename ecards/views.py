from django import forms
from ecards.models import Send
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from postmark.django_backend import EmailBackend
from django.conf import settings
import hashlib
import urllib2
from urllib import urlencode

info_urls = {
    'movies': '/industry/movie-theaters/e52906ca8ab74af5b5845e3a6a62d07d',
    'candy': '/industry/confectionery-processors-manufacturers/47f675067c1540a8aeb2f36de03090bb',
    'flowers': '/industry/florists-nursery-services/17add5dc860640cd984625c5aa11e020',
    'jewelry': '/industry/jewelry/3cc47c6e2157414b88697f45b5b5152f',
    'restaurants': '/industry/restaurants-drinking-establishments/a9a400d4febf4bff8688a0e47b0d4bc2'
}

class SendForm(forms.ModelForm):
    message = forms.CharField(max_length=1024, widget=forms.Textarea())
    class Meta:
        model = Send
        exclude = ('ip', 'card')

PostmarkBackend = EmailBackend(apikey=settings.POSTMARK_API_KEY)

def send_card(request, card):
    card_url = 'http://%s/media/images/ecards/%s.jpg' % (request.META['HTTP_HOST'], card)
    card_page_url = 'http://%s/valentines/ecard/%s/' % (request.META['HTTP_HOST'], card)
    if request.method == 'POST':
        form = SendForm(request.POST)
        if form.is_valid():
            send = form.save(commit=False)
            send.ip = request.META['REMOTE_ADDR']
            send.card = card
            send.save()
            
            subject = '%s sent you an e-card' % send.sender_name
            context = {
                'message': send.message,
                'sender_name': send.sender_name,
                'recipient_name': send.recipient_name,
                'card_url': card_url,
                'card_page_url': card_page_url,
                'id': send.pk,
                'hash': generate_message_hash(send.pk)
            }
            text_content = render_to_string('ecards/email.txt', context)
            html_content = render_to_string('ecards/email.html', context)
            
            msg = EmailMultiAlternatives(subject, text_content, settings.ECARD_FROM, [send.recipient_address], connection=PostmarkBackend)
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            
            if request.POST.get('signup', ''):
                if signup_email(send.sender_name, send.sender_address):
                    return HttpResponseRedirect('../thanks/')
            
            return HttpResponseRedirect('../thanks/')
    else:
        form = SendForm()
    
    return direct_to_template(request, 'ecards/address.html', extra_context={'form': form, 'card_url': card_url})

def choose_card(request):
    return direct_to_template(request, 'ecards/choose.html')

def thanks(request):
    return direct_to_template(request, 'ecards/thanks.html', extra_context={'email': request.GET.get('email', False)})

def ecard(request, card, message_id=None, message_hash=None):
    if message_id and message_hash and message_hash == generate_message_hash(message_id):
        message = Send.objects.get(pk=message_id)
    else:
        message = None
    info_url = info_urls.get(card, None)
    card_url = '/media/images/ecards/%s.jpg' % card
    name = card[:-1] if card[-1] == 's' else card
    return direct_to_template(request, 'ecards/card.html', extra_context={'card_url': card_url, 'message': message, 'info_url': info_url, 'name': name, 'email': request.GET.get('email', False), 'label': card})
    
def signup_simple(request):
    email = request.POST.get('email', '')
    zipcode = request.POST.get('zipcode', '')
    signup_email('', email, zipcode)
    return HttpResponseRedirect('../thanks/?email=1')

# util functions
def generate_message_hash(message_id):
    s = '%s%s' % (message_id, settings.SECRET_KEY)
    return hashlib.md5(s).hexdigest()[:5]

def signup_email(name, email, zipcode=None):
    names = name.strip().rsplit(' ', 1)
    first_name = names[0]
    last_name = names[1] if len(names) > 1 else ''
    
    data = {'email': email, 'firstname': first_name, 'lastname': last_name}
    
    if zipcode:
        data['zip'] = zipcode
    
    result = urllib2.urlopen('http://local.publicequalsonline.com/page/s/Valentines_Day_ecard', urlencode(data)).read()
    print result
    return 'SUCCESS' in result
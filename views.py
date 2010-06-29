from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from brisket.forms import ContactForm

EMAIL_RECIPIENTS = getattr(settings, "EMAIL_RECIPIENTS", [])
EMAIL_TEMPLATE = """%(comment)s"""

def contact(request):
    
    if request.method == 'POST':
        
        form = ContactForm(request.POST, label_suffix='')
        
        if form.is_valid():
            
            name = form.cleaned_data['name']
            from_email = '"%s" <%s>' % (name, form.cleaned_data['email'])
            
            email = EmailMessage('[Brisket] contact form submission from %s' % name,    # subject
                                 EMAIL_TEMPLATE % form.cleaned_data,                    # body
                                 from_email,                                            # from
                                 EMAIL_RECIPIENTS,                                      # to
                                 headers={'Reply-To': from_email})                      # headers
            email.send()
            
            messages.success(request, "Thanks for contacting us! We'll get back to you shortly.")
            return HttpResponseRedirect(reverse('contact_form'))
            
    else:
        
        form = ContactForm(label_suffix='')
        
    return render_to_response('contact.html', {'form': form}, context_instance=RequestContext(request))
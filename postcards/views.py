from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django import forms
from postcards.models import *
from postcards.card_text import get_card_png
from django.contrib.localflavor.us.forms import USStateField
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
import postcards
import os
import hashlib
import urllib2
import json
from influence import api

class PostcardForm(forms.ModelForm):
    office = forms.ChoiceField(choices=(('', '---------'), ('house', 'House'), ('senate', 'Senate')), required=False)
    state = forms.ChoiceField(choices=([('', '---------')] + list(STATE_CHOICES)), required=False)
    num_candidates = forms.ChoiceField(widget=forms.RadioSelect(), choices=((1, '1'), (2, '2')))
    class Meta:
        model = Postcard
        fields = ('office', 'state', 'td_id', 'num_candidates', 'sender_name', 'sender_address1', 'sender_address2', 'sender_city', 'sender_state', 'sender_zip', 'recipient_name', 'recipient_address1', 'recipient_address2', 'recipient_city', 'recipient_state', 'recipient_zip', 'message')

    
def order(request):
    search_error = False
    if request.method == 'POST':
        form = PostcardForm(request.POST)
        if form.is_valid():
            card = form.save()
            return HttpResponseRedirect('/postcard/confirm/%s/%s' % (card.id, card.get_code()))
    else:
        # they haven't submitted anything; try search and geolocation
        latlon = ()
        initial = {}
        if 'location' in request.GET:
            locinfo = json.loads(urllib2.urlopen("http://where.yahooapis.com/geocode?q=%s&flags=J&appid=%s" % (urllib2.quote(request.GET['location']), settings.YAHOO_API_KEY)).read())
            if 'Results' in locinfo['ResultSet'] and locinfo['ResultSet']['Results']:
                latlon = (locinfo['ResultSet']['Results'][0]['latitude'], locinfo['ResultSet']['Results'][0]['longitude'])
            else:
                search_error = "We're sorry; we were unable to find a location matching your search."
        else:
            ipinfo = json.loads(urllib2.urlopen("http://ipinfodb.com/ip_query.php?ip=%s&output=json&timezone=false" % request.META['REMOTE_ADDR']).read())
            latlon = (ipinfo['Latitude'], ipinfo['Longitude'])
        
        if latlon:
            success = True
            try:
                districtinfo = json.loads(urllib2.urlopen("http://services.sunlightlabs.com/api/districts.getDistrictFromLatLong.json?apikey=%s&latitude=%s&longitude=%s" % (settings.API_KEY, latlon[0], latlon[1])).read())
            except urllib2.HTTPError:
                success = False
            if success:
                state = districtinfo['response']['districts'][0]['district']['state']
                district = districtinfo['response']['districts'][0]['district']['number']
                #hack for single-district states
                if district == 0:
                    district = 1
                district = "%02d" % district
                congress = api.candidates_by_location("%s-%s" % (state, district))
                house = filter(lambda s: s['seat'] == 'federal:house', congress)
                inc = filter(lambda s: s['seat_status'] == 'I', house)
                
                if inc:
                    initial = {'office': 'house', 'state': state, 'td_id': inc[0]['entity_id']}
                elif house:
                    initial = {'office': 'house', 'state': state, 'td_id': house[0]['entity_id']}
        
        if 'location' in request.GET and not initial and not search_error:
            search_error = "We're sorry; we were unable to locate a politician at that location."
        
        
        form = PostcardForm(initial=initial)

    return direct_to_template(request, 'postcards/order.html', {'form': form, 'search_error': search_error})

def thumbnail(request, type, id):
    img_dir = os.path.join(os.path.dirname(postcards.__file__), 'static', 'png')
    thumb = get_thumbnail(type, id)
    return HttpResponse(open(thumb, 'rb'), mimetype='image/png')

def preview(request, id, hash):
    card = Postcard.objects.get(id=id)
    if hash != card.get_code():
        raise Http404
    image = get_card_png(card)
    return HttpResponse(open(image, 'rb'), mimetype='image/png')
    
def confirm(request, id, hash):
    # first, check the hash
    card = Postcard.objects.get(id=id)
    if hash != card.get_code():
        raise Http404
    type = 'candidate' if card.num_candidates == 1 else 'race'
    
    thumb = get_thumbnail(type, card.td_id)
    
    return direct_to_template(request, 'postcards/confirm.html', {'front': '/postcard/thumbnail/%s/%s' % (type, card.id), 'card': card})

# utility stuff
def get_thumbnail(type, id):
    img_dir = os.path.join(os.path.dirname(postcards.__file__), 'static', 'png')
    files = os.listdir(img_dir)
    match = filter(lambda s: s.startswith(type) and s.endswith('%s.png' % id), files)
    if match:
        return os.path.join(img_dir, match[0])
    else:
        return os.path.join(img_dir, 'resources', '%s.png' % type)
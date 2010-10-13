from django.template.defaultfilters import stringfilter, force_escape
from django import template
from django.contrib.humanize.templatetags.humanize import ordinal, intcomma

register = template.Library()

@register.filter(name='district_name')
def district_name(district):
    if district['seat'] == 'federal:senate':
        return 'Senate'
    elif district['seat'] == 'federal:house' and district['district']:
        d = district['district'].split('-')
        num = ordinal(int(d[1]))
        return 'House %s District' % num
    return ''

@register.filter(name='barchart')
def barchart(bar_data):
    # constant sizes of things
    bar_width = 100
    label_width = 150
    dollar_width = 40
    bar_height = 12
    bar_spacing = 4
    pre_bar = 4
    
    types = [ellipsize(k, 30) for k in bar_data.keys()]
    labels = ['$%s' % intcomma(int(float(l))) for l in bar_data.values()]
    numbers = [float(l) for l in bar_data.values()]
    
    ypos = bar_spacing
    xpos = label_width + pre_bar
    
    out = ""
    
    for i in range(len(types)):
        width = bar_width * (float(numbers[i]) / max(numbers))
        # bar
        out += '<rect x="%s" y="%s" width="%s" height="%s" style="stroke: none; fill: #efcc01" />' % (
            xpos,
            ypos,
            width,
            bar_height
        )
        
        # number
        out += '<text class="legend" x="%s" y="%s">%s</text>' % (
            xpos + width + 5,
            ypos + 9,
            force_escape(labels[i])
        )
        
        # type label
        out += '<text class="legend" x="%s" y="%s">%s</text>' % (
            0,
            ypos + 9,
            force_escape(types[i])
        )
        
        ypos += bar_height + bar_spacing
    
    out += '<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke: #444545; fill: none; stroke-width: 2pt;" />' % (
        label_width,
        0,
        label_width,
        len(types) * (bar_height + bar_spacing) + bar_spacing + 1.38
    )
    
    out += '<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke: #444545; fill: none; stroke-width: 2pt;" />' % (
        label_width,
        len(types) * (bar_height + bar_spacing) + bar_spacing,
        label_width + pre_bar + bar_width + dollar_width,
        len(types) * (bar_height + bar_spacing) + bar_spacing
    )
    
    return out

def ellipsize(val, length):
    if len(val) > length:
        return '%s...' % val[:length - 2]
    else:
        return val
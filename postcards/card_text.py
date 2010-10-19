from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Flowable, Spacer
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib import enums

from django.template import Context, Template
import postcards
from postcards.models import Postcard

from django.utils.html import strip_tags
import os, subprocess

address_format = "{{ name }}<br />{{ address1 }}{% if address2 %}<br />{{ address2 }}{% endif %}<br />{{ city }}, {{ state }} {{ zip }}"

class HR(Flowable):
    def __init__(self, thickness):
        self.line_thickness = thickness
    
    def wrap(self,availWidth, availHeight):
        self._width = availWidth
        self._height = self.line_thickness
        return self._width, self._height
    
    def draw(self):
        self.canv.setLineWidth(self.line_thickness)
        self.canv.line(0, .5 * self.line_thickness, self._width, .5 * self.line_thickness)


def render_card_pdf(card, filename):
    # set up styles
    regular = ParagraphStyle('default')
    regular.fontName = 'Helvetica'
    regular.fontSize = 9
    regular.leading = 11
    
    small = ParagraphStyle('default')
    small.fontName = 'Helvetica'
    small.fontSize = 7
    small.leading = 9
    
    large = ParagraphStyle('default')
    large.fontName = 'Helvetica'
    large.fontSize = 11
    large.leading = 13
    
    text = []
    
    # generate content
    address_template = Template(address_format)
    
    # return address
    text.extend([Paragraph(address_template.render(Context({
        'name': card.sender_name,
        'address1': card.sender_address1,
        'address2': card.sender_address2,
        'city': card.sender_city,
        'state': card.sender_state,
        'zip': card.sender_zip,
    })), small), Spacer(10, 10)])
    
    text.append(Paragraph(strip_tags(card.message).replace('\n', '<br />'), regular))
        
    text.extend([Spacer(10, 10), HR(0.5), Spacer(10, 10)])
    text.append(Paragraph('The Sunlight Foundation is a non-partisan non-profit that uses cutting-edge technology and ideas to make government transparent and accountable. Visit SunlightFoundation.com to learn more.', small))
    
    canv = Canvas(filename)
    canv.setPageSize((6.25 * inch, 4.5 * inch))
    
    f = Frame(0.375 * inch, 0.75 * inch, 3.125 * inch, 3.375 * inch, showBoundary=0)
    
    f.addFromList(text, canv)
    
    address = Frame(3.75 * inch, 1 * inch, 2 * inch, 1.5 * inch, showBoundary=0)
    address.addFromList([Paragraph(address_template.render(Context({
        'name': card.recipient_name,
        'address1': card.recipient_address1,
        'address2': card.recipient_address2,
        'city': card.recipient_city,
        'state': card.recipient_state,
        'zip': card.sender_zip,
    })), large)], canv)
    
    canv.save()

def get_card_pdf(card, invalidate=False):
    postcard_dir = os.path.dirname(postcards.__file__)
    pdf_dir = os.path.join(postcard_dir, 'static', 'messages', 'pdf')
    
    pdf_path = os.path.join(pdf_dir, "message_%s.pdf" % card.id)
    if not os.path.exists(pdf_path) or invalidate:
        render_card_pdf(card, pdf_path)
    return pdf_path

def render_card_png(card, png_path, invalidate=False):
    pdf = get_card_pdf(card, invalidate)
    mogrify = subprocess.Popen(['mogrify', '-format', 'png', '-density', '400', '-resize', '435x313', pdf])
    mogrify.wait()
    print '%s.png' % pdf[:-4], png_path
    os.rename('%s.png' % pdf[:-4], png_path)

def get_card_png(card, invalidate=False):
    postcard_dir = os.path.dirname(postcards.__file__)
    png_dir = os.path.join(postcard_dir, 'static', 'messages', 'png')
    
    png_path = os.path.join(png_dir, "message_%s.png" % card.id)
    
    if not os.path.exists(png_path) or invalidate:
        render_card_png(card, png_path, invalidate)
    return png_path
    
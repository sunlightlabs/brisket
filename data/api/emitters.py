from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson
from piston.emitters import Emitter
from dc_web.api.models import APIInvocation
from dcdata.contribution.models import NIMSP_TRANSACTION_NAMESPACE,\
    CRP_TRANSACTION_NAMESPACE
import csv
import datetime

class AmnesiacFile(object):
    def __init__(self):
        self.content = ""
    def write(self, chunk):
        self.content += chunk
    def read(self, size=None):
        value = self.content
        self.content = ""
        return value

class StatsLogger(object):
    def __init__(self):
        self.stats = { 'total': 0 }
    def log(self, record):
        ns = record['transaction_namespace']
        self.stats[ns] = self.stats.get(ns, 0) + 1
        self.stats['total'] += 1

class StreamingLoggingEmitter(Emitter):
    
    def stream(self, request, stats):
        raise NotImplementedError('please implement this method')
    
    def stream_render(self, request):
        
        stats = StatsLogger()
        
        if self.handler.fields:
            fields = self.handler.fields
        else:
            fields = self.data.model._meta.get_all_field_names()
            if self.handler.exclude:
                for field in self.handler.exclude:
                    fields.remove(field)
        
        for chunk in self.stream(request, fields, stats):
            yield chunk
            
        APIInvocation.objects.create(
            user=request.user,
            method=self.handler.__class__.__name__,
            query_string=request.META['QUERY_STRING'],
            total_records=stats.stats['total'],
            crp_records=stats.stats.get(CRP_TRANSACTION_NAMESPACE, 0),
            nimsp_records=stats.stats.get(NIMSP_TRANSACTION_NAMESPACE, 0),
            execution_time=0, # fill this out!!!
        )
        
            
class StreamingLoggingJSONEmitter(StreamingLoggingEmitter):    
    
    def stream(self, request, fields, stats):
        yield "["
        for record in self.data.values():
            stats.log(record)
            seria = simplejson.dumps(record, cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)
            yield seria + ","
        yield "]"

class StreamingLoggingCSVEmitter(StreamingLoggingEmitter):
    
    def stream(self, request, fields, stats):
        f = AmnesiacFile()
        writer = csv.DictWriter(f, fieldnames=fields)
        yield ",".join(fields) + "\n"
        for record in self.data.values(*fields):
            stats.log(record)
            writer.writerow(record)
            yield f.read()
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson
from piston.emitters import Emitter
from dc_web.api.middleware import RETURN_ENTITIES_KEY
from dc_web.api.models import Invocation
from matchbox.models import entityref_cache
from dcdata.contribution.models import NIMSP_TRANSACTION_NAMESPACE,\
    CRP_TRANSACTION_NAMESPACE
from time import time
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
        #ns = record['transaction_namespace']
        ns = record.get('transaction_namespace', 'unknown')
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
        
        if request.session.get(RETURN_ENTITIES_KEY, False):
            entity_fields = entityref_cache.get(self.handler.model, [])
            final_fields = fields + entity_fields
        else:
            final_fields = fields
        
        start_time = time()
        
        for chunk in self.stream(request, final_fields, stats):
            yield chunk

        print("emitter returned %s results in %s seconds." % (stats.stats['total'], time() - start_time))
            
        Invocation.objects.create(
            caller_key=request.apikey.key,
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
        count = 0
        for record in self.data.values():
            out_record = { }
            for f in fields:
                out_record[f] = record[f]
            stats.log(out_record)
            seria = simplejson.dumps(out_record, cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)
            if count == 0:
                yield seria
            else:
                yield "," + seria
            count += 1
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
            
            
from piston.emitters import Emitter
import csv

class AmnesiacFile(object):
    def __init__(self):
        self.content = ""
    def write(self, chunk):
        self.content += chunk
    def read(self, size=None):
        value = self.content
        self.content = ""
        return value
        

class CSVEmitter(Emitter):
    
    def stream_render(self, request):
        
        fields = self.data.model._meta.get_all_field_names()
        for field in self.handler.exclude:
            fields.remove(field)
        
        f = AmnesiacFile()
        writer = csv.DictWriter(f, fieldnames=fields)
        
        yield ",".join(fields) + "\n"
        
        for record in self.data.values(*fields):
            writer.writerow(record)
            yield f.read()
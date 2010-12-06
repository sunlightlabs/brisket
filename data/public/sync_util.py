import os
from django.conf import settings

def cache_fix(s):
    split = s.split(settings.MEDIASYNC['AWS_PREFIX'])
    if len(split) < 2:
        return ''
    rel = s.split(settings.MEDIASYNC['AWS_PREFIX'])[1][1:]
    rpath = os.path.join(settings.MEDIA_ROOT, rel)
    paths = []
    if os.path.exists(rpath):
        paths.append(rpath)
    else:
        JOINED = settings.MEDIASYNC.get('JOINED', {})
        print rpath, JOINED
        if rel in JOINED:
            paths.extend([os.path.join(settings.MEDIA_ROOT, p) for p in JOINED[rel]])
    times = []
    for path in paths:
        try:
            times.append(int(os.stat(path).st_mtime))
        except:
            pass
    print rpath, paths, times
    if times:
        return "t=%s" % max(times)
    else:
        return "t=%s" % 0

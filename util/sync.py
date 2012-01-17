import subprocess, os
git = subprocess.Popen('cd %s; git log -n 1 --raw --oneline' % os.path.dirname(os.path.abspath(__file__)), shell=True, stdout=subprocess.PIPE)
out, err = git.communicate()
__git_rev__ = out.split(' ')[0]

def git_cache_fix(s):
    return "g=%s" % __git_rev__

def cache_fix(s):
    from settings import MEDIASYNC, MEDIA_ROOT
    import os

    split = s.split(MEDIASYNC['AWS_PREFIX'])
    if len(split) < 2:
        return ''

    rel = s.split(MEDIASYNC['AWS_PREFIX'])[1][1:]
    if rel.endswith('.gz'):
        rel = rel[:-3]
    
    rpath = os.path.join(MEDIA_ROOT, rel)
    paths = []
    if os.path.exists(rpath):
        paths.append(rpath)
    else:
        JOINED = MEDIASYNC.get('JOINED', {})
        if rel in JOINED:
            paths.extend([os.path.join(MEDIA_ROOT, p) for p in JOINED[rel]])
    times = []
    for path in paths:
        try:
            times.append(int(os.stat(path).st_mtime))
        except:
            pass
    if times:
        return "t=%s" % max(times)
    else:
        return "t=%s" % 0

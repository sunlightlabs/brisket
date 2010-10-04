def single_map(value, istart, istop, ostart, ostop):
    try:
        return ostart + (ostop - ostart) * ((value - istart) / float(istop - istart))
    except ZeroDivisionError:
        return ostart

def list_map(l, ostart, ostop, istart=None, istop=None):
    if istart is None:
        istart = min(l)
    if istop is None:
        istop = max(l)
    return [single_map(v, istart, istop, ostart, ostop) for v in l]

def multi_list_map(ll, ostart, ostop):
    mins = [min(l) for l in ll]
    maxes = [max(l) for l in ll]
    istart = min(mins)
    istop = max(maxes)
    return [list_map(l, ostart, ostop, istart, istop) for l in ll]
from config import *
from sets import Set

def all_in(a, b):
    for x in a:
        if x not in b:
            return False
    return True

def nr_to_txt(cm):
    ret=[]
    for name, community in community_map.items():
        if all_in(community, cm):
            ret.append(name)

    return ' '.join(ret)

def extended(x):
    return x.startswith('target:') or x.startswith('origin:')

def not_extended(x):
    return not ( x.startswith('target:') or x.startswith('origin:') )

def txt_to_nr(cm):
    ret=[]
    cret=Set()
    xcret=Set()
    for x in cm:
        cret.update( filter(not_extended, community_map.get(x) ))
        xcret.update( filter(extended, community_map.get(x) ))
    
    if len(cret) > 0:
        ret.append('community [%s] ' % ' '.join(cret))

    if len(xcret) > 0:
        ret.append('extended-community [%s] ' % ' '.join(xcret))

    return ' '.join(ret)


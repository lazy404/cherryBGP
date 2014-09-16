from config import *
from sets import Set

def all_in(a, b):
    for x in a:
        if x not in b:
            return False
    return True

def nr_to_txt(cm):
    print 'nr to txt', cm

    ret=[]
    for name, community in community_map.items():
        if all_in(community, cm):
            ret.append(name)

    print 'nr_to_txt(%s) = %s' % (str(cm), str(ret))

    return ' '.join(ret)

def extended(x):
    return x.startswith('target:')
def not_extended(x):
    return not x.startswith('target:')

def txt_to_nr(cm):
    print 'txt to nr', cm
    ret=[]
    cret=Set()
    xcret=Set()
    for x in cm:
        cret.update( filter(not_extended, community_map.get(x) ))
        xcret.update( filter(extended, community_map.get(x) ))

    print 'txt_to_nr(%s) = %s %s' % (str(cm), str(cret),str(xcret))
    
    if cret:
        ret.append('community [%s] ' % ' '.join(cret))

    if cret:
        ret.append('extended-community [%s] ' % ' '.join(xcret))

    return ' '.join(ret)


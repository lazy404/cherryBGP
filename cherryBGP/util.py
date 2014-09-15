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

    return ' '.join(ret)

def txt_to_nr(cm):
    ret=Set()
    print 'txt nr', cm
    for x in cm:
        ret.update(community_map.get(x))

    return ' '.join(ret)

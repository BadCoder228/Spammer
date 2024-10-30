from random import shuffle, choice
from fake_useragent import UserAgent
import string


def randomed(arg=False):
    lits = []
    
    for i in range(7):
        toapp_l =[]
        
        for i in range(7):
            sym = list(string.ascii_letters+string.digits)
            shuffle(sym)
            toapp = ''.join(sym[:9])
            toapp_l.append(toapp)
       
        else:
            lits.append(''.join(toapp_l))
            
    return choice(lits) if arg else f'{choice(lits)}@gmail.com'


def useragent():
    return {'User-Agent' : UserAgent().random}, UserAgent().random

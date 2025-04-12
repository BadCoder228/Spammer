from random import choice
from fake_useragent import UserAgent
from string import ascii_letters


def randomed(arg=False):
    ranchars = []

    [ranchars.append(choice(ascii_letters)) for i in range(9)]
    
    return "".join(ranchars) if arg else f'{"".join(ranchars)}@gmail.com'


def useragent():
    return {'User-Agent' : UserAgent().random}, UserAgent().random

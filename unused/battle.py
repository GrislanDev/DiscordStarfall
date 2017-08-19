from random import randint

noa = 1000
nod = 800

mula = 1.1
muld = 1.25

while noa > 400 and nod > 240:
    atka = randint(0, int(noa * mula * 0.45))
    atkd = randint(0, int(nod * muld * 0.45))
    noa -= atkd
    nod -= atka
    print ("{0}, {1}, {2}, {3}".format(atka, atkd, noa, nod))

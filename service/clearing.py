import click
import re

from model import Hospital

handlers = ['name', 'coordinate']

def cleanHopsitalName():
    pattern = re.compile(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+")
    #  string = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+'"," ",line)

    for hos in Hospital.nodes:
        name = hos.name
        print("%s-%s" % (hos.sourceType, name))
        ns = re.sub(pattern, " ", name)
        nss = ns.split(' ')
        hos.fullName = name
        hos.name = nss[0]
        hos.nickName = ",".join(nss[1:])
        hos.save()


def cleanHospitalCoordinate():
    pass

@click.command()
@click.option('--handler', '-h', type=click.Choice(handlers), multiple=True)
def cleanHospital(handler):
    hs = handler if handler else handlers
    if 'name' in hs:
        cleanHopsitalName()
    if 'coordinate' in hs:
        cleanHospitalCoordinate()


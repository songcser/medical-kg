import click
import re

from model import Hospital, SOURCETYPE

handlers = ['name', 'coordinate']

def cleanHopsitalName():
    #  pattern = re.compile(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+")
    pattern = re.compile(r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+'")

    for docs in SOURCETYPE:
        for hos in Hospital.nodes.filter(sourceType=docs[0]):
            name = hos.fullName
            print("%s-%s" % (hos.sourceType, name))
            ns = re.sub(pattern, " ", name)
            nss = ns.split(' ')
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


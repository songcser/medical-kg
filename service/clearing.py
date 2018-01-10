import click
import re

from model import Hospital, SOURCETYPE

handlers = ['name', 'coordinate']

def cleanHopsitalName():
    #  pattern = re.compile(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+")
    #  pattern = re.compile(r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+'")
    pattern = re.compile(r"（(.+)）|\((.+)\)")

    for docs in SOURCETYPE:
        for hos in Hospital.nodes.filter(sourceType=docs[0]):
            name = hos.fullName
            print("%s-%s" % (hos.sourceType, name))
            ns = pattern.sub("", name)
            nss = pattern.findall(name)
            print(ns)
            print(nss)
            hos.name = ns
            if nss:
                hos.nickName = ",".join([ls for lss in nss for ls in lss if ls])
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


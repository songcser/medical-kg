import click
import re

from model import Hospital, SOURCETYPE

handlers = ['check', 'name', 'coordinate']

def checkHospitalName():
    pattern = re.compile(r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+'")
    for docs in SOURCETYPE:
        for hos in Hospital.nodes.filter(sourceType=docs[0]):
            name = hos.name
            nss = pattern.findall(name)
            if nss:
                print(name)
                print(hos.fullName)


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
    if 'check' in hs:
        checkHospitalName()
    if 'name' in hs:
        cleanHopsitalName()
    if 'coordinate' in hs:
        cleanHospitalCoordinate()

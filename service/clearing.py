import click
import re
import os

from geopy.geocoders import Baidu, GaoDe
from geopy.distance import vincenty
from model import Hospital, SOURCETYPE

sourceType = [t[0] for t in SOURCETYPE]
handlers = ['check', 'name', 'coordinate']
BAIDU_AK = os.environ.get('BAIDU_AK', "y8xcnaLtEwfxiGmA5GSBeoGzgtenFXLe")
GAODE_AK = os.environ.get('GAODE_AK', '923d3a373da95e6f2d20481b31a6873e')
baidu = Baidu(BAIDU_AK)
gaode = GaoDe(GAODE_AK)

def checkHospitalName(docs):
    pattern = re.compile(r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+'")
    for doc in docs or sourceType:
        for hos in Hospital.nodes.filter(sourceType=doc):
            name = hos.name
            nss = pattern.findall(name)
            if nss:
                print('%s--%s--%s--%s' % (doc, hos.name, hos.fullName, hos.nickName))


def cleanHopsitalName(docs):
    pattern = re.compile(r"（(.*?)）|\((.*?)\)| (.+?)|/(.+?)|\((.*?)|（(.*?)\)|,(.*?)|,(.*)|\.(.*)")

    for doc in docs or sourceType:
        for hos in Hospital.nodes.filter(sourceType=doc):
            name = hos.fullName if hos.fullName else hos.name
            name = name.strip()
            print("%s-%s" % (hos.sourceType, name))
            ns = pattern.sub("", name)
            nss = pattern.findall(name)
            hos.name = ns
            hos.fullName = name
            if nss:
                hos.nickName = ",".join([ls for lss in nss for ls in lss if ls])
            hos.save()

def distance(first, second):
    return vincenty(first, second).m

def getBaiduSearch(address, city=None):
    try:
        info = baidu.search(address, city=city, ret_coordtype='gcj02ll',
                            city_limit=True, timeout=20)
        return info
    except:
        return None


def getBaiduGeo(address, city=None):
    try:
        info = baidu.geocode(address, city=city, ret_coordtype='gcj02ll',
                            timeout=20)
        return info
    except:
        return None


def getBaiduCoordinate(hos):
    city = hos.getCity()
    print("Baidu: %s %s %s" % (hos.id, city.name, hos.name))
    g = getBaiduGeo(hos.name, city.name)
    s = getBaiduSearch(hos.name, city.name)
    d = distance((s.latitude, s.longitude),
                 (g.latitude, g.longitude)) if s and g else None
    hos.baiduCoordinate = {
        'sLongitude': s.longitude if s else None,
        'sLatitude': s.latitude if s else None,
        'gLongitude': g.longitude if g else None,
        'gLatitude': g.latitude if g else None,
        'distance': d,
    }
    print("Baidu -> %s" % hos.baiduCoordinate)

def getGaodeSearch(address, city=None):
    info = gaode.search(address, city=city, timeout=5)
    return info


def getGaodeGeo(address, city=None):
    info = gaode.geocode(address, city=city, timeout=5)
    return info


def getGaodeCoordinate(hos):
    city = hos.getCity()
    print("Gaode: %s %s" % (city.name, hos.name))
    g = getGaodeGeo(hos.name, city.name)
    s = getGaodeSearch(hos.name, city.name)
    d = distance((s.latitude, s.longitude),
                 (g.latitude, g.longitude)) if s and g else None
    hos.gaodeCoordinate = {
        'sLongitude': s.longitude if s else None,
        'sLatitude': s.latitude if s else None,
        'gLongitude': g.longitude if g else None,
        'gLatitude': g.latitude if g else None,
        'distance': d,
    }
    print("Gaode: %s" % hos.gaodeCoordinate)


def cleanHospitalCoordinate(docs):
    for doc in docs or sourceType:
        for hos in Hospital.nodes.filter(sourceType=doc):
            getBaiduCoordinate(hos)
            getGaodeCoordinate(hos)
            hos.save()


@click.command()
@click.option('--handler', '-h', type=click.Choice(handlers), multiple=True)
@click.option('--docs', '-d', type=click.Choice([doc[0] for doc in SOURCETYPE]), multiple=True)
def cleanHospital(handler, docs):
    hs = handler if handler else handlers
    if 'check' in hs:
        checkHospitalName(docs)
    if 'name' in hs:
        cleanHopsitalName(docs)
    if 'coordinate' in hs:
        cleanHospitalCoordinate(docs)

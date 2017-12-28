import click
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Search
from model import Hospital, Doctor, Province, City, District, \
    HospitalSimilarity, Department, HosDocRel, DoctorSimilarity

client = Elasticsearch('192.168.2.20:9200')

docs = ['qqyy', 'cnkang', 'yyk99', 'xywy', 'xsjk', 'familydoctor', 'haodf',
        'guahaowang']

def get_province(province):
    if not province:
        return None
    p = Province.nodes.get_or_none(name=province)
    if not p:
        p = Province(name=province).save()
    return p

def get_city(city, province):
    if not city:
        return None
    c = City.nodes.get_or_none(name=city)
    if not c:
        c = City(name=city).save()
        if province:
            c.province.connect(province)
    c.save()
    return c

def get_district(district, city):
    if not district:
        return None
    d = District.nodes.get_or_none(name=district)
    if not d:
        d = District(name=district).save()
        if city:
            d.city.connect(city)
    d.save()
    return d

def get_department(dep):
    if not dep:
        return None
    d = Department.nodes.get_or_none(name=dep)
    if not d:
        d = Department(name=dep).save()
    return d

@click.group()
def clis():
    pass

@click.command()
@click.option('--doc_types', '-d', type=click.Choice(docs), multiple=True)
def hospital(doc_types):
    for doc_type in doc_types:
        start, limit, i, err = 0, 500, 0, 0
        while True:
            try:
                s = Search(using=client, index="hospital-%s" % doc_type).sort()
                s = s[start:start+limit]
                res = s.execute()
                if s.count() == 0:
                    break
                for hit in res:
                    i += 1
                    print("%s--%s--%s" % (doc_type, i, hit.hospitalName))
                    h = Hospital.nodes.get_or_none(hid=hit.document_id)
                    if h: continue
                    data = hit.to_dict()
                    province = get_province(data.get('province', None))
                    city = get_city(data.get('city', None), province)
                    district = get_district(data.get('district', None), city)
                    h = Hospital(
                        hid=data['document_id'],
                        name=data['hospitalName'],
                        hType=data.get('hospitalType', None),
                        description=data['description'],
                        managementMode=data.get('managementMode', None),
                        sourceUrl=data.get('source_url', None),
                        sourceType=data.get('document_type', None),
                        #  province=data.get('province', None),
                        #  city=data.get('city', None),
                        #  district=data.get('district', None),
                        street=data.get('street', None),
                        place=data.get('place', None),
                        email=data.get('email', None),
                        direction=data.get('direction', None),
                        website=data.get('website', None),
                        level=data.get('level', None),
                        adcode=data.get('adcode', None),
                        streetNumber=data.get('streetNumber', None),
                        medicalInsurance=data.get('medicalInsurance', None),
                        telephone=data.get('telephone', None),
                    ).save()
                    if province:
                        h.province.connect(province)
                    if city:
                        h.city.connect(city)
                    if district:
                        h.district.connect(district)
                    depClass = data.get('departmentClass', None)
                    if not depClass:
                        continue
                    for deplist in depClass:
                        deps = deplist.get('departments', None)
                        if not deps:
                            continue
                        for dep in deps:
                            d = get_department(dep['name'])
                            if not d:
                                continue
                            h.departments.connect(d)
                    h.save()
                    del data
                start += limit
            except Exception as e:
                print(e)
                err += 1
                if err > 10:
                    break


@click.command()
@click.option('--doc_types', '-d', type=click.Choice(docs), multiple=True)
def doctor(doc_types):
    for doc_type in doc_types:
        start, limit, i, err = 0, 500, 0, 0
        while True:
            try:
                s = Search(using=client, index="doctor-%s" % doc_type).sort()
                s = s[start:start+limit]
                res = s.execute()
                if s.count() == 0:
                    break
                for hit in res:
                    i += 1
                    print("%s--%s--%s" % (doc_type, i, hit.name))
                    d = Doctor.nodes.get_or_none(did=hit.document_id)
                    if d: continue
                    data = hit.to_dict()
                    goodat = data.get('goodat', None)
                    description = data.get('description', None)
                    sex = data.get('sex', None),
                    d = Doctor(
                        did=data['document_id'],
                        name=data['name'],
                        goodat="".join(goodat.split()) if goodat else None,
                        sex=''.join(sex.split()) if sex and isinstance(sex, str) else None,
                        description=''.join(description.split()) if description and isinstance(description, str) else None,
                        title=data.get('title', None),
                        sourceUrl=data.get('source_url', None),
                        sourceType=data.get('document_type'),
                        headerUrl=data.get('headerUrl', None),
                    ).save()
                    hs = data.get('hospitals', [])
                    deps = []
                    for h in hs:
                        deps.extend(h['departments'])
                        hos = Hospital.nodes.get_or_none(hid=h['hospital_id'])
                        if hos:
                            d.hospital.connect(hos, {
                                'department': ','.join(h['departments'])
                            })
                    if deps:
                        department = get_department(deps[0])
                        if department:
                            d.department.connect(department)
                    province = get_province(data.get('province', None))
                    city = get_city(data.get('city', None), province)
                    if province:
                        d.province.connect(province)
                    if city:
                        d.city.connect(city)
                    d.save()
                    del data
                start += limit
            except Exception as e:
                print(e)
                err += 1
                if err > 10:
                    break

clis.add_command(hospital)
clis.add_command(doctor)

if __name__ == "__main__":
    clis()

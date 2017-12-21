from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from model import Hospital, Doctor

client = Elasticsearch('192.168.2.20:9200')


def import_hospital(doc_type):
    s = Search(using=client, index="hospital-*")
    s = s.query('match', document_type=doc_type)
    i = 0
    for hit in s.scan():
        i += 1
        print(hit.hospitalName)
        print(i)
        h = Hospital.nodes.get_or_none(hid=hit.document_id)
        if h: continue
        data = hit.to_dict()
        h = Hospital(
            hid=data['document_id'],
            name=data['hospitalName'],
            hType=data.get('hospitalType', None),
            description=data['description'],
            managementMode=data.get('managementMode', None),
            sourceUrl=data.get('source_url', None),
            sourceType=data.get('document_type', None),
            province=data.get('province', None),
            city=data.get('city', None),
            district=data.get('district', None),
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


def import_doctor(doc_type):
    s = Search(using=client, index="doctor-*")
    s = s.query('match', document_type=doc_type)
#  hits = s.execute()
    for hit in s.scan():
        print(hit.name)
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
            province=data.get('province', None),
            sex=''.join(sex.split()) if sex and isinstance(sex, str) else None,
            city=data.get('city', None),
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
        d.department = deps
        d.save()


if __name__ == "__main__":
    docs = ['qqyy', 'cnkang', 'yyk99', 'xywy', 'xsjk', 'familydoctor', 'haodf',
            'guahaowang']
    for doc in docs:
        print("Import: %s" % doc)
        import_hospital(doc)
        import_doctor(doc)

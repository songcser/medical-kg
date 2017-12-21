from neomodel import config
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom, FloatProperty,
                      StructuredRel, ArrayProperty)

config.DATABASE_URL = 'bolt://neo4j:admin@neo4j:7687'

class HospitalSimilarity(StructuredRel):
    similarity = FloatProperty()
    coordDistance = IntegerProperty()
    province = StringProperty()
    city = StringProperty()
    district = StringProperty()

class Hospital(StructuredNode):
    SOURCETYPE = (
        ('qqyy', "中国医院大全"),
        ('zhizhuwang', "蜘蛛网"),
        ('cnkang', "中华康网"),
        ('yyk99', "99健康网"),
        ('yixuebaike', "医学百科"),
        ('xywy', "寻医问药"),
        ('xsjk', "携手健康网"),
        ('familydoctor', "家庭医生在线"),
        ('mapbar', "图吧"),
        ('haodf', "好大夫在线"),
        ('guahaowang', "挂号网"),
    )
    hid = UniqueIdProperty()
    name = StringProperty()
    hType = StringProperty()
    description = StringProperty()
    managementMode = StringProperty()
    sourceUrl = StringProperty()
    sourceType = StringProperty(choices=SOURCETYPE)
    province = StringProperty()
    city = StringProperty()
    district = StringProperty()
    street = StringProperty()
    place = StringProperty()
    email = StringProperty()
    direction = StringProperty()
    website = StringProperty()
    level = StringProperty()
    adcode = StringProperty()
    streetNumber = StringProperty()
    medicalInsurance = StringProperty()
    telephone = StringProperty()
    longitude = FloatProperty()
    latitude = FloatProperty()
    aimilarity = RelationshipTo('Hospital', "HOSPITALSIMILARITY",
                                model=HospitalSimilarity)

class HosDocRel(StructuredRel):
    department = StringProperty()

class DoctorSimilarity(StructuredRel):
    similarity = FloatProperty()
    department = StringProperty()

class Doctor(StructuredNode):
    did = UniqueIdProperty()
    name = StringProperty()
    goodat = StringProperty()
    province = StringProperty()
    city = StringProperty()
    sex = StringProperty()
    description = StringProperty()
    title = StringProperty()
    sourceUrl = StringProperty()
    sourceType = StringProperty()
    headerUrl = StringProperty()
    department = ArrayProperty()
    hospital = RelationshipTo(Hospital, 'WORKIN', model=HosDocRel)

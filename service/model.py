from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
        UniqueIdProperty, RelationshipTo, RelationshipFrom, FloatProperty,
        StructuredRel, ArrayProperty, Relationship, JSONProperty)

config.DATABASE_URL = 'bolt://neo4j:admin@neo4j:7687'
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

class Province(StructuredNode):
    name = StringProperty(unique_index=True)

class City(StructuredNode):
    name = StringProperty(unique_index=True)
    province = RelationshipTo(Province, "CityProvinceRel")

class District(StructuredNode):
    name = StringProperty(unique_index=True)
    city = RelationshipTo(City, "DistrictCityRel")

class HospitalSimilarity(StructuredRel):
    similarity = FloatProperty()
    coordDistance = IntegerProperty()
    province = StringProperty()
    city = StringProperty()
    district = StringProperty()

class Hospital(StructuredNode):
    hid = UniqueIdProperty()
    name = StringProperty()
    nickName = StringProperty()
    fullName = StringProperty()
    hType = StringProperty()
    description = StringProperty()
    managementMode = StringProperty()
    sourceUrl = StringProperty()
    sourceType = StringProperty(choices=SOURCETYPE)
    province = RelationshipTo(Province, "HosptialProvinceRel")
    city = RelationshipTo(City, "HospitalCityRel")
    district = RelationshipTo(District, "HospitalDistrictRel")
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
    baiduCoordinate = JSONProperty()
    gaodeCoordinate = JSONProperty()
    aimilarity = Relationship('Hospital', "HospitalAimilarity",
                                model=HospitalSimilarity)
    departments = Relationship('Department', "HospitalDepartmentRel")

    def getCity(self):
        query = "MATCH (a) WHERE id(a)={self}MATCH (a)-[:HospitalCityRel]->(b) RETURN b"
        results, columns = self.cypher(query)
        return City().inflate(results[0][0]) if results else None

class Department(StructuredNode):
    name = StringProperty()

class HosDocRel(StructuredRel):
    department = StringProperty()

class DoctorSimilarity(StructuredRel):
    similarity = FloatProperty()
    department = StringProperty()

class Doctor(StructuredNode):
    did = UniqueIdProperty()
    name = StringProperty()
    goodat = StringProperty()
    province = RelationshipTo(Province, "DoctorProvinceRel")
    city = RelationshipTo(City, "DoctorCityRel")
    sex = StringProperty()
    description = StringProperty()
    title = StringProperty()
    sourceUrl = StringProperty()
    sourceType = StringProperty()
    headerUrl = StringProperty()
    department = RelationshipTo(Department, "WorkInDepartment")
    hospital = RelationshipTo(Hospital, 'WorkInHospital', model=HosDocRel)

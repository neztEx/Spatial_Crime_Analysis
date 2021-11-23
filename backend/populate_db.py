from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from geoalchemy2 import Geometry
from sqlalchemy.event import listen
from sqlalchemy.sql import select, func
from sqlalchemy.ext.declarative import declarative_base

import platform
import sys



def load_spatialite(dbapi_conn, connection_record):
  dbapi_conn.enable_load_extension(True)
  print(platform.system())
  if(platform.system() == 'Darwin'):
    dbapi_conn.load_extension('/opt/homebrew/Cellar/libspatialite/5.0.1_1/lib/mod_spatialite.dylib')
  elif(platform.system() == 'Linux'):
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')
  else:  
    print('Unable to assess OS type')
    sys.exit()

engine = create_engine('sqlite:///gis.db', echo=True)
listen(engine, 'connect', load_spatialite)

conn = engine.connect()
conn.execute(select([func.InitSpatialMetaData()]))
conn.close()

Base = declarative_base()
class Crime(Base):
  __tablename__ = 'crime'
  id = Column(Integer, primary_key=True)
  DR_NO = Column(Integer)
  Date_Rptd = Column(Date)
  DATE_OCC = Column(Date)
  TIME_OCC = Column(Time)
  AREA = Column(Integer)
  AREA_NAME = Column(String)
  Rpt_Dist_No = Column(Integer)
  Part_1_2 = Column(Integer)
  Crm_Cd = Column(Integer)
  Crm_Cd_Desc = Column(String)
  Mocodes = Column(String)
  Vict_Age = Column(Integer)
  Vict_Sex = Column(String)
  Vict_Descent = Column(String)
  Premis_Cd = Column(Integer)
  Premis_Desc = Column(String)
  Weapon_Used_Cd = Column(Integer)
  Weapon_Desc = Column(String)
  Status = Column(String)
  Status_Desc = Column(String)
  Crm_Cd_1 = Column(Integer)
  Crm_Cd_2 = Column(Integer)
  Crm_Cd_3 = Column(Integer)
  Crm_Cd_4 = Column(Integer)
  LOCATION = Column(String)
  Cross_Street = Column(String)
  LAT_LON = Column(Geometry(geometry_type='POINT'))

  DR_NO,  Date_Rptd,  DATE_OCC,  TIME_OCC,  AREA ,  AREA_NAME,  Rpt_Dist_No ,  Part_1_2 ,  Crm_Cd ,  Crm_Cd_Desc,  Mocodes,  Vict_Age ,  Vict_Sex,  Vict_Descent,  Premis_Cd ,  Premis_Desc,  Weapon_Used_Cd ,  Weapon_Desc, Status,  Status_Desc,  Crm_Cd_1 ,  Crm_Cd_2 ,  Crm_Cd_3 ,  Crm_Cd_4 ,  LOCATION, Cross_Street, LAT_LON
  def __init__(self, DR_NO,  Date_Rptd,  DATE_OCC,  TIME_OCC,  AREA ,  AREA_NAME,  Rpt_Dist_No ,  Part_1_2 ,  Crm_Cd ,  Crm_Cd_Desc,  Mocodes,  Vict_Age ,  Vict_Sex,  Vict_Descent,  Premis_Cd ,  Premis_Desc,  Weapon_Used_Cd ,  Weapon_Desc, Status,  Status_Desc,  Crm_Cd_1 ,  Crm_Cd_2 ,  Crm_Cd_3 ,  Crm_Cd_4 ,  LOCATION, Cross_Street, LAT_LON):
    self.DR_NO = DR_NO
    self.Date_Rptd = Date_Rptd
    self.DATE_OCC = DATE_OCC
    self.TIME_OCC = TIME_OCC
    self.AREA = AREA
    self.AREA_NAME = AREA_NAME
    self.Rpt_Dist_No = Rpt_Dist_No
    self.Part_1_2 = Part_1_2
    self.Crm_Cd = Crm_Cd
    self.Crm_Cd_Desc = Crm_Cd_Desc
    self.Mocodes = Mocodes
    self.Vict_Age = Vict_Age
    self.Vict_Sex = Vict_Sex
    self.Vict_Descent = Vict_Descent
    self.Premis_Cd = Premis_Cd
    self.Premis_Desc = Premis_Desc
    self.Weapon_Used_Cd = Weapon_Used_Cd
    self.Weapon_Desc = Weapon_Desc
    self.Status = Status
    self.Status_Desc = Status_Desc
    self.Crm_Cd_1 = Crm_Cd_1
    self.Crm_Cd_2 = Crm_Cd_2
    self.Crm_Cd_3 = Crm_Cd_3
    self.Crm_Cd_4 = Crm_Cd_4
    self.LOCATION = LOCATION
    self.Cross_Street = Cross_Street
    self.LAT_LON = LAT_LON


'''
import csv


conn = engine.connect()
with open('../dataset/crime_data.csv') as csvfile:
  crime_data = csv.reader(csvfile)
  
  for i, row in enumerate(crime_data):
    print(len(row))
    if(i != 0):
      datum = Crime(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26]+ row[27] )
    conn.execute()
conn.close()
'''

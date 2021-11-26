from sqlalchemy import create_engine, event, Column, Integer, String, Date, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.event import listen
from sqlalchemy.sql import select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from datetime import datetime, date

import platform
import sys


def load_spatialite(dbapi_conn, connection_record):
  dbapi_conn.enable_load_extension(True)
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
  DATE_TIME_OCC = Column(DateTime)
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
  LAT_LON = Column(Geometry(geometry_type='POINT', management=True))

  def __init__(self, DR_NO,  Date_Rptd,  DATE_TIME_OCC,  AREA ,  AREA_NAME,  Rpt_Dist_No ,  Part_1_2 ,  Crm_Cd ,  Crm_Cd_Desc,  Mocodes,  Vict_Age ,  Vict_Sex,  Vict_Descent,  Premis_Cd ,  Premis_Desc,  Weapon_Used_Cd ,  Weapon_Desc, Status,  Status_Desc,  Crm_Cd_1 ,  Crm_Cd_2 ,  Crm_Cd_3 ,  Crm_Cd_4 ,  LOCATION, Cross_Street, LAT_LON):
    self.DR_NO = DR_NO
    self.Date_Rptd = Date_Rptd
    self.DATE_TIME_OCC = DATE_TIME_OCC
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


Crime.__table__.create(engine)


Session = sessionmaker(bind=engine)
session = Session()

import csv

with open('../dataset/crime_data.csv') as csvfile:
  crime_data = csv.reader(csvfile)
  
  for i, row in enumerate(crime_data):
    if(i != 0):
      print("HOUR: " + row[3][0:2])
      print("MINUTE: " + row[3][2:])
      datum = Crime(int(row[0]),      #DR_NO
          date(int(row[1][6:10]), int(row[1][0:2]), int(row[1][3:5])),      #Date_Rptd
          datetime(int(row[2][6:10]), int(row[2][0:2]), int(row[2][3:5]), hour=int(row[3][0:2]), minute=int(row[3][2:])),  #Date_Time_OCC
          int(row[4]),                #Area
          row[5],                     #Area_Name
          int(row[6]),                #Rpt_dist_no
          int(row[7]),                #part_1_2
          -1 if row[8] == '' else int(row[8]),                #Crm_cd
          row[9],                     #Crm_cd_desc
          row[10],                    #Mocodes
          -1 if row[11] == '' else int(row[11]),               #vict_age
          row[12],                    #vict_sex
          row[13],                    #vict_descent
          -1 if row[14] == '' else int(row[14]),               #premis_cd
          row[15],                    #premis_desc
          -1 if row[16] == '' else int(row[16]),               #weapon_used_cd
          row[17],                    #weapon_desc
          row[18],                    #status
          row[19],                    #status_desc
          -1 if row[20] == '' else int(row[20]),               #crm_cd_1
          -1 if row[21] == '' else int(row[21]),               #crm_cd_2
          -1 if row[22] == '' else int(row[22]),               #crm_cd_3
          -1 if row[23] == '' else int(row[23]),               #crm_cd_4
          row[24],                    #Location
          row[25],                    #Cross_street
          'POINT('+row[26] + ' ' + row[27] + ')' )         #Lat_lon
      
      session.add(datum)
      session.commit()

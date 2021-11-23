from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.sql import select, func
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

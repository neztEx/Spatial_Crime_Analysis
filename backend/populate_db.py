from sqlalchemy import create_engine
from sqlalchemy.event import listen


def load_spatialite(dbapi_conn, connection_record):
  dbapi_conn.enable_load_extension(True)
  dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')

engine = create_engine('sqlite:///gis.db', echo=True)
listen(engine, 'connect', load_spatialite)

conn = engine.connect()
conn.execute(select([func.InitSpatialMetaData()]))
conn.close()

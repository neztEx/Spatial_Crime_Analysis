# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# MySQLdb module written by Andy Dustman, documentation at http://mysql-python.sourceforge.net/MySQLdb.html
# GeoSearch crawler written by Chris Cantey, MS GIS/Cartography, University of Wisconsin, https://geo-odyssey.com
# MwSQLdb schema written with great assistance from Steve Hemmy, UW-Madison DoIT
from keywords import crimeTypeArr

from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream
import time
# import MySQLdb
import csv
import random
import os
from dotenv import load_dotenv


# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret as well as the access_token and secret will be generated for you after you register with Twitter Developers
load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

# Create your MySQL schema and connect to database, ex: mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpwd');
# db=MySQLdb.connect(host='localhost', user='root', passwd='newpwd', db='twitter') 
# db.set_character_set('utf8')

Coords = dict()
XY = []
# curr=db.cursor()

#per request, write output to csv, rather than mysql. Be aware of limited rows to csv. The streaming API will return millions of rows per day.
# csvfile = open('../dataset/geopy_results.csv','a')
# csvwriter = csv.writer(csvfile)


class StdOutListener(StreamListener):
    """ A listener handles tweets that are the received from the stream. 
    This is a basic listener that inserts tweets into MySQLdb.
    """
    def on_status(self, status):
        
        print("Tweet Text: "+status.text, status.place, status.coordinates)
        print("GOT HERE")
        text = status.text
        csvfile = open(os.path.join(os.getcwd(),'..','./dataset/tweetsGeo.csv'), 'a')

        try:
            Coords.update(status.coordinates)
            XY = (Coords.get('coordinates'))  #Place the coordinates values into a list 'XY'
            #print "X: ", XY[0]
            #print "Y: ", XY[1]
            #Alternatively write to CSV. CSV's. limited
            writer = csv.writer(csvfile)
            writer.writerow([
                # unicode(status.id_str).encode("utf-8"),unicode(status.created_at).encode("utf-8"),XY[1],XY[0],unicode(status.text).encode("utf-8")])
                status.id_str,
                status.id,
                status.author.screen_name,
                XY[1],
                XY[0],
                status.text,
                status.place,
                ['#{}'.format(hashtag['text']) for hashtag in status.entities['hashtags']]
            ])
        except:
            print("ERROR!!")
            #Often times users opt into 'place' which is neighborhood size polygon
            #Calculate center of polygon
            Box = status.place.bounding_box.coordinates[0]                                    
            XY = [(Box[0][0] + Box[2][0])/2, (Box[0][1] + Box[2][1])/2]
            #print "X: ", XY[0]
            #print "Y: ", XY[1] 
            #Alternatively write to CSV. CSV's. limited
            writer = csv.writer(csvfile)
            writer.writerow([
                # unicode(status.id_str).encode("utf-8"),unicode(status.created_at).encode("utf-8"),XY[1],XY[0],unicode(status.text).encode("utf-8")])
                status.id_str,
                status.id,
                status.author.screen_name,
                XY[1],
                XY[0],
                status.text,
                status.place,
                ['#{}'.format(hashtag['text']) for hashtag in status.entities['hashtags']]
            ])
            # pass
        # Comment out next 4 lines to avoid MySQLdb to simply read stream at console
        # curr.execute("""INSERT INTO TwitterFeed2 (UserID, Date, Lat, Lng, Text) VALUES
        #     (%s, %s, %s, %s, %s);""",
        #     (status.id_str,status.created_at,XY[1],XY[0],text))
        # db.commit()
                      

def main():
    l = StdOutListener()    
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    stream = Stream(auth, l, timeout=30.0)
    #Only records 'locations' OR 'tracks', NOT 'tracks (keywords) with locations'
    while True:
        try:
            # Call tweepy's userstream method 
            # Use either locations or track, not both
            # -118.5978,33.7052,-117.3056,34.2981 <- LA area
            stream.filter(locations=[-118,33,-117,34])##These coordinates are approximate bounding box around USA
            #stream.filter(track=['obama'])## This will feed the stream all mentions of 'keyword' 
            break
        except Exception as e:
             # Abnormal exit: Reconnect
             nanoSeconds=random.randint(60,63)
             time.sleep(nanoSeconds)            

if __name__ == '__main__':
    main()
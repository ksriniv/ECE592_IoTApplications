import math
import csv
import sqlite3
from random import randint
import sys
database = 'ZeroInitialized.db'
def eucledian_dist(x,y):
    temp = location[0][0]- float(x)
    ans1 = math.pow(temp,2)
    ans2 = math.pow(location[0][1]-float(y),2)
    answer = math.pow(ans1+ans2,0.5)
    return answer

def update_data():
    c.execute("UPDATE AmbientLight SET ambientlight = ? WHERE gpsvalue = ? AND timesegment = ?" ,
          (ambientlight, gpsvalue, timesegment))
    conn.commit()
    c.close()
    conn.close()


with open('./csv/all_waypoints.csv') as f:
    waypoints=[tuple(line) for line in csv.reader(f)]

for i in range(0,len(waypoints)):
    x,y = waypoints[i]
    waypoints[i] = float(x),float(y)


test_location = [waypoints[randint(0,430)]]
test_val = randint(0,255)
test_timesegment = str(sys.argv[4]).zfill(4)

## These should be taken from user input
location = [(float(sys.argv[1]),float(sys.argv[2]))]
#print(sys.argv[0],sys.argv[1])
#location = [(35.769937, -78.676704)]
ambientlight = sys.argv[3]
timesegment = test_timesegment
print("Input Location: ",location)
print("Input Ambient Light: ", ambientlight)

distance_vector = []
for (x,y) in waypoints:
    answer = [eucledian_dist(x,y)*1000000]
    distance_vector = distance_vector + answer
#print (min(distance_vector))
if min(distance_vector) < 100:
    closest_point = distance_vector.index(min(distance_vector))
    gpsvalue = str([repr(waypoints[closest_point][0]), repr(waypoints[closest_point][1])])

    conn = sqlite3.connect(database)
    c = conn.cursor()

    update_data()
    print("Light Data updated at location: ", gpsvalue)
else:
    print("Input point is not part of map. Data not stored")

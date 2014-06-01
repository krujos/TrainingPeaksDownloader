import xmltodict
import requests
#First, go shove your user info into: http://www.trainingpeaks.com/tpwebservices/service.asmx?op=GetWorkoutsForAthlete
#and copy the resulting xml into tpworkouts.xml..

doc = xmltodict.parse(open('tpworkouts.xml').read())

workouts = doc['ArrayOfWorkout']['Workout']

count = 0
total_miles = 0
ids = []
#The best / only way I could figure out the Training Peaks PersonID was to go to the old (flex) UI, and try to print
#the workout calendar. It will have the person ID in the URL.
personid = str(ID_GOES_HERE)
username = ''
password = ''

for workout in workouts:
    if "Bike" != workout['WorkoutTypeDescription']:
        continue

    if '@xsi:nil' in workout['TimeTotalInSeconds']:
        continue

    print workout['WorkoutDay'], workout['WorkoutId'], workout['WorkoutTypeDescription'], int(
        workout['TimeTotalInSeconds']) / 60, ' min long'

    if '@xsi:nil' in workout['DistanceInMeters']:
        if '@xsi:nil' in workout['PowerAverage']:
            #No Power, was either the track or something I don't care about.
            continue

    else:
        miles = (float(workout['DistanceInMeters']) / 1609.3)
        print "%f miles" % miles
        total_miles += miles

    count += 1
    ids.append(workout['WorkoutId'])

print "You have %d workouts to deal with over %f miles " % (count, total_miles)

for workout_id in ids:
    r = requests.post("http://www.trainingpeaks.com/tpwebservices/service.asmx/GetExtendedWorkoutsForAccessibleAthlete",
                     data={'password': password, 'personId': personid, 'username': username, 'workoutIds': workout_id})
    pwx = open('pwx/' + str(workout_id) + '.pwx', "w")
    pwx.write(r.text)
    pwx.close()

#you now have all your stuff in the ./pwx directory. use http://pwx.raytracer.dk/ to convert them.
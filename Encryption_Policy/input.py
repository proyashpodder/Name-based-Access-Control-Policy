from nltk.corpus import words
import random
from collections import defaultdict
import os
import subprocess
import csv


def input_schema_generator():
    a = words.words()
    for numpub in range(2,11):
        fileName='input_schema/pubnum_'+str(numpub)+'.txt'
        f = open(fileName,"w")
        f.write('_network: "Home"')
        f.write('\n')

        f.write('#pub: _network/$location/events/value ENCRYPTEDBY [_network, _network/location] WHERE {location: "bedroom" | "livingroom"}')
        #f.write("#pub: home/$location/events/value")
        f.write('\n')
        
        for i in range(numpub+1):
            pubName = random.choice([x for x in a if (len(x) == 5)])
            #pub = pubName + ': '
            tmpWord = random.choice([x for x in a if (len(x) == 5)])
            
            f.write(pubName+ ' : #pub ENCRYPTEDBY [location] WHERE {location:" '+tmpWord+'"}')
            f.write('\n')

def result():
    with open('enc.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Number of Publications', 'Compilation Time'])
        for numpub in range(2,11):
            print(numpub)
            cmd = "time python3 run.py input_schema/pubnum_"+str(numpub)+".txt"
            a = os.system(cmd)
            print(a)
#input_schema_generator()
result()



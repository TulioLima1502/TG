import h5py
import random
from subprocess import call
import os

TrainData = [
    './extract-bagfiles/primeiro.h5',
    './extract-bagfiles/segundo.h5',
]

if os.path.isfile("TrainData.txt") is True:
    os.remove("TrainData.txt")
if os.path.isfile("TestData.txt") is True:
    os.remove("TestData.txt")

RandomData = []
RandomDataTrain = []
RandomDataTest = []

identifier = 0
for path in TrainData:
    try:
        with h5py.File(path, "r") as archive:
            index = archive["X"]
            identifier += index.shape[0]
            #print identifier

    except IOError:
        print "Failed"

TrainDataSize = int(identifier * 0.7)
TestDataSize = int(identifier * 0.3)

for i in range(0,identifier):
    RandomData.append(str(i))

print TrainDataSize, TestDataSize
#print RandomData

i=0
for i in range(0,TrainDataSize):
    
    RandomNumber = random.randint(0,identifier)
    while str(RandomNumber) not in RandomData:
        RandomNumber = random.randint(0,identifier)
    
    if str(RandomNumber) in RandomData:
        #print RandomNumber
        RandomData.remove(str(RandomNumber))
        RandomDataTrain.append(RandomNumber)
    i += 1

RandomDataTest = RandomData

#print sorted(RandomDataTrain)
#print sorted(RandomDataTest)
#print len(RandomDataTrain), TrainDataSize

DataFileTrain = open("TrainData.txt", "w")
for word in sorted(RandomDataTrain):
    DataFileTrain.write(str(word) +'\n')
DataFileTrain.close()

DataFileTest = open("TestData.txt", "w")
for word in RandomDataTest:
    DataFileTest.write(word+'\n')
DataFileTest.close()

call('nohup ./server.py --batch 50 --port 5557 --validation --list TrainData.txt &',shell=True)
call('nohup ./server.py --batch 50 --port 5556 --list TestData.txt &', shell=True)


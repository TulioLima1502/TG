import h5py
import random
from subprocess import call
import os

TrainData = [
    './extract-bagfiles/retas_1.h5',
    './extract-bagfiles/retas_2.h5',
    './extract-bagfiles/curvas_suaves_1.h5',
    './extract-bagfiles/curvas_suaves_2.h5',
    './extract-bagfiles/curvas_em_T_1.h5',
]

if os.path.isfile("TrainData.txt") is True:
    os.remove("TrainData.txt")
if os.path.isfile("TestData.txt") is True:
    os.remove("TestData.txt")
if os.path.isfile("ValidationData.txt") is True:
    os.remove("ValidationData.txt")

RandomData = []
RandomDataTrain = []
RandomDataTest = []
RandomDataValidation = []

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
TestDataSize = int(identifier * 0.15)
ValidationDataSize = int(identifier * 0.15)

for i in range(0,identifier):
    RandomData.append(str(i))

print TrainDataSize, TestDataSize, ValidationDataSize
#print RandomData

i=0
for i in range(0,TrainDataSize):
    secure_random = random.SystemRandom()
    RandomNumber = secure_random.choice(RandomData)
    while str(RandomNumber) not in RandomData:
        RandomNumber = random.choice(RandomData)
    
    if str(RandomNumber) in RandomData:
        #print RandomNumber
        RandomData.remove(str(RandomNumber))
        RandomDataTrain.append(RandomNumber)
    i += 1

for i in range(0,TestDataSize):
    secure_random = random.SystemRandom()
    RandomNumber = secure_random.choice(RandomData)
    while str(RandomNumber) not in RandomData:
        RandomNumber = random.choice(RandomData)
    
    if str(RandomNumber) in RandomData:
        #print RandomNumber
        RandomData.remove(str(RandomNumber))
        RandomDataTest.append(RandomNumber)
    i += 1

RandomDataValidation = RandomData

#print sorted(RandomDataTrain)
#print sorted(RandomDataTest)
#print sorted(RandomDataValidation)
#print len(RandomDataTrain), TrainDataSize

DataFileTrain = open("TrainData.txt", "w")
for word in RandomDataTrain:
    DataFileTrain.write(str(word) +'\n')
DataFileTrain.close()

DataFileTest = open("TestData.txt", "w")
for word in RandomDataTest:
    DataFileTest.write(str(word)+'\n')
DataFileTest.close()

DataFileValidation = open("ValidationData.txt", "w")
for word in RandomDataValidation:
    DataFileValidation.write(str(word)+'\n')
DataFileValidation.close()

exit()

call('nohup ./server.py --batch 50 --port 5557 --validation --list TrainData.txt &',shell=True)
call('nohup ./server.py --batch 50 --port 5556 --list TestData.txt &', shell=True)


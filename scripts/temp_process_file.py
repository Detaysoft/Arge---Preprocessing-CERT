import glob

extractedFileWriteDir = "..\\datasets\\CERT\\r4.2\\featureExtractedDataset\\"

freadfeature = open(extractedFileWriteDir + "extractedDatasetSeq.csv","r")
freadfeature.readline()
minD = 24123123
maxD = 0
line=1

for sample in freadfeature:
    sample = sample.replace("\n","")
    samplesp = sample.split(",")
    actionSequence = samplesp[8]
    actionSequencesp = actionSequence.split("-")
    if len(actionSequencesp) < minD:
        minD = len(actionSequencesp)
        print(samplesp[0])
    line+=1
print(minD)
"""
for sample in freadfeature:
    sample = sample.replace("\n","")
    samplesp = sample.split(",")
    dur1 = float(samplesp[8])
    dur2 = float(samplesp[9])
    
    if dur1 + dur2 != 0:
    
        if dur1 + dur2 < minD:
            minD = dur1 + dur2
        if dur1 + dur2 > maxD:
            maxD = dur1 + dur2
    line+=1
print(minD,maxD)  

answerFileDir = "..\\datasets\\CERT\\answers\\"
maliciousFileList = glob.glob(answerFileDir + "r4.2-1\\*")

tot1 = tot2 = tot3 = 0
for fName in maliciousFileList:
    maliciousActionFile = open(fName,"r")
    for seq in maliciousActionFile:
        tot1+=1

maliciousFileList = glob.glob(answerFileDir + "r4.2-2\\*")

for fName in maliciousFileList:
    maliciousActionFile = open(fName,"r")
    for seq in maliciousActionFile:
        tot2+=1
        
maliciousFileList = glob.glob(answerFileDir + "r4.2-3\\*")
for fName in maliciousFileList:
    maliciousActionFile = open(fName,"r")
    for seq in maliciousActionFile:
        tot3+=1

print(tot1,tot2,tot3)

userActionSessionFileDir = "..\\datasets\\CERT\\r4.2\\combined_filed_with_respect_to_user\\"
userFileList = glob.glob(userActionSessionFileDir + "*.csv")

total_action = 0

logon=logoff=http=email=conn=disconn=f=0

for elem in userFileList:
    fread = open(elem,"r")
    for row in fread:
        row = row.replace("\n","")
        rowsp = row.split(",")
        actionType = rowsp[-1]        
        total_action+=1
        if "Logon" in actionType:
            logon+=1
        elif "Logoff" in actionType:
            logoff+=1
        elif "http" in actionType:
            http+=1
        elif "email" in actionType:
            email+=1
        elif "Connect" in actionType:
            conn+=1
        elif "Disconnect" in actionType:
            disconn+=1
        else:
            f+=1
print(total_action)
print("logon",logon)
print("Logoff",logoff)
print("http",http)
print("email",email)
print("connect",conn)
print("disconnect",disconn)
print("file",f)
"""
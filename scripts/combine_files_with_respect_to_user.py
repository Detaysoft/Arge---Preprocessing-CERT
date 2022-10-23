from datetime import datetime
import numpy as np
ldapFileList = ["2010-01","2010-02","2010-03","2010-04","2010-05","2010-06","2010-07","2010-08","2010-09","2010-10","2010-11","2010-12","2011-01","2011-02","2011-03","2011-04","2011-05"]
dataFileDir = "..\\datasets\\CERT\\r4.2\\"

def processLDAP():
    oldUserIdList = []
    for elem in ldapFileList:
        fread = open(dataFileDir + "LDAP\\" + elem+".csv","r")
        fread.readline()
        userIdList = []
        for row in fread:
            row = row.replace("\n", "")
            row = row.replace("\r", "")
            rowsp = row.split(",")
            userIdList.append(rowsp[1])
        newUser = [userId for userId in userIdList if userId not in oldUserIdList]
        leavingEmployees = [userId for userId in oldUserIdList if userId not in userIdList]
        oldUserIdList = userIdList
        #print(len(newUser),len(leavingEmployees),len(userIdList))
def extractUsers():
    userList = []
    fread = open(dataFileDir + "LDAP\\2010-01.csv","r")
    fread.readline()
    for row in fread:
        row = row.replace("\n", "")
        row = row.replace("\r", "")
        rowsp = row.split(",")
        userList.append(rowsp[1])
    userList = list(set(userList))
    return userList

def createEmptyUserIdDict():
    userIdList = extractUsers()
    userActionDictionary = {}
    for userId in userIdList:
        userActionDictionary[userId] = []   
    return userActionDictionary


def combine_action_squence_for_user():
    userActionDictionary = createEmptyUserIdDict()
    print("Dictionary Created.")
    print("Device file is extracting...")
    exract_action_sequence_device(userActionDictionary)
    print("File file is extracting...")
    exract_action_sequence_file(userActionDictionary)
    print("Logon file is extracting...")
    exract_action_sequence_logon(userActionDictionary)
    print("Email file is extracting...")
    exract_action_sequence_email(userActionDictionary)
    print("Http file is extracting...")
    exract_action_sequence_http(userActionDictionary)
    print("Extraction completed")
    return userActionDictionary

def exract_action_sequence_device(userActionDictionary):
    deviceFile = open(dataFileDir +  "device.csv","r")
    deviceFile.readline()
    for action in deviceFile:
        action = action.replace("\n", "")
        action = action.replace("\r", "")
        actionsp = action.split(",")
        actionId = actionsp[0]
        date = actionsp[1]
        date = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
        userId = actionsp[2]
        actionPc = actionsp[3]
        actionType = actionsp[4]
        userActionDictionary[userId].append([actionId,date,actionPc,actionType])

def exract_action_sequence_file(userActionDictionary):
    fileFile = open(dataFileDir + "file.csv","r")
    fileFile.readline()
    for action in fileFile:
        action = action.replace("\n", "")
        action = action.replace("\r", "")
        actionsp = action.split(",")
        actionId = actionsp[0]
        date = actionsp[1]
        date = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
        userId = actionsp[2]
        actionPc = actionsp[3]
        userActionDictionary[userId].append([actionId,date,actionPc,"file"])



def exract_action_sequence_logon(userActionDictionary):
    logonFile = open(dataFileDir + "logon.csv","r")
    logonFile.readline()
    for action in logonFile:
        action = action.replace("\n", "")
        action = action.replace("\r", "")
        actionsp = action.split(",")
        actionId = actionsp[0]
        date = actionsp[1]
        date = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
        userId = actionsp[2]
        actionPc = actionsp[3]
        actionType = actionsp[4]
        userActionDictionary[userId].append([actionId,date,actionPc,actionType])
  
def exract_action_sequence_email(userActionDictionary):
    emailFile = open(dataFileDir + "email.csv","r")
    emailFile.readline()
    for action in emailFile:
        action = action.replace("\n", "")
        action = action.replace("\r", "")
        actionsp = action.split(",")
        actionId = actionsp[0]
        date = actionsp[1]
        date = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
        userId = actionsp[2]
        actionPc = actionsp[3]
        userActionDictionary[userId].append([actionId,date,actionPc,"email"])

def exract_action_sequence_http(userActionDictionary):
    httpFile = open(dataFileDir + "http.csv","r")
    httpFile.readline()
    for action in httpFile:
        action = action.replace("\n", "")
        action = action.replace("\r", "")
        actionsp = action.split(",")
        actionId = actionsp[0]
        date = actionsp[1]
        date = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
        userId = actionsp[2]
        actionPc = actionsp[3]
        userActionDictionary[userId].append([actionId,date,actionPc,"http"])

def sort_dictionary_by_user(userActionDictionary):
    for elem in userActionDictionary.keys():
        userActionDictionary[elem] = np.array(userActionDictionary[elem])
        userActionDictionary[elem] = userActionDictionary[elem][np.argsort(userActionDictionary[elem][:,1])]
    print("Dictionary sorted")

def create_user_action_squence_file(userActionDictionary):
    for elem in userActionDictionary.keys():
        print(elem)
        userFile = open(dataFileDir + "combined_filed_with_respect_to_user\\" + elem + ".csv","w")
        currentUserData = userActionDictionary[elem]
        for i in range(currentUserData.shape[0]):
            stringDate = currentUserData[i][1].strftime("%m/%d/%Y %H:%M:%S")
            userFile.write(currentUserData[i][0] +","+ stringDate+"," +currentUserData[i][2] +","+ currentUserData[i][3] + "\n")
        userFile.close()
        



#userActionDictionary = combine_action_squence_for_user()
#sort_dictionary_by_user(userActionDictionary) 
#create_user_action_squence_file(userActionDictionary)
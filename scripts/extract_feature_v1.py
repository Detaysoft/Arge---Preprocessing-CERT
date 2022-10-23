
"""
userID, team, functional Unit, O, C, E, A, N
session duration work off, session duration work on
number of file work on, number of file work off
number of http work on, number of http work off
number of email work on, number of email work off
number of device work on, number of device work off
session sqeunce
target
"""

import numpy as np
import glob
from datetime import datetime
from datetime import time



ldapFileDir = "..\\datasets\\CERT\\r4.2\\LDAP\\"
userActionSessionFileDir = "..\\datasets\\CERT\\r4.2\\combined_filed_with_respect_to_user\\"
rawDataDir = "..\\datasets\\CERT\\r4.2\\"
answerFileDir = "..\\datasets\\CERT\\answers\\"
extractedFileWriteDir = "..\\datasets\\CERT\\r4.2\\featureExtractedDataset\\"

def extract_malicious_users():
    maliciousUserList = []
    maliciousActionList = []
    maliciousFileList = glob.glob(answerFileDir + "r4.2-1\\*")
    for fName in maliciousFileList:
        maliciousActionFile = open(fName,"r")
        for seq in maliciousActionFile:
            seq = seq.replace("\n","")
            seq = seq.replace("\r","")
            seqsp = seq.split(",")
            maliciousUserList.append(seqsp[3])
            maliciousActionList.append([seqsp[0],seqsp[1],seqsp[2],seqsp[3],"1"])     
    maliciousUserList = list(set(maliciousUserList))
    
    maliciousFileList = glob.glob(answerFileDir + "r4.2-2\\*")
    for fName in maliciousFileList:
        maliciousActionFile = open(fName,"r")
        for seq in maliciousActionFile:
            seq = seq.replace("\n","")
            seq = seq.replace("\r","")
            seqsp = seq.split(",")
            maliciousUserList.append(seqsp[3])
            maliciousActionList.append([seqsp[0],seqsp[1],seqsp[2],seqsp[3],"2"])     
    maliciousUserList = list(set(maliciousUserList))
    
    maliciousFileList = glob.glob(answerFileDir + "r4.2-3\\*")
    for fName in maliciousFileList:
        maliciousActionFile = open(fName,"r")
        for seq in maliciousActionFile:
            seq = seq.replace("\n","")
            seq = seq.replace("\r","")
            seqsp = seq.split(",")
            maliciousUserList.append(seqsp[3])
            maliciousActionList.append([seqsp[0],seqsp[1],seqsp[2],seqsp[3],"3"])     
    maliciousUserList = list(set(maliciousUserList))   
    maliciousActionList = np.array(maliciousActionList)
    return maliciousActionList, maliciousUserList


def extract_user_inf():
    ldapFile = open(ldapFileDir + "2010-01.csv","r")
    ldapFile.readline()
    userInfList = []
    for userseq in ldapFile:
        userseq = userseq.replace("\n","")
        userseq = userseq.replace("\r","")
        userseqsp = userseq.split(",")
        userId = userseqsp[1]
        userFncUnit = userseqsp[5]
        userTeam = userseqsp[7]
        oceanFile = open(rawDataDir + "psychometric.csv" , "r")
        oceanFile.readline()
        o=c=e=a=n = 0
        for oceans in oceanFile:
            oceans = oceans.replace("\n","")
            oceans = oceans.replace("\r","")
            oceanssp = oceans.split(",")
            userIdOcean = oceanssp[1]
            if userIdOcean == userId:
                o = oceanssp[2]
                c = oceanssp[3]
                e = oceanssp[4]
                a = oceanssp[5]
                n = oceanssp[6]
                break
        oceanFile.close()
        userInfList.append([userId,userFncUnit,userTeam,o,c,e,a,n])
        if o==0 or c==0 or e==0 or a==0 or n==0:
            print("err")
    return userInfList

def transform_string_inf_to_encoded(userInfList):
    fncUnitList = []
    teamList = []
    for elem in userInfList:
        fncUnitList.append(elem[1])
        teamList.append(elem[2])
    fncUnitList = list(set(fncUnitList))  
    teamList = list(set(teamList))
    for elem in userInfList:
        elem[1] = fncUnitList.index(elem[1])
        elem[2] = teamList.index(elem[2])

def time_in_range(actionTime):
    start = time(8, 0, 0)
    end = time(19, 0, 0)
    return start <= actionTime <= end
def take_diff_of_two_time(t1,t2):
    today = datetime.today()
    t1_d = datetime.combine(today, t1)
    t2_d = datetime.combine(today, t2)
    diff = t2_d - t1_d
    return diff.seconds/3600

def compute_session_duration(logOnDate,logOffDate):
    session_duration_work_on = session_duration_work_off = 0
    if time_in_range(logOnDate.time()) and  time_in_range(logOffDate.time()):
        session_duration_work_on = take_diff_of_two_time(logOnDate.time(),logOffDate.time())
        
    elif not time_in_range(logOnDate.time()) and  not time_in_range(logOffDate.time()):
        session_duration_work_off = take_diff_of_two_time(logOnDate.time(),logOffDate.time())
        
    elif time_in_range(logOnDate.time()) and  not time_in_range(logOffDate.time()):
        session_duration_work_on = take_diff_of_two_time(logOnDate.time(),time(19,0,0))
        session_duration_work_off = take_diff_of_two_time(time(19,0,0),logOffDate.time())
        
    else:
        session_duration_work_on = take_diff_of_two_time(time(8,0,0),logOffDate.time())
        session_duration_work_off = take_diff_of_two_time(logOnDate.time(),time(8,0,0))
        
    return session_duration_work_on, session_duration_work_off

def compute_number_of_email(actionSequence):
    n_of_email_work_on = n_of_email_work_off = 0;
    for action in actionSequence:
        if "email" in action[1]:
            actionDate = datetime.strptime(action[0], '%m/%d/%Y %H:%M:%S')
            if time_in_range(actionDate.time()):
                n_of_email_work_on += 1
            else:
                n_of_email_work_off += 1
    return n_of_email_work_on, n_of_email_work_off


def compute_number_of_file(actionSequence):
    n_of_file_work_on = n_of_file_work_off = 0;
    for action in actionSequence:
        if "file" in action[1]:
            actionDate = datetime.strptime(action[0], '%m/%d/%Y %H:%M:%S')
            if time_in_range(actionDate.time()):
                n_of_file_work_on += 1
            else:
                n_of_file_work_off += 1
    return n_of_file_work_on, n_of_file_work_off

def compute_number_of_http(actionSequence):
    n_of_http_work_on = n_of_http_work_off = 0;
    for action in actionSequence:
        if "http" in action[1]:
            actionDate = datetime.strptime(action[0], '%m/%d/%Y %H:%M:%S')
            if time_in_range(actionDate.time()):
                n_of_http_work_on += 1
            else:
                n_of_http_work_off += 1
    return n_of_http_work_on, n_of_http_work_off

def compute_number_of_device(actionSequence):
    n_of_device_work_on = n_of_device_work_off = 0;
    for action in actionSequence:
        if "Connect" in action[1] or "Disconnect" in action[1]:
            actionDate = datetime.strptime(action[0], '%m/%d/%Y %H:%M:%S')
            if time_in_range(actionDate.time()):
                n_of_device_work_on += 1
            else:
                n_of_device_work_off += 1
    return n_of_device_work_on, n_of_device_work_off

def generate_features_for_nonmalicious(extractedFileWriteName,userId,userInf):
    print(userId,"Non-Malicious")
    userDataFile = open(userActionSessionFileDir + userId + ".csv","r")
    actionSequence = []
    extractedFileWrite = open(extractedFileWriteName,"a")
    
    for userData in userDataFile:
        userData = userData.replace("\n", "")
        userDatasp = userData.split(",")
        actionSequence.append([userDatasp[1],userDatasp[3]])
        if "Logoff" in userDatasp[3]:
            logOnDate =  datetime.strptime(actionSequence[0][0], '%m/%d/%Y %H:%M:%S')
            logOffDate = datetime.strptime(actionSequence[-1][0], '%m/%d/%Y %H:%M:%S')       
            session_duration_work_on, session_duration_work_off = compute_session_duration(logOnDate,logOffDate)
            n_of_email_work_on, n_of_email_work_off = compute_number_of_email(actionSequence)
            n_of_file_work_on, n_of_file_work_off = compute_number_of_file(actionSequence)
            n_of_http_work_on, n_of_http_work_off = compute_number_of_http(actionSequence)
            n_of_device_work_on, n_of_device_work_off = compute_number_of_device(actionSequence)
            actionSequenceString = "-".join(np.array(actionSequence)[:,1])
            
            featureVector = [userId,userInf[1],userInf[2],userInf[3],userInf[4],
                             userInf[5],userInf[6],userInf[7],
                             session_duration_work_on, session_duration_work_off,
                             n_of_email_work_on, n_of_email_work_off,
                             n_of_file_work_on, n_of_file_work_off,
                             n_of_http_work_on, n_of_http_work_off,
                             n_of_device_work_on, n_of_device_work_off,
                             actionSequenceString,0]
            
            featureVectorListString = [str(elem) for elem in featureVector]
            featureVectorString = ",".join(featureVectorListString)
            extractedFileWrite.write(featureVectorString + "\n")
            actionSequence = []
    extractedFileWrite.close()
    
def computeTargetForSequence(userId,actionSequence,maliciousActionList):
    maliciousActionListOfUser = [userMal for userMal in maliciousActionList if userMal[3]==userId]
    for action in actionSequence:
        actionDate = action[0]
        actionType = action[1]
        actionId = action[2]
        for maliciousActionOfUser in maliciousActionListOfUser:
            maliciousActionOfUserType = maliciousActionOfUser[0]
            maliciousActionOfUserId = maliciousActionOfUser[1]
            maliciousActionOfUserDate = maliciousActionOfUser[2]
            if (actionDate==maliciousActionOfUserDate and 
                actionType==maliciousActionOfUserType and
                actionId == maliciousActionOfUserId):
                return int(maliciousActionOfUser[4])
    return 0
    

def generate_features_for_malicious(extractedFileWriteName,userId,maliciousActionList,userInf):
    print(userId,"Malicious")
    userDataFile = open(userActionSessionFileDir + userId + ".csv","r")
    actionSequence = []
    extractedFileWrite = open(extractedFileWriteName,"a")
    
    for userData in userDataFile:
        userData = userData.replace("\n", "")
        userDatasp = userData.split(",")
        actionSequence.append([userDatasp[1],userDatasp[3],userDatasp[0]])
        if "Logoff" in userDatasp[3]:
            logOnDate =  datetime.strptime(actionSequence[0][0], '%m/%d/%Y %H:%M:%S')
            logOffDate = datetime.strptime(actionSequence[-1][0], '%m/%d/%Y %H:%M:%S')       
            session_duration_work_on, session_duration_work_off = compute_session_duration(logOnDate,logOffDate)
            n_of_email_work_on, n_of_email_work_off = compute_number_of_email(actionSequence)
            n_of_file_work_on, n_of_file_work_off = compute_number_of_file(actionSequence)
            n_of_http_work_on, n_of_http_work_off = compute_number_of_http(actionSequence)
            n_of_device_work_on, n_of_device_work_off = compute_number_of_device(actionSequence)
            actionSequenceString = "-".join(np.array(actionSequence)[:,1])
            sequenceTarget = computeTargetForSequence(userId,actionSequence,maliciousActionList)
            
            featureVector = [userId,userInf[1],userInf[2],userInf[3],userInf[4],
                             userInf[5],userInf[6],userInf[7],
                             session_duration_work_on, session_duration_work_off,
                             n_of_email_work_on, n_of_email_work_off,
                             n_of_file_work_on, n_of_file_work_off,
                             n_of_http_work_on, n_of_http_work_off,
                             n_of_device_work_on, n_of_device_work_off,
                             actionSequenceString,sequenceTarget]
                        
            featureVectorListString = [str(elem) for elem in featureVector]
            featureVectorString = ",".join(featureVectorListString)
            extractedFileWrite.write(featureVectorString + "\n")
            actionSequence = []
    extractedFileWrite.close()
    
def exract_features(userInfList,maliciousActionList,maliciousUserList):
    extractedFileWriteName = extractedFileWriteDir + "extractedDataset.csv"
    extractedFileWrite = open(extractedFileWriteName,"w")
    extractedFileWrite.write("userId,"
                             "functional_unit,"
                             "team,"
                             "o,"
                             "c,"
                             "e,"
                             "a,"
                             "n,"
                             "session_duration_work_on,"
                             "session_duration_work_off,"
                             "n_of_email_work_on,"
                             "n_of_email_work_off,"
                             "n_of_file_work_on,"
                             "n_of_file_work_off,"
                             "n_of_http_work_on,"
                             "n_of_http_work_off,"
                             "n_of_device_work_on,"
                             "n_of_device_work_off,"
                             "actionSequenceString,"
                             "sequenceTarget\n")
    extractedFileWrite.close()
    currentUser = 0
    for userInf in userInfList:
        currentUser+=1
        print(currentUser)
        userId = userInf[0]
        if userId not in maliciousUserList:
            generate_features_for_nonmalicious(extractedFileWriteName,userId,userInf)
        else:
            generate_features_for_malicious(extractedFileWriteName,userId,maliciousActionList,userInf)
            

#userInfList = extract_user_inf()
#transform_string_inf_to_encoded(userInfList)
#maliciousActionList, maliciousUserList = extract_malicious_users()
#exract_features(userInfList,maliciousActionList,maliciousUserList)
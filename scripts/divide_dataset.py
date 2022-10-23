
import numpy as np

#Seq = 0-7, 18,19
#WoSeq = 0-17, 19

SeqInd = [0,1,2,3,4,5,6,7,18,19]
WoSeqInd = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19]
extractedFileReadDir = "..\\datasets\\CERT\\r4.2\\featureExtractedDataset\\"

extractedFileRead = open(extractedFileReadDir + 
                         "extractedDataset.csv","r")

extractedFileWriteWoSeq = open(extractedFileReadDir + 
                               "extractedDatasetWoSeq.csv","w")

extractedFileWriteSeq = open(extractedFileReadDir + 
                             "extractedDatasetSeq.csv","w")

for row in extractedFileRead:
    row.replace("\n","")
    rowsp = np.array(row.split(","))
    
    extractedFileWriteWoSeq.write(",".join(rowsp[WoSeqInd]))
    extractedFileWriteSeq.write(",".join(rowsp[SeqInd]))

extractedFileRead.close()
extractedFileWriteWoSeq.close()
extractedFileWriteSeq.close()

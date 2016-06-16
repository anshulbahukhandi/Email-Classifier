#Name : Anshul Bahukhandi
#Date : 6/15/2016
#Project : Email Classifier
#Description : This is an email classifier that is based on supervised machine learning algorithm and
#              and implemented using support vector machine

import os , numpy , sys

#Vocabulary and number of words in vocabulary
wordCount=0
vocabulary=[]
training_data=[]

def updateVocabulary():
    # Reading spam training files
    global wordCount
    os.chdir('C:/Users/Anshul/PycharmProjects/SpamClassifier/training_data/spam')
    for filename in os.listdir(os.getcwd()):
            fileobject = open(filename)
            for line in fileobject:
                for word in line.split():
                    vocabulary.append(word)
                    wordCount+=1
    #reading non-spam training files
    os.chdir('C:/Users/Anshul/PycharmProjects/SpamClassifier/training_data/not_spam')
    for filename in os.listdir(os.getcwd()):
        fileobject = open(filename)
        for line in fileobject:
            for word in line.split():
                vocabulary.append(word)
                wordCount += 1
    print wordCount

def printVocabulary():
    for word in vocabulary:
        print word


def createFeatureVectors():
    # creating feature vector for each of the spam emails
    os.chdir('C:/Users/Anshul/PycharmProjects/SpamClassifier/training_data/spam')
    for file in os.listdir(os.getcwd()):
        featureVector=[]
        for word in vocabulary:
            if word in open(file).read():
                featureVector.append(1)
            else:
                featureVector.append(0)
        training_data.append({'x':featureVector , 'y':1})
    # creating feature vector for each of the non-spam emails
    os.chdir('C:/Users/Anshul/PycharmProjects/SpamClassifier/training_data/not_spam')
    for file in os.listdir(os.getcwd()):
        featureVector = []
        for word in vocabulary:
            if word in open(file).read():
                featureVector.append(1)
            else:
                featureVector.append(0)
        training_data.append({'x': featureVector, 'y': -1})

    print 'No . of  emails in training data:', len(training_data)

#Function to print any feature vector in the training data
def printfeatureVector(index):
    print 'class is : ', training_data[index]['y']
    print 'length of feature vector is : ', len(training_data[index]['x'])
    for int in training_data[index]['x']:
        print int

# All the data has been acquired till this point . Time to implement the support vector machine
# using sequential minimal optimization


#Function to calculate the dot product of two lists
#NO NEED TO EXPLICITLY USE IN MAIN , ITS USED BY OTHER FUNCTIONS
def dotProduct(list1  , list2):
    if len(list1)!=len(list2):
        return 0
    total=0
    for i in range(0,len(vocabulary)):
        total=total+list1[i]*list2[i]
        return total

featureMatrix=[]
#Function to pre- compute the required dot products of all the feature vectors
#NO NEED TO EXPLICITLY USE IN MAIN , ITS USED BY OTHER FUNCTIONS
def createFeatureMatrix():
    createFeatureVectors()
    global featureMatrix
    for i in range(0 ,len(training_data)):
        for j in range(i ,len(training_data)):
            temp=dotProduct(training_data[i]['x'] , training_data[j]['x'])

# vector of alphas initialized to zero
alpha =[]

#NO NEED TO EXPLICITLY USE IN MAIN , ITS USED BY OTHER FUNCTIONS
def computeAlphaySum(k,l):
    alphaySum = 0
    global training_data
    global alpha
    for i in range(0, len(training_data)):
        if i!=k and i!=l:
            alphaySum += training_data[i]['y'] * alpha[i]
    return alphaySum

#NO NEED TO EXPLICITLY USE IN MAIN , ITS USED BY OTHER FUNCTIONS
def computeW():
    B=0
    for i in range(0,len(training_data)):
        for j in range(0,len(training_data)):
            B+=training_data[i]['y']*training_data[j]['y']*alpha[i]*alpha[j]*featureMatrix[i][j]
    return sum(alpha)-0.5 * B

#MUST EXPLICITLY USE IN MAIN
INCREMENT=1
C=10 #parameter for L1 regularization
def computeAlpha():
    global alpha
    global featureMatrix
    createFeatureMatrix()
    #Initializing here because we get training data after we call createFeatureMatrix
    #initializing alpha
    for i in range(0,len(training_data)):
        alpha.append(0)
    #initializing featureMatrix
    for i in range(0, len(training_data)):
        featureMatrix.append([0] * len(training_data))

    #changing two alpha's turn by turn
    for i in range(0,len(training_data)):
        for j in range(0,len(training_data)):
            if i!=j:
                alpha1=alpha[i]
                alpha2=alpha[j]
                # Two alphas to change selected
                wInitial=0
                while True:
                    alpha[i]+=INCREMENT
                    if alpha[i]>C:
                        break
                    alpha[j]=(-computeAlphaySum(i,j)- alpha[i]*training_data[i]['y'])/training_data[j]['y']
                    temp=computeW()
                    if temp>wInitial:
                        wInitial=temp
                    else:
                        alpha[i]=alpha1
                        alpha[j]=alpha2
                        break

b=0
w=[]
#MUST EXPLICITLY USE IN MAIN
def computeWB():
    global w
    w = [0] * wordCount
    #computing w
    for i in range(0,len(training_data)):
        for j in range(0, wordCount):
            w[j]+=alpha[i]*training_data[i]['y']*training_data[i]['x'][j]
    #computing b
    tempmax=-sys.maxint-1
    for i in range(0,len(training_data)):
        if training_data[i]['y']==-1:
            temp=dotProduct(w,training_data[i]['x'])
            if temp>tempmax:
                tempmax=temp
    tempmin=sys.maxint
    for i in range(0,len(training_data)):
        if training_data[i]['y']==1:
            temp=dotProduct(w,training_data[i]['x'])
            if temp<tempmin:
                tempmin=temp
    b= -0.5*(tempmax + tempmin)

#classify the texts in the folder named test_data
def classifyTestData():
    os.chdir('C:/Users/Anshul/PycharmProjects/SpamClassifier/')
    resultfile=open("result.txt","w")
    os.chdir('C:/Users/Anshul/PycharmProjects/SpamClassifier/test_data')
    for file in os.listdir(os.getcwd()):
        featureVector = []
        for word in vocabulary:
            if word in open(file).read():
                featureVector.append(1)
            else:
                featureVector.append(0)
        if (dotProduct(w,featureVector)+b)>0:
            resultfile.write("SPAM!!\n")
        else:
            resultfile.write("NOT SPAM!!\n")
    resultfile.close()

def main():
    updateVocabulary()
    computeAlpha()
    computeWB()
    classifyTestData()

main()
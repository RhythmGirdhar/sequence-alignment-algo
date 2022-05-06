import sys
import math

inputFile = sys.argv[1]
outputFile = sys.argv[2]

DELTA = 30

ALPHA = {
            "A": {"A": 0, "C": 110, "G": 48, "T": 94},
            "C": {"A": 110, "C": 0, "G": 118, "T": 48}, 
            "G": {"A": 48, "C": 118, "G": 0, "T": 110}, 
            "T": {"A": 94, "C": 48, "G": 110, "T": 0}
        }

def generateSequences(inputFile):

    f = open(inputFile, "r")

    # parse input and get counts
    baseDict = {}
    firstString = ""
    lastString = ""
    for line in f.readlines():
        # remove spaces and newlines
        # check if numeric, if so then that is an index
        # if not, then that is a base string
        strippedLine = line.strip().replace("\n", "")
        if(strippedLine.isnumeric()):
            prevIdxList = baseDict[lastString]
            prevIdxList.append(strippedLine)
        else:
            if(lastString == ""):
                firstString = strippedLine
            lastString = strippedLine
            baseDict[lastString] = []

    #2𝑗 * 𝑙𝑒𝑛(𝑠1) and 2 . Please note that the base strings need not have to be of equal 𝑘 * 𝑙𝑒𝑛(𝑠2)

    lenX = math.pow(2, len(baseDict[firstString])) * len(firstString)
    lenY = math.pow(2, len(baseDict[lastString])) * len(lastString)

    X = firstString
    Y = lastString

    # generate X
    for idx in baseDict[firstString]:
        firstSection = X[:int(idx)+1]
        secondSection = X[int(idx)+1:]
        X = firstSection + X + secondSection

    # generate Y
    for idx in baseDict[lastString]:
        firstSection = Y[:int(idx)+1]
        secondSection = Y[int(idx)+1:]
        Y = firstSection + Y + secondSection

    assert(len(X) == lenX)
    assert(len(Y) == lenY)
    return X, Y

X, Y = generateSequences(inputFile)

M = []

# initialize the M values (first row & first column) as 0
# "#" if we havent found the value yet
zArr = [0 for z in range(len(Y))]
jArr = ['#' for j in range(len(Y))]
jArr[0] = 0
iArr = [jArr for i in range(len(X))]
iArr[0] = zArr

# M is the memoized array
M = iArr

# Sequence Alignment Recurrence Relation
# OPT(i, j) = min(
#       alpha_xi_yj + OPT(i-1, j-1), # case 1 - they match
#       DELTA + OPT(i-1, j), # case 2 - they dont match update X index
#       DELTA + OPT(i, j-1) # case 3 - they dont match update Y index
#  )
print(X)
print(Y)

for i in range(1, len(X)):
    for j in range(1, len(Y)):
        if(X[i] == Y[j]):
            print(X[i], Y[j], ALPHA[ X[i]] [Y[j]], M[i-1][j-1])
            M[i][j] = ALPHA[ X[i]] [Y[j]] + M[i-1][j-1]
        elif(len(X) > len(Y)):
            print('try2')
            M[i][j] = 1
        elif(len(X) < len(Y)):
            print('try3')
            M[i][j] = 2
print(M)
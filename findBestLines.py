




import time
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import sys
from itertools import combinations
from random import random

def toAngle(radius):
    return 180/np.pi * radius

def calCoeffAndIntercept(x):
    timeTuple = x['TIME']
    addrTuple = x['addr']
    coeff = (addrTuple[1]-addrTuple[0]) / (timeTuple[1]-timeTuple[0])
    inter = addrTuple[0] - coeff*timeTuple[0]
    return (round(coeff,3), round(inter,3))

def genFile(filename):
    lineCoeff = [random(), random(), random(), random()]
    lineInter = [random(), random(), random(), random()]
    dots = []
    for i in range(4):
        for j in range(400):
            x = random()
            y = lineCoeff[i]*x + lineInter[i]
            dots.append((x, y))

    f = open(filename, "w")
    for d in dots:
        f.write(str(d[0])+","+str(d[1])+"\n")
    f.close()

def main():



    #read data
    inputFile = sys.argv[1]
    genFile(inputFile)
    data = pd.read_csv(inputFile, names=["TIME", "addr"])

    #separate data
    TIME = data.iloc[:, 0].values.reshape(-1, 1)
    addr = data.iloc[:, 1].values.reshape(-1, 1)

    #Linear regression
    Lregressor = LinearRegression()
    Lregressor.fit(TIME, addr)

    #get coefficient and intercept
    intercept = Lregressor.intercept_[0]
    coefficient = Lregressor.coef_[0][0]
    angle = toAngle(np.arctan(coefficient))
    print(angle)

    tic = time.perf_counter()
    #get points above linear regression
    #higherPoints = data[(coefficient*data.TIME + intercept > data.addr)]
    higherPoints = data
    higherPoints = higherPoints.reset_index(drop=True)
    #print(higherPoints)

    #all pairs of highPoints
    dataC = higherPoints.apply(lambda r: list(combinations(r, 2)), axis=0)
    dataC = zip(dataC['TIME'], dataC['addr'])
    dataC = pd.DataFrame(dataC, columns = ['TIME', 'addr'])
    #print()

    dataC['lineEq'] = dataC.apply(calCoeffAndIntercept, axis=1)
    dataC = dataC.round(decimals=3)
    print(dataC.shape)

    count = dataC.groupby('lineEq').count()
    count = count.sort_values(by=['TIME'], ascending=False)
    print(count[0:5])
    print(count.shape)
    toc = time.perf_counter()
    print(toc - tic)

if __name__ == "__main__":
    main()

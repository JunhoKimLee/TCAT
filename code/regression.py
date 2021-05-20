# The code used to run linear and logistic regressions on the data to model key relationships

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt

data = pd.read_csv("data.csv")


def logistic_xy(x, y):
    model = LogisticRegression(solver="liblinear", random_state=0)
    model.fit(x, y)
    b0 = model.intercept_[0]
    b1 = model.coef_[0][0]
    b2 = model.coef_[0][1]
    b3 = model.coef_[0][2]
    score = model.score(x, y)
    print("The mean accuracy of this model is: " +
          str(round(score*100, 2)) + "%")
    print("The model is: ln(y/(1-y)) = " + str(round(b0, 4)) + " + " +
          str(round(b1, 4)) + "*x_1 + " + str(round(b2, 4)) + "*x_2 + " + str(round(b3, 4)) + "*x_3")
    print()


def linear_xy(x, y):
    model = LinearRegression()
    model.fit(x, y)
    #b0 = model.intercept_
    #b1 = model.coef_[0]
    #b2 = model.coef_[1]
    #b3 = model.coef_[2]
    score = model.score(x, y)
    print("The R^2 of this model is: " + str(round(score*100, 2)) + "%")
    # print("The model is: y = " + str(round(b0, 4)) + " + " +
    #      str(round(b1, 4)) + "*x_1 + " + str(round(b2, 4)) + "*x_2 + " + str(round(b3, 4)) + "*x_3")
    print()


# year and price of ticket regression
x = data["What is your graduation year?"]
y = data["With which of the methods have you used the TCAT in the past? (check all that apply) - Cash"]


def x_shower(x):
    output = np.zeros(len(x))
    for i in x.keys():
        output[i] = x[i]
    output = output.reshape(-1, 1)
    return output


def y_shower(y):
    output = np.zeros(len(y))
    for i in y.keys():
        if y[i] == "Cash":
            output[i] = 1
        else:
            output[i] = 0
    #output = output.reshape(-1, 1)
    return output


x = x_shower(x)
y = y_shower(y)

senior = []
junior = []
sophomore = []
for i in x:
    s = 0
    j = 0
    so = 0
    if i == 2021:
        s += 1
    elif i == 2022:
        j += 1
    elif i == 2023:
        so += 1
    senior.append(s)
    junior.append(j)
    sophomore.append(so)
year = {
    "2021": senior,
    "2022": junior,
    "2023": sophomore,
}
x = pd.DataFrame(year, columns=["2021", "2022", "2023"])

print("Year vs Cash logistic")
logistic_xy(x, y)
print("Year vs Cash linear")
linear_xy(x, y)

# location and price of ticket regression
y = data["What is the maximum you would pay for a single bus fare?"]


def fare_shower(y):
    output = np.zeros(len(y))
    for i in y.keys():
        output[i] = float(y[i][1:])
    output = output.reshape(-1, 1)
    return output


y = fare_shower(y)

# year vs fare $
print("Year vs fare linear")
linear_xy(x, y)

x = data["Where are you planning to live next year?"]

west = []
ctown = []
other = []
for i in x:
    w = 0
    c = 0
    o = 0
    if i == "West Campus ":
        w += 1
    elif i == "Collegetown":
        c += 1
    elif i == "Other":
        o += 1
    west.append(w)
    ctown.append(c)
    other.append(o)
year = {
    "West Campus": west,
    "Collegetown": ctown,
    "Other": other
}

x = pd.DataFrame(year, columns=["West Campus", "Collegetown", "Other"])

print("Loc vs fare linear")
linear_xy(x, y)

y = data["With which of the methods have you used the TCAT in the past? (check all that apply) - Cash"]
y = y_shower(y)

print("Loc vs cash linear")
linear_xy(x, y)
print("Loc vs cash logistic")
logistic_xy(x, y)

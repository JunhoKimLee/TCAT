# This file is now deprecated and contains a regression algorithm that is now a relic of the past.

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt

data = pd.read_csv("data.csv")
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

model = LogisticRegression(solver="liblinear", random_state=0)
model.fit(x, y)
b0 = model.intercept_
b1 = model.coef_
score = model.score(x, y)
print(score)

plt.scatter(x, y)
plt.plot(x, np.exp(b0+b1*x)/(1+np.exp(b0+b1*x)), c='red')
plt.show()


# beginning of avg linear regression


def year_avgs(x, y, labels):
    fresh = 0
    soph = 0
    junior = 0
    senior = 0
    fresh_c = 0
    soph_c = 0
    junior_c = 0
    senior_c = 0
    for i in range(len(x)):
        if x[i] == labels[0]:
            senior_c += 1
            senior += y[i]
        elif x[i] == labels[1]:
            junior_c += 1
            junior += y[i]
        elif x[i] == labels[2]:
            soph_c += 1
            soph += y[i]
        else:
            fresh_c += 1
            fresh += y[i]
    fr = fresh/fresh_c
    so = soph/soph_c
    ju = junior/junior_c
    se = senior/senior_c

    x = np.array(labels).reshape(-1, 1)
    y = np.array([se, ju, so, fr]).reshape(-1, 1)
    return x, y


def linear_xy(x, y, labels):
    lr = LinearRegression()
    lr.fit(x, y)
    w = lr.coef_[0]
    b = lr.intercept_
    print(w)
    print(b)

    y_pred = np.array([w*labels[0]+b, w*labels[1]+b,
                      w*labels[2]+b, w*labels[3]+b])
    r2 = r2_score(y, y_pred)
    print(r2)

    plt.scatter(x, y)
    plt.plot(x, w*x+b, c='red')
    plt.show()


label = [2021, 2022, 2023, 2024]
x, y = year_avgs(x, y, label)
linear_xy(x, y, label)

# year and price of ticket regression
x = data["What is your graduation year?"]
y = data["What is the maximum you would pay for a single bus fare?"]


def fare_shower(y):
    output = np.zeros(len(y))
    for i in y.keys():
        output[i] = float(y[i][1:])
    output = output.reshape(-1, 1)
    return output


x = x_shower(x)
y = fare_shower(y)
label = [2021, 2022, 2023, 2024]
x, y = year_avgs(x, y, label)
linear_xy(x, y, label)


# location and price of ticket regression
x = data["Where are you planning to live next year?"]
y = data["What is the maximum you would pay for a single bus fare?"]


def float_shower(x, labels):
    output = []
    for i in x.keys():
        if x[i] == "Collegetown":
            output.append(labels[0])
        elif x[i] == "North Campus":
            output.append(labels[1])
        elif x[i] == "Other":
            output.append(labels[3])
        else:
            output.append(labels[2])
    return output


# key:
# 1 = collegetown
# 2 = other
# 3 = west campus
# 4 = north campus
label = [1, 4, 3, 2]
x = float_shower(x, label)
print(x)
y = fare_shower(y)
x, y = year_avgs(x, y, label)
linear_xy(x, y, label)

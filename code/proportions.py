# Automated script that cranked out proportions data for the project

import pandas as pd
import math

data = pd.read_csv("data.csv")

percent = .95
z = 1.96


def proportion_interval(p, z, n):
    """
    Takes a proportion p, z-factor z, and sample size n, and calculates max
    error range using the confidence interval formula
    """
    return z*math.sqrt(p*(1-p)/n)


def proportion(data, question, z, aff):
    """
    Takes a dataset, question, z-factor, and affirmative response, and returns
    both the sample proportion for the specified question in the dataset that
    answered in the affirmative as well as the confidence interval
    """
    p = 0
    n = 0
    for i in data[question]:
        if i in aff:
            p += 1
            n += 1
        else:
            n += 1
    p = p/n
    h = proportion_interval(p, z, n)
    return p, h


def proportion_printer(p, h, percent, question):
    print(question)
    print("The sample of the proportion that answered in the affirmative is: " +
          str(round(p*100, 1)) + "%")
    low = p-h
    high = p+h
    if p-h < 0:
        low = 0
    if p+h > 1:
        high = 1
    print("The " + str(round(percent*100)) + "%" + " confidence interval of the proportion is: [" + str(
        round(low*100, 1)) + "%, " + str(round(high*100, 1)) + "%].")
    print()


p, h = proportion(
    data, "Will you have a car on campus next year?", z, ["Yes", "Maybe"])
proportion_printer(
    p, h, percent, "Will you have a car on campus next year? (yes or maybe)")

p, h = proportion(data, "Have you ever taken the TCAT?", z, ["Yes"])
proportion_printer(p, h, percent, "Have you ever taken the TCAT?")

p, h = proportion(data, "With which of the methods have you used the TCAT in the past? (check all that apply) - Cornell ID (free for first-year students, weekends + evening for all students)",
                  z, ["Cornell ID (free for first-year students, weekends + evening for all students)"])
proportion_printer(p, h, percent, "With which of the methods have you used the TCAT in the past? (check all that apply) - Cornell ID (free for first-year students, weekends + evening for all students)")

p, h = proportion(
    data, "With which of the methods have you used the TCAT in the past? (check all that apply) - Prepaid TCAT card", z, ["Prepaid TCAT card"])
proportion_printer(
    p, h, percent, "With which of the methods have you used the TCAT in the past? (check all that apply) - Prepaid TCAT card")

p, h = proportion(
    data, "With which of the methods have you used the TCAT in the past? (check all that apply) - OmniRide Pass", z, ["OmniRide Pass"])
proportion_printer(
    p, h, percent, "With which of the methods have you used the TCAT in the past? (check all that apply) - OmniRide Pass")

p, h = proportion(
    data, "With which of the methods have you used the TCAT in the past? (check all that apply) - Cash", z, ["Cash"])
proportion_printer(
    p, h, percent, "With which of the methods have you used the TCAT in the past? (check all that apply) - Cash")

p, h = proportion(
    data, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Walking", z, ["Every Day", "4-6 times per week", "1-3 times per week"])
proportion_printer(
    p, h, percent, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Walking (at least once a week)")

p, h = proportion(
    data, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Bus", z, ["Every Day", "4-6 times per week", "1-3 times per week"])
proportion_printer(
    p, h, percent, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Bus (at least once a week)")

p, h = proportion(
    data, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Car", z, ["Every Day", "4-6 times per week", "1-3 times per week"])
proportion_printer(
    p, h, percent, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Car (at least once a week)")

p, h = proportion(
    data, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Rideshare", z, ["Every Day", "4-6 times per week", "1-3 times per week"])
proportion_printer(
    p, h, percent, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Rideshare (at least once a week)")

p, h = proportion(
    data, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Bike, Scooter, Skateboard", z, ["Every Day", "4-6 times per week", "1-3 times per week"])
proportion_printer(
    p, h, percent, "How often do you anticipate use the following transportation modes in Ithaca next year, provided cla - Bike, Scooter, Skateboard (at least once a week)")

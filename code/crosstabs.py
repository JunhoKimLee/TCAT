# Automated script that cranked out all the crosstab analysis for the project

import pandas as pd
import math

data = pd.read_csv("data.csv")
for i in range(len(data)):
    if data["With which of the methods have you used the TCAT in the past? (check all that apply) - Cash"][i] != "Cash":
        data["With which of the methods have you used the TCAT in the past? (check all that apply) - Cash"][i] = "No Cash"
    if data["Where are you planning to live next year?"][i] in ["Collegetown", "Other"]:
        data["Where are you planning to live next year?"][i] = "Off-Campus"
    else:
        data["Where are you planning to live next year?"][i] = "On-Campus"
    if data["What is your graduation year?"][i] in [2021, 2022]:
        data["What is your graduation year?"][i] = "Upperclassmen"
    else:
        data["What is your graduation year?"][i] = "Underclassmen"
    if data["What is your family income?"][i] in ["0-25k", "25-50k", "50-75k", "75-100k", "100-150k"]:
        data["What is your family income?"][i] = "<150k"
    elif data["What is your family income?"][i] == "Prefer not to answer":
        data["What is your family income?"][i] = "NaN"
    else:
        data["What is your family income?"][i] = ">150k"
    if data["Will you have a car on campus next year?"][i] != "No":
        data["Will you have a car on campus next year?"][i] = "Yes"
    if data["What is the maximum you would pay for a single bus fare?"][i] in ["$0.00", "$0.50", "$1.00", "$1.50"]:
        data["What is the maximum you would pay for a single bus fare?"][i] = "No more"
    else:
        data["What is the maximum you would pay for a single bus fare?"][i] = "More"

    # data.to_csv("crosstab_data.csv")


def crosstab_analysis(data, do_cash=True):
    if do_cash:
        var = "With which of the methods have you used the TCAT in the past? (check all that apply) - Cash"
        y = "Cash"
        n = "No Cash"
    else:
        var = "What is the maximum you would pay for a single bus fare?"
        y = "More"
        n = "No more"

    def get_relationship(d1, d2, fst_total, snd_total):
        """
        Takes 2 crosstabs d1 and d2 that is the fst_total crosstab split
        accordingly based on the secondary variable (whose total crosstab is
        snd_total) and determines whether the first or second variable has a
        more pronounced impact.
        """
        sec_sum = 0
        t_sum = 0
        for i in range(len(fst_total)):
            t_sum += fst_total[y][i]+fst_total[n][i]
        for i in range(len(fst_total)):
            t = (fst_total[y][i]+fst_total[n][i])/t_sum
            sec_sum += t*(d2[y][i]-d1[y][i])

        fst_sum = 0
        sum_1 = d1[y][1] - d1[y][0]
        sum_2 = d2[y][1] - d2[y][0]
        t_1 = snd_total[y][0] + snd_total[n][0]
        t_2 = snd_total[y][1] + snd_total[n][1]
        t_3 = t_1 + t_2
        t_1 = t_1/t_3
        t_2 = t_2/t_3
        fst_sum = t_1*sum_1 + t_2*sum_2

        delta = abs(fst_sum) - abs(sec_sum)
        if delta > 0:
            print("The first variable has a greater impact by " +
                  str(round(delta*100, 1)) + "%")
        else:
            print("The second variable has a greater impact by " +
                  str(round(-delta*100, 1)) + "%")

    def year_crosstab(under=True):
        """
        Produces a sub-crosstab of the location crosstab that segments by
        underclassman if under=True and upperclassman otherwise.
        """
        underclassmen = data.copy()
        mycol = underclassmen["What is your graduation year?"]
        for i in mycol.keys():
            if under:
                if mycol[i] == "Upperclassmen":
                    underclassmen = underclassmen.drop(i)
            else:
                if mycol[i] == "Underclassmen":
                    underclassmen = underclassmen.drop(i)

        cash = underclassmen[var]
        location = underclassmen["Where are you planning to live next year?"]
        return pd.crosstab(location, cash, normalize="index")

    cash = data[var]
    location = data["Where are you planning to live next year?"]
    loc_total = pd.crosstab(location, cash)
    year_total = pd.crosstab(
        data["What is your graduation year?"], cash)
    under = year_crosstab()
    upper = year_crosstab(False)
    print(under)
    print(upper)
    get_relationship(under, upper, loc_total, year_total)

    def income_crosstab(rich_bool=True):
        rich = data.copy()
        mycol = rich["What is your family income?"]
        for i in mycol.keys():
            if rich_bool:
                if mycol[i] != ">150k":
                    rich = rich.drop(i)
            else:
                if mycol[i] != "<150k":
                    rich = rich.drop(i)

        cash = rich[var]
        location = rich["Where are you planning to live next year?"]
        return pd.crosstab(location, cash, normalize="index")

    income = data.copy()
    mycol = income["What is your family income?"]
    for i in mycol.keys():
        if mycol[i] != "NaN":
            income = income.drop(i)

    cash = income[var]
    location = income["Where are you planning to live next year?"]
    year = income["What is your graduation year?"]

    loc_total = pd.crosstab(location, cash)
    year_total = pd.crosstab(year, cash)

    rich = income_crosstab()
    poor = income_crosstab(False)
    print(rich)
    print(poor)
    get_relationship(poor, rich, loc_total, year_total)

    def gender_crosstab(male=True):
        rich = data.copy()
        mycol = rich["What gender do you identify as?"]
        for i in mycol.keys():
            if male:
                if mycol[i] != "Male":
                    rich = rich.drop(i)
            else:
                if mycol[i] != "Female":
                    rich = rich.drop(i)

        cash = rich[var]
        location = rich["Where are you planning to live next year?"]
        return pd.crosstab(location, cash, normalize="index")

    gender = data.copy()
    mycol = gender["What gender do you identify as?"]
    for i in mycol.keys():
        if mycol[i] not in ["Male", "Female"]:
            gender = gender.drop(i)

    cash = gender[var]
    location = gender["Where are you planning to live next year?"]
    year = gender["What is your graduation year?"]

    loc_total = pd.crosstab(location, cash)
    year_total = pd.crosstab(year, cash)

    male = gender_crosstab()
    female = gender_crosstab(False)
    print(male)
    print(female)
    get_relationship(male, female, loc_total, year_total)

    def car_crosstab(own=True):
        rich = data.copy()
        mycol = rich["Will you have a car on campus next year?"]
        for i in mycol.keys():
            if own:
                if mycol[i] != "Yes":
                    rich = rich.drop(i)
            else:
                if mycol[i] != "No":
                    rich = rich.drop(i)

        cash = rich[var]
        location = rich["Where are you planning to live next year?"]
        return pd.crosstab(location, cash, normalize="index")

    cash = data[var]
    location = data["Where are you planning to live next year?"]
    year = data["What is your graduation year?"]

    loc_total = pd.crosstab(location, cash)
    year_total = pd.crosstab(year, cash)

    car = car_crosstab()
    nocar = car_crosstab(False)
    print(car)
    print(nocar)
    get_relationship(car, nocar, loc_total, year_total)


crosstab_analysis(data)
print()
crosstab_analysis(data, False)

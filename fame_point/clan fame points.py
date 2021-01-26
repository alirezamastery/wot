import numpy as np
import pandas as pd
import time
import concurrent.futures as cf
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import matplotlib.pyplot as plt


def interest(percent, days, amount):
    x = amount
    for i in range(days):
        x = x + x * percent
    return int(x)


percentages = [[0.05, 10],
               [0.05, 50],
               [0.1, 250],
               [0.2, 1000],
               [0.2, 2500],
               [0.3, 5000],
               [0.3, 20000],
               [0.4, 30000],
               [0.4, 40000],
               [0.4, 50000]]

percentages_sum = [[0, 0]]
step = [0, 0]
# for per in percentages:
#     percentages_sum.append(per)
#     print(percentages_sum)

for per in percentages:
    step[0] += per[0]
    step[0] = round(step[0], 1)
    step[1] += per[1]
    percentages_sum.append(step[:])


def calculator(base):
    totals = list()
    for i, per in enumerate(percentages):
        print(f'{f"step: {i}":-^70}')
        base_income = base
        income = base_income
        multiplier = 1
        total = 0
        counter = 0
        for day in range(14):
            total += int(income)
            while counter < i and total > percentages[counter][1]:
                multiplier += percentages[counter][0]
                total -= percentages[counter][1]
                income = int(base_income * multiplier)
                counter += 1
            print(f'day: {day:<9} | total: {int(total):<5} | multiplier: {multiplier:<4.2f} | income: {income}')
        print(f'total: {total:<7} | income: {int(income):<5}')

        totals.append(int(total))
        if i > 1 and totals[-1] < totals[-2]:
            print('-' * 70)
            print(totals)
            print('found step:', i -1 )
            return i - 1



calculator(1400)
# results = list()
# inputs = [x for x in range(100 , 2000)]
# for i in inputs:
#     results.append(calculator(i))
# y_range = [x for x in range(11)]
# y_labels = ['0 %' , '5 %' , '5 %' , '10 %' , '20 %' , '20 %' , '30 %' , '30 %' , '40 %' , '40 %' , '40 %']
#
# plt.plot(inputs , results , linewidth=5)
# plt.xlabel('average daily base fame points' , labelpad=20 , fontsize=18)
# plt.ylabel('optimum boost level' , labelpad=20 , fontsize=18)
#
# plt.xticks(fontsize=18)
# plt.yticks(y_range , y_labels , fontsize=18)
#
# plt.grid()
#
# plt.show()

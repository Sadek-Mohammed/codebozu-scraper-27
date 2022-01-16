# import the typing library for best practices in coding (suggested by pycharm
from typing import Any
# import the sentiment analysis function
from sentiment import analyze_sent
# import pandas for csv file writing
import pandas as pd

# add a dictionary for positivity index and another dictionary for the negativity index
ratings_positive = {"Move": [], "Impact": [], "Upshot": []}
ratings_negative = {"Move": [], "Impact": [], "Upshot": []}
# add a dictionary for calculating the average of the positivity and negativity data for each column.
avg = {'Move': 0, 'Impact': 0, 'Upshot': 0}

# initializing the dictionaries with 30 columns
for i in range(0, 30):
    ratings_positive['Move'].append([])
    ratings_positive['Impact'].append([])
    ratings_positive['Upshot'].append([])
    ratings_negative['Move'].append([])
    ratings_negative['Impact'].append([])
    ratings_negative['Upshot'].append([])


# read the function
def avg_calc(ratings):
    for counter in range(0, 30):
        for key in ratings.keys():
            avg[key] += ratings[key][counter]
    for key in ratings.keys():
        avg[key] /= 30
        avg[key] = round(avg[key], 4)
    fin_avg = 0
    for key in avg.keys():
        fin_avg += avg[key]
    fin_avg /= 3
    fin_avg = round(fin_avg, 4)
    print(fin_avg)


def generate_data(trumps):
    for key in trumps.keys():
        if not key == 'Things':
            for counter in range(0, 30):
                if not trumps[key][counter] == "is not declared":
                    dic = analyze_sent(trumps[key][counter])
                    ratings_positive[key][counter] = dic['pos']
                    ratings_negative[key][counter] = dic['neg']
                else:
                    ratings_positive[key][counter] = 0.0
                    ratings_negative[key][counter] = 0.0
    # print(ratings_positive)
    # print(ratings_negative)
    avg_calc(ratings_positive)
    # print(avg)
    data_pos = pd.DataFrame(ratings_positive)
    data_neg = pd.DataFrame(ratings_negative)
    # changing data frame to csv.
    data_pos.to_csv("Insights/pos.csv", index=False)
    data_neg.to_csv("Insights/neg.csv", index=False)

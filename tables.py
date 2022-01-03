from sentiment import analyze_sent
from typing import Any
import pandas as pd

ratings_positive: dict[str, list[Any]] = {"Move": [], "Impact": [], "Upshot": []}
ratings_negative: dict[str, list[Any]] = {"Move": [], "Impact": [], "Upshot": []}
avg = {'Move': 0, 'Impact': 0, 'Upshot': 0}
for i in range(0, 30):
    ratings_positive['Move'].append([])
    ratings_positive['Impact'].append([])
    ratings_positive['Upshot'].append([])
    ratings_negative['Move'].append([])
    ratings_negative['Impact'].append([])
    ratings_negative['Upshot'].append([])


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
    data_pos.to_csv("pos.csv", index=False)
    data_neg.to_csv("neg.csv", index=False)

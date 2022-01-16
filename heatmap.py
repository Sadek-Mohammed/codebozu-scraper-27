import csv
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

root = 'Insights/'
files = ['bbc.csv', 'dm.csv', 'cnn.csv', 'fox_news.csv', 'WashingtonPost.csv']

sentiment_list: list = [[0] * 5] * 5

# bbc and dm scrapers do not support other candidates

for i in range(5):
    avg = 0
    df = pd.read_csv(root + files[i])

    if i in [0, 1]:
        for j in range(0, 19):
            avg += (float(df['pos'][j]) * 1000)
        sentiment_list[0][i] = (avg / 20)

    elif i in [2, 3]:
        df = df.transpose()
        for index in range(5):
            sentiment_row = df[2][index][1:-2].strip().split(', ')
            for num in sentiment_row:
                print(num)
                avg += float(num)
            sentiment_list[i][index] = (avg / len(sentiment_row))

    else:
        index = 0
        avg = 0
        for j in range(25):
            avg += (float(df['pos'][j]))
            if j % 5 == 0 and j != 0:
                sentiment_list[i][index] = avg/5
                avg = 0

data = np.array(sentiment_list, np.int32)

plt.imshow(data, cmap='autumn', interpolation='nearest')

plt.title('2-D Heat Map')
plt.xlabel('News Companies')
plt.ylabel('Politician')

plt.xticks([0, 1, 2, 3, 4], ['BBC', 'DailyMail', 'CNN', 'Fox News', 'WashingtonPost'])
plt.yticks([0, 1, 2, 3, 4], ['Donald Trump', 'Joe Biden', 'Barack Obama', 'George W. Bush', 'Bill Clinton'])
plt.show()

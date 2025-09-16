import pandas as pd
import matplotlib.pyplot as plt


def plotTemp(path):
    df = pd.read_csv(path, delimiter=',')
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    start = '2025-09-13 10:27:13'
    end   =  '2025-09-13 10:40:00'
    sub_df = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]

    plt.plot(sub_df['timestamp'], sub_df['power'])
    plt.plot(sub_df['timestamp'], sub_df['rxShifting'])
    plt.show()


def main():
    pathInp = input('inserisci path file: ')
    temp = True
    
    if temp:
        plotTemp(pathInp)


main()
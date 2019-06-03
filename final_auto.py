import pandas as pd
import numpy as np
import json
import string

def main():
    dframe = pd.read_excel('bank.xlsx')

    unique_accounts = list(dframe["Account No"].unique())

    account_map = {}
    for i in unique_accounts:
        account_map[i] = i[:-1]

    dframe["Account No"] = dframe["Account No"].map(account_map)

    unique_list = []
    for i, x in account_map.items():
        unique_list.append(x)

    account_list = []
    for x in unique_list:
        account_list.append(dframe[dframe["Account No"] == x])

    with open('result.json', 'r') as rf:
        tokens = json.loads(rf.read())

    zer = np.zeros((len(dframe),))
    dframe['A'] = zer
    dframe['B'] = zer
    dframe['C'] = zer
    dframe['D'] = zer
    dframe['E'] = zer

    for x in unique_list:
        account_list.append(dframe[dframe["Account No"] == x])

    df1 = account_list[0]

    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))

    for df1 in account_list:
        for i, x in enumerate(df1["Account No"]):
            if i % 100 == 0:
                print(i, end=' ')
            current_row = df1.iloc[i]
            current_trans = current_row["TRANSACTION DETAILS"].lower()

            for x in tokens:
                if x in current_trans:
                    current_row[tokens[x]] = x

            df1.iloc[i] = current_row


if __name__ == '__main__':
   main()

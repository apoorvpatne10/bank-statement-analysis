# ###################### Clean Code ######################

#### Subset - Withdrawal Amount, Sum - Deposit Amount
# bank_acc1 = bank[bank["Account No"] == 409000611074]

# [409000611074 409000493201 409000425051 409000405747 409000438611
#  409000493210 409000438620      1196711      1196428 409000362497]
import pandas as pd
from fuzzywuzzy import fuzz

bank = pd.read_csv('Data/bank3.csv')

# Returns a dataframe object consisting of matching narrations
def seq_match(df_temp, trans_details):

    df_temp.reset_index(inplace=True, drop=True)

    df_res = []
    for i, (x, y) in enumerate(df_temp.iterrows()):
        # Considered threshold : 30
        if fuzz.ratio(trans_details, df_temp.loc[i, "TRANSACTION DETAILS"]) > 30:
            df_res.append(df_temp.loc[i])

    return pd.DataFrame(df_res)


def subsetsum(array, num):

    if num == 0 or num < 1:
        return []
    elif len(array) == 0:
        return []
    else:
        if array[0] == num:
            return [array[0]]
        else:
            with_v = subsetsum(array[1:],(num - array[0]))
            if with_v:
                return [array[0]] + with_v
            else:
                return subsetsum(array[1:],num)


# 1. 409000611074
# 2. 409000493201
# 3. 409000425051
# 4. 409000405747
# 5. 409000438611 - Bogus
# 6. 409000493210 - Bogus
# 7. 409000438620 - Bogus
# 8. 1196711 - Bogus - S
# 9. 1196428 - Bogus
# 10. 409000362497 - Bogus

def main():
    df_acc1 = bank[bank["Account No"] == 1196711]
    df_res = pd.DataFrame()

    for (index, row) in df_acc1.iterrows():

        if index % 1000 == 0:
            print(index)

        if row["DEPOSIT AMT"] >= 0:
            acc_no = row["Account No"]
            date = row["VALUE DATE"]
            deposit_amt = row["DEPOSIT AMT"]
            trans_details = row["TRANSACTION DETAILS"]

            df_temp =\
                df_acc1[(df_acc1["Account No"] == acc_no) & (df_acc1["VALUE DATE"] == date) & (df_acc1["WITHDRAWAL AMT"] > 0)]

            # Further reducing the search space by getting matching transactions
            df_temp_res = seq_match(df_temp, trans_details)

            if not df_temp_res.empty:
                withdrawal_amt = list(df_temp_res["WITHDRAWAL AMT"])
                subset =  subsetsum(withdrawal_amt, deposit_amt)
                if len(subset) > 1:
                    print("***************************************")
                    print(f"Deposit Amount {deposit_amt}")
                    print(f"Withdrawal Amount : {subset}")
                    print(f"Date {date}")
                    print(f"Transaction Details {trans_details}")
                    print("***************************************")

if __name__ == '__main__':
    main()

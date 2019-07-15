import os
import pandas as pd
from fuzzywuzzy import fuzz
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Fraud
from .forms import MyForm

# [409000611074 409000493201 409000425051 409000405747 409000438611
#  409000493210 409000438620      1196711      1196428 409000362497]

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


def home(request):
    context = {}

    bank = pd.read_csv(f'{os.getcwd()}/detect/data/bank3.csv')

    bank.drop(["A", "B", "C", "D", "E"], axis=1, inplace=True)
    bank.drop(["CHQ.NO."], axis=1, inplace=True)

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            acc_no_curr = int(form.cleaned_data['account_choice'])
            print(acc_no_curr)
            df_acc1 = bank[bank["Account No"] == acc_no_curr]
            df_res = []

            if acc_no_curr not in list(Fraud.objects.values_list('acc_no', flat=True).distinct()):
                print(f'Processing... {len(df_acc1)}')
                ctr = 0
                for i, (index, row) in enumerate(df_acc1.iterrows()):

                    if i % 2 == 0:
                        print(f"{i}/{len(df_acc1)}")

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
                            if len(subset) > 0:
                                df_res.append([acc_no, trans_details, date, deposit_amt, subset, len(subset)])
                                ctr += 1
                                print(f'Found possible fraud transaction : {ctr}!')

                df_res = pd.DataFrame(df_res, columns=['Account_No', 'Transaction_Details', 'Date', 'Deposit_Amount', 'Withdrawal_Subset', 'subset_size'])
                df_res.reset_index(drop=True, inplace=True)

                model_instances = [Fraud(
                    acc_no=record[0],
                    trans_details=record[1],
                    date=record[2],
                    deposit_amt=record[3],
                    withdraw_amt=record[4],
                    subset_size=record[5]
                ) for record in df_res.values]

                Fraud.objects.bulk_create(model_instances)

            context = {
                'fraud_trans': Fraud.objects.filter(acc_no=acc_no_curr).order_by('-subset_size'),
                'accounts': list(Fraud.objects.values_list('acc_no', flat=True).distinct()),
                'form': form
            }
            return render(request, 'detect/index.html', context)
    else:
        form = MyForm()
        context = {
            'form': form,
            'fraud_trans': None,
            'accounts': None
        }
        # return redirect('http://localhost:8000')
        return render(request, 'detect/index.html', context)

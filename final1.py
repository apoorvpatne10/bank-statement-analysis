import argparse
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def create_summary(ll, i, newdf, Master_Summary, Summary):
    sum_forensic = newdf[(newdf['A']==ll)]

    sum_withdrawl = sum(sum_forensic['WITHDRAWAL AMT'])
    sum_Deposit = sum(sum_forensic['DEPOSIT AMT'])

    Master_Summary.loc[i] = [ll,sum_Deposit,sum_withdrawl]

    def set_values(x,sw,sd):
        for ele in Summary.columns:
            dfk=(sum_forensic[(sum_forensic['B']==ele) & (sum_forensic['Account No'] == int(x))])
            Summary[ele][x]=len(dfk.index)
            Summary['Bank/Firm_Name']=ll            
            sw += sum(dfk['WITHDRAWAL AMT'])
            sd += sum(dfk['DEPOSIT AMT'])
        return sw,sd

    for m in Summary.index:
        sw=0
        sd=0
        sw,sd=set_values(m,sw,sd)
        Summary['Total Withdrawl'][m]=sw
        Summary['Total Deposit'][m]=sd
    #print(Summary.head(4))
    # Summary.to_csv('Summary.csv', mode='a', header=False)


def main():

    df1 = pd.read_excel('bank.xlsx')
    list2=[]
    list1 = df1['Account No'].unique()

    newdf = pd.read_csv('bank3.csv')
    with open('result.json', 'r') as rf:
        dict1 = json.loads(rf.read())

    for i in list1:
        i = i[:-1]
        list2.append(i)

    (la,lb,lc,ld,le) = ([],[],[],[],[])
    for u in dict1:
        if dict1[u]=='A':
            la.append(u)
        elif dict1[u]=='B':
            lb.append(u)
        elif dict1[u]=='C':
            lc.append(u)
        elif dict1[u]=='D':
            ld.append(u)
        else:
            pass

    while True:
        print("Enter your choice : ")
        print("1. Banking")
        print("2. Transaction mode")
        print("3. Transfer type (FDRL)")
        print("4. Tax")
        print("5. Direct transaction")

        ch = int(input())

        if ch == 1:
            newdf['DEPOSIT AMT'].fillna(0,inplace=True)
            newdf['WITHDRAWAL AMT'].fillna(0,inplace=True)
            Master_Summary = pd.DataFrame(columns=['BANK/FIRM_NAME','TOTAL_DEPOSIT','TOTAL_WITHDRAWL'])

            column=[]
            column.append('AccountNo')
            column[1:] = lb[:]
            column.append('Bank/Firm_Name')
            column.append('Total Withdrawl')
            column.append('Total Deposit')

            Summary = pd.DataFrame(columns=column)
            Summary['AccountNo']=list2
            Summary.set_index(['AccountNo'],inplace=True)

            sum_forensic = newdf[(newdf['A']=='indiaforensic') | (newdf['A']=='indfor')]

            sum_withdrawl = sum(sum_forensic['WITHDRAWAL AMT'])
            sum_Deposit = sum(sum_forensic['DEPOSIT AMT'])

            def set_values(x,sw,sd):
                for ele in Summary.columns:
                    dfk=(sum_forensic[(sum_forensic['B']==ele) & (sum_forensic['Account No'] == int(x))])
                    Summary[ele][x]=len(dfk.index)
                    Summary['Bank/Firm_Name']='indiaforensic'
                    sw += sum(dfk['WITHDRAWAL AMT'])
                    sd += sum(dfk['DEPOSIT AMT'])
                return sw,sd

            for m in Summary.index:
                sw=0
                sd=0
                sw,sd=set_values(m,sw,sd)
                Summary['Total Withdrawl'][m]=sw
                Summary['Total Deposit'][m]=sd

            Master_Summary.loc[0] = ['Indiaforensic',sum_Deposit,sum_withdrawl]
            # Summary.to_csv('Summary.csv', mode='a', header=True)

            for ll in range(1,len(la)):
                create_summary(la[ll], ll, newdf, Master_Summary, Summary)

            Master_Summary['TOTAL_DEPOSIT'][0] = Master_Summary['TOTAL_DEPOSIT'][0] + Master_Summary['TOTAL_DEPOSIT'][2]
            Master_Summary['TOTAL_WITHDRAWL'][0] = Master_Summary['TOTAL_WITHDRAWL'][0] + Master_Summary['TOTAL_WITHDRAWL'][2]

            Master_Summary.drop(Master_Summary.index[[2]], inplace=True)
            Master_Summary.reset_index(drop=True, inplace=True)

            sns.set(style="whitegrid")

            fig=plt.figure(figsize=(15, 15))
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)

            g= sns.barplot(x='TOTAL_WITHDRAWL',y='BANK/FIRM_NAME', data=Master_Summary, palette='Set2',ax=ax1)
            g.set_xscale('log')

            g=sns.barplot(x='TOTAL_DEPOSIT',y='BANK/FIRM_NAME', data=Master_Summary, palette='hls')
            g.set_xscale('log')

            plt.show()

            print('\n\n')
            print("Master Summary\n")
            print(Master_Summary)
            print('\n\n')

            # 1.1
            print("\nEnter your choice:\n")
            for i, x in enumerate(la):
                print(f"{i+1} - {x}")

            inp = int(input())
            bank = la[inp-1]

            Summary = pd.read_csv('Summary.csv')
            df_indfor = Summary[Summary['Bank/Firm_Name'] == bank]
            df_indfor = df_indfor.astype({'cashdep':int,'neft':int,
             'imps':int,
             'rtgs':int,
             'electronic':int,
             'aeps':int,
             'nfs':int,
             'chq':int,
             'rupay':int,
             'cash':int,
             'pos':int,
             'visa':int,
             'atm':int,
             'sweep':int,
             'payu':int,
             'csh':int,
             'bbps':int,
             'stl':int,
             'master':int,
             'maestro':int,
             'e-billing':int,
             'online':int,
             'epayment':int})
            df_indfor.drop(['Bank/Firm_Name', 'Total Withdrawl','Total Deposit'], axis=1,inplace=True)
            print(df_indfor.head())
            df_indfor.set_index('AccountNo',inplace=True)


            # df_indfor.index
            plt.figure(figsize=(18,8))
            sns.heatmap(df_indfor, annot=True,cbar=False,cmap="RdYlGn_r")
            plt.show()
            plt.xticks(rotation=30)

            summ = pd.read_csv('Summary.csv')

            fig = plt.figure(figsize=(10, 13))
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)

            my_df = summ[summ["Bank/Firm_Name"] == bank]
            # plt.subplot(title="Total Withdrawl for different accounts (fdrl)")
            obj = sns.barplot(x="AccountNo", y="Total Withdrawl", data=my_df, palette="Set2", ax=ax1)
            obj.set_yscale('log')
            plt.xticks(rotation=30)

            # plt.subplot(title="Total Deposit for different accounts (fdrl)")
            obj = sns.barplot(x="AccountNo", y="Total Deposit", data=my_df, palette="Paired", ax=ax2)
            obj.set_yscale('log')
            plt.xticks(rotation=30)

            plt.show()

        elif ch == 2:
            Total_Mode = pd.DataFrame(columns=lb,index=list2)

            def create_summarY():
                def set_values(x):
                    for ele in Total_Mode.columns:
                        dfk=(newdf[(newdf['B']==ele) & (newdf['Account No'] == int(x))])
                        Total_Mode[ele][x]=len(dfk.index)

                for m in Total_Mode.index:
                    set_values(m)

            for ll in range(0,len(la)):
                create_summarY()

            Total_Mode = Total_Mode.astype({'cashdep':int,'neft':int,
                 'imps':int,
                 'rtgs':int,
                 'electronic':int,
                 'aeps':int,
                 'nfs':int,
                 'chq':int,
                 'rupay':int,
                 'cash':int,
                 'pos':int,
                 'visa':int,
                 'atm':int,
                 'sweep':int,
                 'payu':int,
                 'csh':int,
                 'bbps':int,
                 'stl':int,
                 'master':int,
                 'maestro':int,
                 'e-billing':int,
                 'online':int,
                 'epayment':int})

            # Total_Mode.index
            plt.figure(figsize=(18,12))
            sns.heatmap(Total_Mode,annot=True,cbar=False,cmap='RdYlGn_r')
            plt.xticks(rotation=30)
            plt.show()

        elif ch == 3:
            Transfer_type = pd.DataFrame(columns=['Type','Count_in_FDRL'])
            Transfer_type=Transfer_type.astype({'Type':int,'Count_in_FDRL':int})
            #Only for FDRL Bank
            df4=newdf[newdf['A']=='fdrl']
            df41 = df4[df4['C']=='internal']
            df42 = df4[df4['C']=='national']
            Transfer_type['Type']=['internal','national']
            Transfer_type['Count_in_FDRL']=[len(df41),len(df42)]
            plt.pie(Transfer_type['Count_in_FDRL'],labels=Transfer_type['Type'],startangle=90,autopct="%1.2f%%")
            plt.axis('equal')
            plt.show()

        elif ch == 4:
            Charges_Type = pd.DataFrame(columns=['Type','Count'])
            Charges_Type=Charges_Type.astype({'Type':int,'Count':int})
            df50 = newdf[newdf['D']==ld[0]]
            df51 = newdf[newdf['D']==ld[1]]
            df52 = newdf[newdf['D']==ld[2]]
            df53 = newdf[newdf['D']==ld[3]]
            df54 = newdf[newdf['D']==ld[4]]
            df55 = newdf[newdf['D']==ld[5]]
            df56 = newdf[newdf['D']==ld[6]]
            df57 = newdf[newdf['D']==ld[7]]
            Charges_Type['Type']=ld
            Charges_Type['Count']=[len(df50),len(df51),len(df52),len(df53),len(df54),len(df55),len(df56),len(df57)]
            plt.figure(figsize=(10,10))
            plt.pie(Charges_Type['Count'],labels=Charges_Type['Type'],startangle=90,autopct="%1.2f%%")
            plt.axis('equal')
            plt.show()

        elif ch == 5:
            direct = newdf[newdf['E']=='direct']
            colum = ['Account_No','Count']
            direct1 = pd.DataFrame(columns=colum)
            direct1['Count']=[0 for i in range(0,10)]

            list2=[int(lis) for lis in list2]
            direct1['Account_No']=list2

            for k in direct1.index:
                x=direct1.iloc[k,0]
                df3=direct[x==direct['Account No']]
                direct1.iloc[k,1]=len(df3)

            plt.figure(figsize=(10,6))
            g= sns.barplot(y='Count',x='Account_No', data=direct1, palette='Set2')
            g.set_yscale('log')
            plt.xticks(rotation=30)
            plt.show()

        print("Repeat? (y/n)")
        if input().lower() != 'y':
            break


if __name__ == '__main__':
    main()

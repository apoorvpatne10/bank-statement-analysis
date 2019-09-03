# bank-statement-analysis

**[MMCOE Hacksprint Winners](https://indiaforensic.com/hacksprint/)**

## Sample : All possible fradulent transactions for account no. 1196711

![demo](https://i.imgur.com/FEmZKSk.png)

Bank Statement Analysis – We've tried to build a tool to categorize the narrations appearing in the bank statements into a logical manner. The bank account statements are attached here for analysis. These are consolidated and extracted bank account statements of various bank accounts. It would be able to categorise similar transactions on the basis of narrations. 

Transaciton details in the corporate bank accounts would be read and grouped to find out the inflow and outflow of money.

We can extend our project to a point where it can find recurring, similar, transactions by discovering similarities in the description field of transaction. More data will lead to a better generalization.

## Architecture

![ARCHITECTURE DIAGRAM](https://user-images.githubusercontent.com/31184004/54874319-137dd380-4e0f-11e9-9df0-5c11b8352184.jpg)

We've provided a command line interface to the user in which he can choose one option at a time from the following list of options:

* Bank/Firm wise analytics

  * Visualized plots for total withdrawal and total deposits for each bank firm name.
  ![Hi](https://user-images.githubusercontent.com/31184004/54874234-f9db8c80-4e0c-11e9-83aa-c1f8e1da0c85.png)
  
  * Displayed master summary that shows total withdrawal and total deposits for each bank/firm.  
  ![Hi2](https://user-images.githubusercontent.com/31184004/54874241-298a9480-4e0d-11e9-943c-fb0c1c8ae50b.PNG)

  * Provided the user with available banks/firm and displayed heat map for summary of chosen bank.
  
  ![Screenshot from 2019-03-24 05-01-53](https://user-images.githubusercontent.com/31184004/54874257-7a9a8880-4e0d-11e9-8db7-314141798de7.png)
  
  ![Screenshot from 2019-03-24 05-02-06](https://user-images.githubusercontent.com/31184004/54874260-82f2c380-4e0d-11e9-8418-be993db5061b.png)
  
* Transaction Mode

Visualized heatmap for showing the correlation between account numbers and transaction modes.

![Screenshot from 2019-03-24 05-02-48](https://user-images.githubusercontent.com/31184004/54874268-b1709e80-4e0d-11e9-83fe-3f39bea1e7ed.png)

  
* Transfer Type (FDRL)

Visualized pie charts for showing percentage internal and national fund transfer in FDRL.

![Screenshot from 2019-03-24 05-03-08](https://user-images.githubusercontent.com/31184004/54874273-c9e0b900-4e0d-11e9-8dfd-4912044a3169.png)


* Charges/Tax

Visualized pie chart for showing percentage share of each type of charges/cess like tax, gst, income etc.

![Screenshot from 2019-03-24 05-03-23](https://user-images.githubusercontent.com/31184004/54874285-e41a9700-4e0d-11e9-8c0f-ca09d2756591.png)

* Direct Transactions

Visualized bar chart for showing counts of direct transaction for different account numbers.


![Screenshot from 2019-03-24 05-03-40](https://user-images.githubusercontent.com/31184004/54874289-fb598480-4e0d-11e9-8cd5-dffb8ce06583.png)

## Flowchart

![Flowchart](https://user-images.githubusercontent.com/31184004/54874317-0eb91f80-4e0f-11e9-8fdb-acc9c42b4444.jpg)

## Labelling

We've done a one time labelling for transactions in the given data. This result can be used for similar datasets as well.

* **A** : Bank/firm names
* **B** : Mode of transactions
* **C** : Type of transactions in FDRL
* **D** : Taxes/cess/charges
* **E** : Direct transactions (account to account)

```
{
   "indiaforensic":"A",
   "cashdep":"B",
   "fdrl":"A",
   "internal":"C",
   ...
   ...
   "hdfc":"A",
   "net":"D",
   "epayment":"B",
   "loan":"C",
   "cess":"D"
}
```

## Challenges faced

![thumbnail_challenges](https://user-images.githubusercontent.com/31184004/54874589-758d0780-4e14-11e9-9c5a-f2d899ad795f.jpg)

## Install the requirements

```
pip install -r requirements.txt
```

## Try it on command line 
```
apoorv@apoorv:~/Desktop$ python final_cmd.py --help
usage: final_cmd.py [-h] [--master_summary MASTER_SUMMARY]
                    [--mode_of_transfer MODE_OF_TRANSFER]
                    [--medium_of_transfer MEDIUM_OF_TRANSFER]
                    [--types_of_tax TYPES_OF_TAX]
                    [--direct_payments DIRECT_PAYMENTS]

Process some integers.

optional arguments:
  -h, --help            show this help message and exit
  --master_summary MASTER_SUMMARY
                        Infow and outflow summary for each bank/firm. Add 'm'
                        to execute this part.
  --mode_of_transfer MODE_OF_TRANSFER
                        Heat map and deposit/withdraw statistics of bank
                        transactions. Add 'hm' to execute this part.
  --medium_of_transfer MEDIUM_OF_TRANSFER
                        Specifically for FDRL. Add 'mt' to execute this part.
  --types_of_tax TYPES_OF_TAX
                        Plots pie chart for tax charges. Add 'tx' to execute
                        this part.
  --direct_payments DIRECT_PAYMENTS
                        Plots bar chart for direct payments. Add 'dp' to
                        execute this part.

```

## TODO

Labelling done for this dataset can be extended in classification applications. Basically we can train a model to recognize the text input and associate it with the output categories. 

```
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# some sample data

df=pd.DataFrame([
    ['MasterCard online Transaction at GOOGLE *TinderPlus', 'dating'],
    ['CHECKCARD AMAZON AMAZN.COM/BILLWA 125679318', 'shopping'],
    ['CHECKCARD AMAZON AMAZN.COM/BILLWA 467924720', 'shopping'],
    ['Visa Fandango.com CA Fandango.com 787879089', 'entertainment'],
    ['VISA Amazon web services aws.amazon.coWA 12321321', 'work'],
    ['Mastercard Dr Jimmy Smits DDS', 'medical'],
    # ... lots more rows
], columns=['Description','category'])

# convert the input text to something that sklearn can compute on using a TfidfVectorizer
tfidf=TfidfVectorizer()
x_train=tfidf.fit_transform(df.Description)

# we need to also encode the "target" as something the algorithm can handle (numbers)
le=LabelEncoder()
y_train=le.fit_transform(df.category)

# here's the actual ML algorithm
classifier=RandomForestClassifier(n_jobs=-1)

# train the model on your historical data
classifier.fit(x_train.todense(), y_train)

# here's our "new" data that we want to get categories for, we need to treat it the same way
txt_predict=['Amazon web services', 'Harris Teeter', 'Amazon']
x_predict=tfidf.transform(txt_predict)

# do the magic prediction!
predicted=classifier.predict(x_predict.todense())

# predict() output is just a bunch of numbers, we need to turn it back into words
actual_answers=le.inverse_transform(predicted)
print(actual_answers)
```

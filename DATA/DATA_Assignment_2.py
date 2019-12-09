	
// The code in this cell is generated by an Eider credential cell.
// If you import this notebook, UI controls will replace the code.
// The AWS Odin material set shown in the code below will be applied when you run the cell.
eider.odin.setAwsCredential("xxxxxxxxxxxxxxxxxxx)


			    
			    
			    
			    
			    
			    
import pandas as pd
import numpy as np
eider.s3.download('s3://eider-datasets/mlu/DATA_Training.csv','/tmp/DATA_Training.csv')
eider.s3.download('s3://eider-datasets/mlu/DATA_Public_Test.csv','/tmp/DATA_Public_Test.csv')
train = pd.read_csv('/tmp/DATA_Training.csv', na_values = 'null')
public_test = pd.read_csv('/tmp/DATA_Public_Test.csv', na_values = 'null')
train.head()#;public_test.head()
	
a = pd.DataFrame(list(zip(train.columns.values, train.count(axis = 0))))
b = (a[:][1] == 8347)
a = pd.DataFrame(list(zip(train.columns.values, b)))
a.columns = ["Columns", "No Missing Data"]
a

import matplotlib.pyplot as plt
train.hist(bins = 50, figsize=(22, 16), color = "k")
plt.show()


	
from pandas.plotting import scatter_matrix
 
train_set = train.copy()
 
all_attributes = ["response", "score5", "score4", "score3", "score2", "score1","hour", "prime", "contact_type", "day"]
selected_attributes = ["response", "score1","score2","score3"]
scatter_matrix(train_set[selected_attributes], figsize = (10,10), color = "k")
 
train.columns.values
corr_matrix = train_set.corr()
corr_df = pd.DataFrame(corr_matrix["response"].sort_values(ascending = False))
corr_df.columns = ["correlations to CS response"]
corr_df
#corr_matrix["score5"].sort_values(ascending = False)
#corr_matrix["score4"].sort_values(ascending = False)
#corr_matrix["score3"].sort_values(ascending = False)
#...

			    
			    
			    
#=========================ANSWER 5 - VERSION 1	
# create subset (X_train) of features that are numeric and with no missin data
X_train = train_set[["prime", "day", "hour"]][0:6000]
y_train = train_set[["response"]][0:6000]
 
X_test_pub = public_test[["prime", "day", "hour"]]
 
from sklearn import preprocessing
import numpy as np
X_scaled = preprocessing.scale(X_train)
 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import f1_score, accuracy_score
 
dt_clf = DecisionTreeClassifier(random_state = 821150)
log_clf = LogisticRegression()
rnd_clf = RandomForestClassifier(random_state = 821150)
svm_clf = SVC()
voting_clf = VotingClassifier(estimators = [ ('lr', log_clf), ('rf', rnd_clf), ('svc', svm_clf)], voting = 'hard')
 
dt_clf.fit(X_scaled, y_train)
#log_clf.fit(X_train, y_train)
#rnd_clf.fit(X_train, y_train)
#svm_clf.fit(X_train, y_train)
#voting_clf.fit(X_train, y_train)
 
def evaluate(clf):
    cross_val = cross_val_score(clf, X_scaled, y_train, cv=5)
    y_train_pred = cross_val_predict(clf, X_scaled, y_train, cv = 5)
    f1 = f1_score(y_train, y_train_pred)
    a_score = accuracy_score(y_train, y_train_pred)
    print("for ", str(clf), "\naccuracy score = ",
    round(a_score, 3), "\nthe f1_score= ", 
    f1, "\ncross_val_score= ", cross_val,
    "\ncv_score_mean= ", round(cross_val.mean(),3), "\n=============================================================================" )
 
#print(np.ravel(y_train).shape)
evaluate(dt_clf)
print(dt_clf.feature_importances_)
pd.DataFrame(X_scaled)
#y_pred=[]
#for i in np.arange(len(X_test)):
#    a = dt_clf.predict(pd.DataFrame(X_test.iloc[0]).T)
#    y_pred.append(int(a))
			    
			    
			    
			 
#==========================ANSWER 5 - VERSION 2
	
### ANSWER 5 ###
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
import numpy as np 
from sklearn import preprocessing
 
feature_cols = ['score1', 'score2', 'score3', 'score4', 'score5', 'response']
df_fetures = pd.DataFrame(train, columns=feature_cols)
df_fetures_no_missing_data = df_fetures.dropna()
sourcevars = df_fetures_no_missing_data.iloc[:, :-1].values #all columns except the last one
targetvar = df_fetures_no_missing_data.iloc[:, -1].values #only the last column
k_fold = 10
 
#class_weight: lets you specify how harshly you penalize incorrect answers of the different types, and
#max_depth: lets you control how deep the tree can be, and thus controls overfitting.
 
fscore_array = np.zeros(10)
cvscore_array = np.zeros(10)
 
## Tune class_weight 
class_weight_list = [{0: 1, 1: 1}, {0: 2, 1: 1}, {0: 3, 1: 1}, {0: 4, 1: 1}, {0: 5, 1: 1}, {0: 6, 1: 1},{0: 7, 1: 1}, {0: 8, 1: 1}, {0: 9, 1: 1}, {0: 10, 1: 1}]
 
for i in range(len(class_weight_list)):
    clf = DecisionTreeClassifier(random_state=0, class_weight=class_weight_list[i], max_depth=None)
    cv_score = cross_val_score(clf, sourcevars, targetvar, cv=k_fold)
    clf.fit(sourcevars, targetvar)
    y_train_pred = clf.predict(sourcevars)
    score_of_f1 = f1_score(targetvar, y_train_pred, average='micro')
    cvscore_array[i] = np.average(cv_score)
    fscore_array[i] = score_of_f1
    #### un-comment-out the print to get details
    #print("when class_weight = {},  average cross_val_score is {}, f1_score = {}".format(class_weight_list[i], np.average(cv_score), score_of_f1))
    
y_df=pd.DataFrame({'x': range(10), 'f1score': fscore_array, 'cvscore': cvscore_array })
# multiple line plot
plt.plot( 'x', 'f1score', data=y_df, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=2)
plt.plot( 'x', 'cvscore', data=y_df, marker='v', markersize=10, color='olive', linewidth=2)
plt.title('Tune class_weight')
plt.legend()
plt.show()
plt.close()
 
## Tune max_depth    
for step_max_depth in range(10, 20): 
    clf = DecisionTreeClassifier(random_state=0, max_depth=step_max_depth)
    cv_score = cross_val_score(clf, sourcevars, targetvar, cv=k_fold)
    clf.fit(sourcevars, targetvar)
    y_train_pred = clf.predict(sourcevars)
    score_of_f1 = f1_score(targetvar, y_train_pred, average='micro')
    cvscore_array[step_max_depth-10] = np.average(cv_score)
    fscore_array[step_max_depth-10] = score_of_f1
    #### un-comment-out the print to get details
    #print("when max_depth = {}, average cross_val_score is {}, f1_score = {}".format(step_max_depth, np.average(cv_score), score_of_f1))
    
y_df=pd.DataFrame({'x': range(10), 'f1score': fscore_array, 'cvscore': cvscore_array })
# multiple line plot
plt.figure()
plt.plot( 'x', 'f1score', data=y_df, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=2)
plt.plot( 'x', 'cvscore', data=y_df, marker='v', markersize=10, color='olive', linewidth=2)
plt.title('Tune max_depth')
plt.legend()
plt.show()
 
#when weight = {0: 3, 1: 1} and max_depth = 16, average cross_val_score is 0.9004615817151997
clf = DecisionTreeClassifier(random_state=0, class_weight={0: 3, 1: 1}, max_depth=16)
cv_score = cross_val_score(clf, sourcevars, targetvar, cv=k_fold)
clf.fit(sourcevars, targetvar)
y_train_pred = clf.predict(sourcevars)
score_of_f1 = f1_score(targetvar, y_train_pred, average='micro')
print("We choose class_weight={} and max_depth = 16, mean cross_val_score = {}, f1 = {}".format({0: 3, 1: 1}, np.average(cv_score), score_of_f1))
 
#Predict the outputs on the public test features, save them as a csv file 
no_missing_test =  public_test.fillna(public_test.mean())
public_test_fetures = pd.DataFrame(no_missing_test, columns=['score1', 'score2', 'score3', 'score4', 'score5'])
y_test_predict = clf.predict(public_test_fetures)
 
results = pd.DataFrame({'ID':no_missing_test['ID'].values,'response': y_test_predict})
results[['ID','response']].to_csv('/tmp/guess.csv', index=False)
print("Submited guess.csv at leaderboard https://leaderboard.corp.amazon.com/tasks/460/leaderboard")

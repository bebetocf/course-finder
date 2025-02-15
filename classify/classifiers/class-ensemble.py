import pandas as pd
from numpy import ravel
from numpy.core.umath_tests import inner1d

from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn import linear_model
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_validate
from output import *


def main():
    dfs = ['../data/dataset/db1.csv', '../data/dataset/db2.csv', '../data/dataset/db3.csv', '../data/dataset/db4.csv', '../data/dataset/db5.csv', '../data/dataset/db6.csv', '../data/dataset/db7.csv']
 
    f = createFile("Ensemble")
    
    for path in dfs:
        print('\n'+path)
        df = pd.read_csv(path)
        X = df.ix[:,1:df.shape[1]-1]
        y = df.ix[:,df.shape[1]-1:df.shape[1]]

        X = X.values
        y = y.values
        
        y = ravel(y)

        clf1 = RandomForestClassifier(n_estimators=500, random_state=0)
        clf2 = linear_model.LogisticRegression(C=0.01)
        clf3 = svm.SVC()
        clf4 = GaussianNB()
        clf5 = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 5), random_state=1)
        
        eclf = VotingClassifier(estimators=[('rf', clf1), ('lr', clf2), ('svm', clf3), ('nb', clf4), ('mlp', clf5)], voting='hard', n_jobs=1)
        folders = 10

        scores = cross_validate(eclf, X, y, cv=folders, scoring=('accuracy', 'precision', 'recall'), return_train_score=True)

        printResults(scores)
        saveResults(f, scores, path)

        # Saving Model
        # eclf.fit(X,y)
        # with open ("./ensemble.ml", 'wb') as fp:
        #     pickle.dump(eclf, fp)

        title = "Ensemble_" + path[-7:-4]
        plot_learning_curve(eclf, title, X, y, cv=folders, n_jobs=1)


        
if __name__ == "__main__":
    main()

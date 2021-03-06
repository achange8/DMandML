from sklearn import datasets
from sklearn import model_selection
from sklearn import naive_bayes
from sklearn import metrics


digits = datasets.load_digits()
data_train, data_test, label_train, label_test = model_selection.train_test_split(
    digits['data'], digits['target'], test_size=0.25)
targetnames = []
for name in digits['target_names']:
    targetnames.append(str(name))

# make models
model = naive_bayes.BernoulliNB()
model.fit(data_train, label_train)

#　データを分類
y_true = label_test
y_pred = model.predict(data_test)
print("真ラベル =", y_true)
print("予測ラベル =", y_pred)

# 分類結果の評価
print("精度 =", metrics.accuracy_score(y_true, y_pred))
print(metrics.classification_report(
    y_true, y_pred, target_names=targetnames))

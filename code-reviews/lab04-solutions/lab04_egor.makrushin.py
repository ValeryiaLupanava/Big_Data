import pandas as pd

from sklearn.feature_selection import VarianceThreshold

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

def transform(data):
    data = data.fillna(0.0)
    data = data.select_dtypes(exclude='object')
    return data


def main():
    raw_data = pd.read_csv('lab04_train.csv')
    data = transform(raw_data)

    var = VarianceThreshold(threshold=0)
    sample_matrix = data.drop('TARGET', axis=1)
    sample_matrix = var.fit_transform(sample_matrix)

    labels = data['TARGET']

    data_train, data_test, labels_train, label_test = train_test_split(sample_matrix, labels,
                                                                       test_size=0.368, stratify=labels)

    classifier = RandomForestClassifier(n_estimators=100, max_depth=None, n_jobs=-1)
    classifier.fit(data_train, labels_train)

    probability_labels = classifier.predict_proba(data_test)[:, 1]

    print("ROC AUC:", roc_auc_score(label_test, probability_labels))

# Prediction
    test_data = pd.read_csv('lab04_test.csv')
    test_data_nmp = transform(test_data)

    test_data_nmp = var.transform(test_data_nmp)
    probability_labels = classifier.predict_proba(test_data_nmp)[:, 1]

    test_data['target'] = pd.Series(probability_labels)
    test_data['id'] = test_data['ID']

# Save result
    result = test_data[['id', 'target']]
    result.to_csv('lab04.csv', mode='w', sep='\t')


if __name__ == "__main__":
    main()
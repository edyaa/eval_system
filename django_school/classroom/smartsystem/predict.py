import pickle
import numpy as np
import random
from sklearn.linear_model import LinearRegression


def alg():

    random_normal = np.random.normal(0, 0.35, size=2000)
    test = np.array(
        [random_normal[i] for i in range(len(random_normal)) if -1.0 < random_normal[i] and random_normal[i] < 1.0])

    grade = []

    for i in range(len(test)):

        if np.quantile(test, 0.1) < test[i] < np.quantile(test, 0.4):
            grade.append(random.randint(50, 65))

        if np.quantile(test, 0.4) < test[i] < np.quantile(test, 0.87):
            grade.append(random.randint(65, 85))

        if test[i] > np.quantile(test, 0.87):
            grade.append(random.randint(85, 100))

        if test[i] < np.quantile(test, 0.1):
            grade.append(random.randint(0, 50))

    grade = np.array(grade)

    random_data = []
    for _ in range(2000):
        random_data.append([float(random.choice(grade)), float(random.choice(grade)), float(random.choice(grade))])

    grade1 = []
    for x in random_data:
        grade1.append(float((x[0] * x[1] * x[2]) ** (1 / 3)))

    x_train = np.array(random_data)
    y_train = np.array(grade1)

    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0)

    x_train -= mean
    x_train /= std

    lm = LinearRegression()
    lm.fit(x_train, y_train)

    return lm, mean, std

model, mean, std = alg()

def predict(score1, score2, score3):
    test = np.array([[score1, score2, score3]])

    test -= mean
    test /= std
    predictions = model.predict(test)

    return round(float(predictions))
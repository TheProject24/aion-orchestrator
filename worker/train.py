import joblib;
import numpy as np;
from sklearn.linear_model import LinearRegression

print("Training the AI Model . . . ")

X_train = np.array([
    [1,1,1],
    [2,2,2],
    [1,2,3],
    [5,5,5]
])
y_train = np.array([30, 60, 60, 150])

model = LinearRegression()
model.fit(X_train, y_train)

joblib.dump(model, "lightweight_model.joblib")

print("Model trained and saved")


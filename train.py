import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report,roc_auc_score
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

df=pd.read_csv("raw_data.csv")
df=df.drop_duplicates()

#unwanted columns remove 
df=df.drop(columns=["patient_id",
    "los_hours",
    "baseline_risk_score",
    "deterioration_event",
    "deterioration_within_12h_from_admission",
    "deterioration_next_12h"])
#target column logic 
df["deterioration_next_1h"] = (
    (df["deterioration_hour"] - df["hour_from_admission"]).between(0,1)
).astype(int)

#removing the deterioration_hour column bcz our work done from generating target column so removing this column is necessary due to model not cheats
df=df.drop(columns=["deterioration_hour"])
print("this is the columns that we need to wnat as input before feature engineering ",df.drop(columns=["deterioration_next_1h"]).columns)
#eda 
plt.scatter(df["heart_rate"],df["deterioration_next_1h"])
plt.xlabel("heart  rate ")
plt.ylabel("deterioration probability")
plt.show()
plt.scatter(df["spo2_pct"],df["deterioration_next_1h"])
plt.xlabel("spo2 percentage %")
plt.ylabel("deteriorTRION probabilty ")
plt.show()
plt.hist(df["deterioration_next_1h"],bins=10,color="purple",edgecolor="pink")
plt.show()
#key insgihts _
#the patient who have hr bw 50 to  142 shows most detrioation probabliyy in their next 1 hr
#the patients who have spo2 pct 74 to 97 shows most detrioation probabliyy in their next 1 hr

#now feature engineering
df["MAP"] = (df["systolic_bp"] + 2 * df["diastolic_bp"]) / 3
df["pulse_pressure"] = df["systolic_bp"] - df["diastolic_bp"]
df["shock_index"] = df["heart_rate"] / df["systolic_bp"]
df["spo2_gap"] = 100 - df["spo2_pct"]

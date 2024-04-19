import streamlit as st
import numpy as np
import pandas as pd
import joblib


def predict_diabetes(input_data):
    # Load the model from the file
    model = joblib.load("ExtraTreesClassifiers.joblib")

    # Load the RobustScaler object
    robust_scaler = joblib.load("robust_scaler.pkl")

    # Load the StandardScaler object
    standard_scaler = joblib.load("standard_scaler.pkl")

    # Load the MinMaxScaler object
    min_max_scaler = joblib.load("min_max_scaler.pkl")

    # Robust scaling
    input_data_robust = robust_scaler.transform(
        input_data[
            [
                "Pregnancies",
                "Glucose",
                "BloodPressure",
                "SkinThickness",
                "Insulin",
                "BMI",
                "DiabetesPedigreeFunction",
                "Age",
            ]
        ]
    )

    # Standard scaling
    input_data_standard = standard_scaler.transform(input_data_robust)

    # Min-Max scaling
    input_data_scaled = min_max_scaler.transform(input_data_standard)

    # Make the prediction
    prediction = model.predict(input_data_scaled)[0]

    if prediction == 1:
        st.error("Probablemente tengas diabetes, consulta a un médico.")
    else:
        st.success("Probablemente no tengas diabetes.")


def main():
    st.title("Diagnostico de Diabetes")
    st.subheader(
        "Ingrese los valores de los siguientes elementos para realizar su diagnostico"
    )

    age = st.slider("Ingresa tu edad", 0, 130, 20)
    st.write("Indicador:", age)

    pregnancies = st.slider("¿Cuántos embarazos has tenido?", 0, 25, 0)
    st.write("N embarazos:", pregnancies)

    glucose = st.slider("Ingresa tu indicador de glucosa", 0, 200, 100)
    st.write("Indicador de glucosa:", glucose)

    blood_presure = st.slider("Ingresa tu indicador de presión sanguinea", 0, 130, 75)
    st.write("Indicador presión sanguinea:", blood_presure)

    skin_thickness = st.slider("Ingresa tu indicador de espesor de piel", 0, 100, 30)
    st.write("Indicador espesor de piel:", skin_thickness)

    insulin = st.slider("Ingresa tu indicador de insulina", 0, 900, 100)
    st.write("Indicador de insulina", insulin)

    bmi = st.slider("Ingresa tu indicador BMI", 0.0, 70.0, 35.0)
    st.write("Indicador BMI:", bmi)

    pedigree_function = st.slider(
        "Ingresa tu indicador de predisposición a la diabetes", 0.0, 3.0, 0.3
    )
    st.write("Indicador de predisposición a la diabetes:", pedigree_function)

    if st.button("Calcular"):
        input_data = pd.DataFrame(
            {
                "Pregnancies": [pregnancies],
                "Glucose": [glucose],
                "BloodPressure": [blood_presure],
                "SkinThickness": [skin_thickness],
                "Insulin": [insulin],
                "BMI": [bmi],
                "DiabetesPedigreeFunction": [pedigree_function],
                "Age": [age],
            }
        )

        predict_diabetes(input_data)


if __name__ == "__main__":
    main()

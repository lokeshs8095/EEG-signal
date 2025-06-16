import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

from speech_module import speak_text
@st.cache_data
def load_dataset():
    df = pd.read_csv("dataset/eeg_dataset.csv")
    return df

@st.cache_resource
def train_model(data):
    X = data.drop("thought", axis=1)
    y = data["thought"]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    return model, scaler

def predict_thought(model, scaler, sample):
    sample_scaled = scaler.transform([sample])
    prediction = model.predict(sample_scaled)
    return prediction[0]

def main():
    st.set_page_config(page_title="EEG Thought-to-Text", layout="centered")
    st.title("EEG Thought-to-Text Converter")

    df = load_dataset()
    model, scaler = train_model(df)

    col1, col2 = st.columns(2)
    with col1:
        alpha_ch1 = st.slider("Alpha Channel 1", 7.0, 9.0, 8.0)
        beta_ch1 = st.slider("Beta Channel 1", 13.0, 15.0, 14.0)
        gamma_ch1 = st.slider("Gamma Channel 1", 30.0, 34.0, 32.0)
    with col2:
        alpha_ch2 = st.slider("Alpha Channel 2", 7.0, 9.0, 8.2)
        beta_ch2 = st.slider("Beta Channel 2", 13.0, 15.0, 13.9)
        gamma_ch2 = st.slider("Gamma Channel 2", 30.0, 34.0, 31.9)

    if st.button("Predict Thought"):
        sample = [alpha_ch1, beta_ch1, gamma_ch1, alpha_ch2, beta_ch2, gamma_ch2]
        prediction = predict_thought(model, scaler, sample)
        st.success(f"Predicted Thought: **{prediction}**")
        speak_text(prediction)


    st.subheader("EEG Wave-length Signals")
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    wave_types = ["alpha_ch1", "beta_ch1", "gamma_ch1"]
    colors = ['blue', 'green', 'purple']

    for i, wave_type in enumerate(wave_types):
        y = df[wave_type].values
        x = np.arange(len(y))
        axs[i].plot(x, y, color=colors[i], linewidth=2)
        axs[i].fill_between(x, y, color=colors[i], alpha=0.3)
        axs[i].set_title(f"{wave_type.replace('_', ' ').title()} Waveform")
        axs[i].set_xlabel("Sample Index")
        axs[i].set_ylabel("Amplitude")
        axs[i].grid(True)

    st.pyplot(fig)

if __name__ == "__main__":
    main()

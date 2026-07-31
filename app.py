import pandas as pd  # ← REMOVE YE LINE (needed nahi)
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import predict_output, model, MODEL_VERSION
from schema.prediction_response import PredictionResponse
app = FastAPI()

@app.get('/')
def home():
    return {'message':'Insurance Premum Prediction API'}

@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None  # ← CHANGED: model is True → model is not None
    }

@app.post('/predict', response_model=PredictionResponse)
def Predict_premium(data: UserInput):  

    user_input = {  # ← CHANGED: pd.DataFrame([{...}]) → just dict
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle,
        'city_tier': data.city_tier,
        'income_lpa': data.income_Lpa,
        'occupation': data.occupation
    }

    prediction = predict_output(user_input)

    # ← CHANGED: Now returning full prediction
    return JSONResponse(
        status_code=200, 
        content={
            'predicted_category': prediction['predicted_category'],
            'confidence': prediction['confidence'],
            'class_probabilities': prediction['class_probabilities']
        }
    )
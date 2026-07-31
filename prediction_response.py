from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        description="The predicted insurance premium category based on customer profile",
        example="Premium_High"
    )
    
    confidence: float = Field(
        description="Model's confidence score (0.0 to 1.0) for the predicted category",
        example=0.92
    )
    
    class_probabilities: Dict[str, float] = Field(
        description="Probability distribution across all premium categories",
        example={
            "Premium_Low": 0.05,
            "Premium_Medium": 0.03,
            "Premium_High": 0.92
        }
    )
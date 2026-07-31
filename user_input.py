from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.city_tier import tier_1_cities,tier_2_cities


# pydantic model to evaluate income data
class UserInput(BaseModel):

    Age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the User')]
    weight: Annotated[float, Field(..., gt=0, description='weight of the User')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='height of the User')]
    income_Lpa: Annotated[int, Field(..., gt=0, description='Annual Salary of the User')]
    smoker: Annotated[bool, Field(..., description='Is User a smoker')]
    city: Annotated[str, Field(..., description='The city the user belong to')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the User')]

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v


    # computed field
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)    

    @computed_field
    @property
    def lifestyle(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.Age < 25:
            return "young"
        elif self.Age < 45:
            return "adult"
        elif self.Age < 60:
            return "middle_aged"
        return "senior"    

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
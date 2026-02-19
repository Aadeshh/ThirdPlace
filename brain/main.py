# brain/main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="The Brain - Vibe Parser")

# This schema ensures our data is high-quality and "hole-free"
class UserVibe(BaseModel):
    interests: List[str] = Field(description="List of active hobbies or fixations")
    avoidance_traits: List[str] = Field(description="Things the user dislikes or wants to avoid")
    social_energy: str = Field(description="High, Medium, or Low social stimulus preference")
    suggested_circles: List[str] = Field(description="Categories of people they would vibe with")

@app.post("/parse-vibe", response_model=UserVibe)
async def parse_vibe(raw_input: str):
    # This is where our SLM (Phi-3) or LLM logic will live.
    # For now, we'll return a mock to test the API "plumbing."
    return {
        "interests": ["Basketball", "Modular Synths"],
        "avoidance_traits": ["Loud Nightclubs", "Small Talk"],
        "social_energy": "Medium",
        "suggested_circles": ["Athletes", "Audiophiles"]
    }
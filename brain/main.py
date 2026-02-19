import os
from fastapi import FastAPI, HTTPException
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="The Brain - Vibe Parser")

# 1. Initialize our local SLM
# We set temperature to 0 for "deterministic" (consistent) results
llm = ChatOllama(model="phi3.5", temperature=0, format="json")

# 2. Define the Schema (The "No-Holes" Guarantee)
class UserVibe(BaseModel):
    interests: List[str] = Field(description="Active hobbies or fixations")
    avoidance_traits: List[str] = Field(description="Things the user dislikes or wants to avoid")
    social_energy: str = Field(description="Level: High, Medium, or Low")
    core_motivation: str = Field(description="The underlying 'why' behind their interests")

# 3. Create the System Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a social psychologist and data miner. Analyze the user's input "
               "to extract their personality profile. Focus on identifying their 'vices' "
               "and 'hobbies' but translate them into clean, actionable interests. "
               "Always return valid JSON."),
    ("user", "{input}")
])

# 4. Chain it together
# Using .with_structured_output ensures the AI adheres to our Pydantic class
structured_llm = llm.with_structured_output(UserVibe)
chain = prompt | structured_llm

@app.post("/parse-vibe", response_model=UserVibe)
async def parse_vibe(user_text: str):
    try:
        # The AI processes the messy text and spits out our clean object
        response = chain.invoke({"input": user_text})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
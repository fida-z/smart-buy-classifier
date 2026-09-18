from dotenv import load_dotenv
from google import genai
import os


def def_gemini(content):
    load_dotenv()
    GEMINI = os.getenv("GEMINI")
    client = genai.Client(api_key=GEMINI)

    prompt = f'''
    You are an automotive market analyst.
    You are given structured information about a used car, its predicted market value, market position, and the main factors affecting its valuation.
    Write exactly 3–5 concise bullet points.
    Requirements:
    - Focus only on useful buying insights.
    - Base every statement only on the provided information.
    - Do not invent facts.
    - Do not mention machine learning, AI, SHAP, prediction models, or confidence scores.
    - Do not greet the user.
    - Do not use emojis.
    - Do not repeat the numerical values unless they help explain the insight.
    - Keep each bullet under 20 words.
    - Use professional, neutral language.
    - Use markdown-friendly italics or bold when needed for emphasis, or for numbers. 
    - Use Rupee symbol when talking about prices.
    - Do not directly parrot the information given to you as input unless totally necessary.
    - Avoid generic advice such as "inspect the vehicle" or "verify documents."

    Generate insights that explain:
    - whether the asking price appears favorable,
    - some information about the make/model and general expert perception about other characters of the car itself,
    - how the car compares with similar listings,or include something about the depriciation if you are able to make sense of it.
    - any noteworthy strengths or weaknesses evident from the supplied data.
    - In the end, give an overall opinion based on what you described about whether the car is worth buying or not.

    Return the output in markdown format.
    Input:
    {content}
    '''
    return(prompt,client)

def get_gemini_stream(prompt, client):
        stream = client.interactions.create(
            model="gemini-3.8-flash", input=prompt, stream=True
        )

        for event in stream:
            if event.event_type == "step.delta" and event.delta.type == "text":
                yield event.delta.text


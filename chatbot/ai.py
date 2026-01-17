import requests
import json

def generate_response(house_info, relevant_data, user_question):
    """
    Calls Ollama to generate a response about the house.
    Uses strict prompt template.
    Returns the AI generated string.
    """
    
    # Format relevant data for the prompt
    relevant_data_str = ""
    for item in relevant_data:
        relevant_data_str += f"- {item['name']} ({item['category_display']}): {item['distance_meters']}m away\n"

    prompt = f"""You are a helpful and professional real estate assistant.

You are answering questions about ONE specific house only.

RULES:
- Use ONLY the data provided.
- Do NOT guess or invent information.
- Do NOT compare with other houses or areas.
- Keep the answer short and friendly (1–2 sentences).
- If something is not in the data, do not mention it.

HOUSE DETAILS:
Name: {house_info['name']}
Location: {house_info['location']}
Price: {house_info['price']}

RELEVANT NEARBY INFORMATION:
{relevant_data_str}

USER QUESTION:
{user_question}

FINAL ANSWER:"""

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral:7b-instruct",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except requests.exceptions.RequestException as e:
        return f"Error communicating with AI service: {str(e)}"

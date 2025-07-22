import config
import requests

async def generate_email(subject, context) -> str:
    """
    Generates a professional email using Perplexity AI's API.
    
    :param api_key: Your Perplexity API Key
    :param subject: The subject context of the email
    :param context: body context of the email
    :return: Generated email text
    """
    url = "https://api.perplexity.ai/chat/completions"
    api_key = config.API_KEY
    
    prompt = (
        f"Write a polite and professional email to notifying them that their "
        f"subscription has expired. Encourage them to renew their subscription to avoid interruption in service. start with Dear User,\n"
        f"End with 'Best regards, Indrajit Sahu, CEO of Udta Panjab'.\n"
    )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "sonar",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    response = await requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
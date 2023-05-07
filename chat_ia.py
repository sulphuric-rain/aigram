from tgconfig import ai_key
import requests


def send_chat_rq(request_text):
    URL_CHAT = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type" : "application/json", "Authorization":f"Bearer {ai_key}"}
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{request_text}"}]
    }
    response = requests.post(URL_CHAT, headers=headers, json=payload)
    return response.json().get("choices")[0].get("message").get("content")
    # return response.json().get("chices")[0].get("message").get("content")


from flask import Blueprint, jsonify, request
from openai import OpenAI
import os

ai_api = Blueprint("ai_api", __name__, url_prefix="/api/ai")

API_TOKEN = "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"
ai_model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_TOKEN,
)


@ai_api.post("/chat")
def chat():
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": "Сообщение не может быть пустым"}), 400

    try:
        response = client.chat.completions.create(
            model=ai_model,
            messages=[
                {
                    "role": "system",
                    "content": "Ты AI-помощник платформы WildRoutes. Ты помогаешь пользователям находить туры, "
                               "рассказываешь о достопримечательностях России, помогаешь с бронированием. "
                               "Ты дружелюбный, вежливый и профессиональный. Отвечай на русском языке."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        ai_response = response.choices[0].message.content

        return jsonify({
            "status": "ok",
            "response": ai_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ai_api.post("/travel-assistant")
def travel_assistant():
    """Туристический ассистент"""
    data = request.json
    user_message = data.get('message', '')
    context = data.get('context', {})

    if not user_message:
        return jsonify({"error": "Сообщение не может быть пустым"}), 400

    try:
        system_prompt = """Ты AI-помощник платформы WildRoutes для поиска и бронирования авторских путешествий.

Твои задачи:
1. Помогать пользователям находить интересные туры по России
2. Рассказывать о достопримечательностях и маршрутах
3. Консультировать по бронированию
4. Давать советы по подготовке к путешествиям
5. Рекомендовать туры на основе предпочтений пользователя

Ты дружелюбный, экспертный и вдохновляющий на путешествия.
Отвечай кратко, но информативно. Используй эмодзи для настроения.
Всегда отвечай на русском языке."""

        response = client.chat.completions.create(
            model=ai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        ai_response = response.choices[0].message.content

        return jsonify({
            "status": "ok",
            "response": ai_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
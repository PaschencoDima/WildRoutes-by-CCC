from flask import Blueprint, jsonify, request
from openai import OpenAI
import os

ai_api = Blueprint("ai_api", __name__, url_prefix="/api/ai")

# Конфигурация OpenAI
API_TOKEN = "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"
ai_model = "stepfun/step-3.5-flash:free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_TOKEN,
)


@ai_api.post("/chat")
def chat():
    """AI чат"""
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
    context = data.get('context', {})  # может содержать user_id, избранное и т.д.

    if not user_message:
        return jsonify({"error": "Сообщение не может быть пустым"}), 400

    try:
        # Формируем системный промпт с контекстом
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
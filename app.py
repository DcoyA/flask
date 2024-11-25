from flask import Flask, request, jsonify
import requests
import openai

app = Flask(__name__)

# OpenAI API Key
openai.api_key = "sk-..."  # GPT API 키 입력

# 카카오톡 REST API URL
KAKAO_API_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # 카카오톡에서 보낸 메시지 추출
    user_message = data['userRequest']['utterance']

    # GPT API 호출
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    # GPT 답변 추출
    assistant_reply = gpt_response['choices'][0]['message']['content']

    # 카카오톡 응답 구성
    response_body = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": assistant_reply
                    }
                }
            ]
        }
    }
    return jsonify(response_body)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

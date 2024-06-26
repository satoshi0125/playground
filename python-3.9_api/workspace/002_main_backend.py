from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE"))

app = Flask(__name__)


AVAILABLE_ROLES = {
    "デフォルト": "標準的なChatGPTの応答",
    "専門家": "専門的で詳細な説明を提供",
    "初心者向け": "簡単な言葉で丁寧に説明",
    "ユーモア": "ジョークを交えた明るい応答",
    "簡潔": "短く要点を押さえた応答"
}

def get_role_prompt(role):
    prompts = {
        "デフォルト": "標準的なアシスタントとして応答してください。",
        "専門家": "専門家として、詳細で正確な情報を提供してください。必要に応じて専門用語を使用しても構いません。",
        "初心者向け": "初心者に説明するように、簡単な言葉で丁寧に説明してください。専門用語は避け、例を用いて分かりやすく説明してください。",
        "ユーモア": "ユーモアを交えて明るく応答してください。適度にジョークを使い、楽しい雰囲気で会話を進めてください。",
        "簡潔": "できるだけ簡潔に、要点を押さえて応答してください。長い説明は避け、核心をついた回答を心がけてください。"
    }
    return prompts.get(role, prompts["デフォルト"])

@app.route('/')
def index():
    return render_template('index.html', roles=AVAILABLE_ROLES)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    role = data.get('role', 'デフォルト')
    messages = data.get('messages', [])

    if not messages:
        system_message = {"role": "system", "content": get_role_prompt(role)}
        messages.append(system_message)

    messages.append({"role": "user", "content": data['message']})

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages)
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply, "messages": messages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI APIキーを設定（環境変数から取得することをお勧めします）
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

# ユーザープロファイルの定義
USER_PROFILES = {
    "A": "専門家で、技術的な用語をよく使う",
    "B": "一般的な知識を持つ人で、平易な言葉を好む"
}

def translate_message(message, from_profile, to_profile):
    system_message = f"""
    あなたは、{from_profile}の人から{to_profile}の人へメッセージを翻訳する専門家です。
    元のメッセージの意味を保ちつつ、受け手にとってより理解しやすい形に変換してください。
    翻訳後のメッセージだけを返してください。
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message['content']

@app.route('/')
def index():
    return render_template('index.html', profiles=USER_PROFILES)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    message = data['message']
    from_profile = data['from_profile']
    to_profile = data['to_profile']

    translated_message = translate_message(message, USER_PROFILES[from_profile], USER_PROFILES[to_profile])

    return jsonify({"translated_message": translated_message})

if __name__ == '__main__':
    app.run(debug=True)
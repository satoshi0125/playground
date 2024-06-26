from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI APIキーを設定（環境変数から取得することをお勧めします）
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

# 拡張されたユーザープロファイルの定義
USER_PROFILES = {
    "医師": "専門的な医学用語を使用し、詳細な診断や治療方針を説明する",
    "看護師": "医療用語と一般的な言葉を組み合わせて使用し、患者のケアや日常的な医療処置について説明する",
    "薬剤師": "薬剤に関する専門知識を持ち、薬の効果や副作用について詳しく説明する",
    "患者（一般成人）": "医学的知識は限られているが、自分の症状や不安について詳しく説明できる",
    "患者（高齢者）": "医学的知識は限られており、複雑な説明を理解するのが難しいことがある。簡潔で分かりやすい説明を好む",
    "患者（子供）": "医学的知識はほとんどなく、簡単な言葉や比喩を使った説明を必要とする",
    "患者の家族": "患者の状態を心配しており、詳細な情報を求める傾向がある。医学的知識は様々",
    "医療事務員": "医療用語の基本的な知識があり、患者と医療提供者の間の調整役を務める",
    "救急救命士": "緊急時の医療処置に関する専門知識があり、簡潔で明確なコミュニケーションを好む",
    "理学療法士": "運動器系の専門用語を使用し、リハビリテーションプランについて詳しく説明する"
}

def translate_message(message, from_profile, to_profile):
    system_message = f"""
    あなたは医療現場での通訳者です。{from_profile}の人から{to_profile}の人へメッセージを翻訳します。
    元のメッセージの意味を保ちつつ、受け手にとってより理解しやすい形に変換してください。
    医療情報の正確さを維持しながら、受け手の理解度に合わせて説明を調整してください。
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
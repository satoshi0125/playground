from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY_HERE")
import os
import time

# OpenAI APIキーを設定

# 利用可能な役割とその説明
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

def chat_with_gpt(messages):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages,
        stream=True)

        collected_chunks = []
        collected_messages = []

        for chunk in response:
            collected_chunks.append(chunk)
            chunk_message = chunk.choices[0].delta
            collected_messages.append(chunk_message)

            if 'content' in chunk_message:
                print(chunk_message['content'], end='', flush=True)
                time.sleep(0.05)  # 表示速度を調整

        print("\n")  # 応答の最後に改行を追加

        full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
        return full_reply_content

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return None

def select_role():
    print("利用可能な役割:")
    for role, description in AVAILABLE_ROLES.items():
        print(f"- {role}: {description}")

    while True:
        role = input("希望する役割を選択してください: ").strip()
        if role in AVAILABLE_ROLES:
            return role
        else:
            print("無効な選択です。リストから役割を選んでください。")

def main():
    messages = []
    print("ChatGPTとの会話を開始します。終了するには 'quit' と入力してください。")

    role = select_role()
    system_message = {"role": "system", "content": get_role_prompt(role)}
    messages.append(system_message)

    print(f"\n選択された役割: {role}")
    print("会話を開始します。\n")

    while True:
        user_input = input("あなた: ")
        if user_input.lower() == 'quit':
            break

        messages.append({"role": "user", "content": user_input})
        print("ChatGPT: ", end='', flush=True)

        response = chat_with_gpt(messages)
        if response:
            messages.append({"role": "assistant", "content": response})

    print("会話を終了します。")

if __name__ == "__main__":
    main()
#!/usr/local/bin/python3

"""OpenAI API sample
OpenAIの回答を一行ずつ表示することができる
OpenAI APIの回答に他する応答を行い会話を続けることができる
"""

import os
import sys
import openai
# import tiktoken


def set_system():
    print("Setting")
    print(" example: You are an expert of Medical technology.", end="")
    ans_setting = input(" : ")
    return ans_setting


def conversation():
    # 設定
    # os.environ["REQUEST_CA_BUNDLE"] = r".¥cacert.pem"
    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""

    # OPENAI_API_KEYにキー文字列をあらかじめセット
    try:
        # openai.api_key = os.environ["OPENAI_API_KEY"]
        openai.api_key = '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'
    except KeyError:
        print("Error: please set OPENAI_API_KEY environment valiable.")
        sys.exit(1)

    messages = []

    ans_setting = set_system()
    if ans_setting != "":
        messages.append({"role": "user", "content": ans_setting})

    while True:
        question = input("Your question(exit/new): ")
        # 会話の初期化
        if question == "new":
            messages = set_system()
            question = input("Restart your question(exit: end): ")
        # quitかexitの入力で会話を終了
        if question == "quit" or question == "exit":
            return
        messages.append({"role": "user", "content": question})

        # openaiに問い合わせる
        model = "gpt-3.5-turbo"
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                stream=True  # 逐次表示のための設定
            )
        except openai.error.RateLimitError as e:
            print(e.user_message)
            break
        except openai.error.InvalidRequestError as e:
            print(e.user_message)
            break

        # AIアシスタントからの回答を逐次表示
        print("Reply from ChatGPT: ")
        temp_mes = ""
        for chunk in response:
            # 前回からの差分を取得
            diff_res = chunk['choices'][0]['delta'].get('content', '')
            if chunk['choices'][0]['finish_reason'] != None:
                # end of stream
                # tokens = response['usage']['total_tokens']
                # print(f"tokens usage: {tokens}")
                break
            # 差分を追加して表示。flush=Trueとすることによりバッファを吐き出すことで逐次的に出力されるように見える。
            print(diff_res, flush=True, end="")
            # 差分を集約して応答の全体を保持
            temp_mes += diff_res
        print("")

        # AIアシスタントからの回答を会話に加える
        # 次回は会話の記録が含まれた形で問い合わせがされる
        messages.append({"role": "user", "content": temp_mes})

        # Token数の表示
        # tokens_num = tiktoken.get_encoding(messages)
        # print(f"Token num = {tokens_num}")


if __name__ == "__main__":
    conversation()

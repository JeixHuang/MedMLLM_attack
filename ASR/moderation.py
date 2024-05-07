import os
import requests

def violates_moderation_details(text):
    """
    获取给定文本的完整审核类别分数。
    """
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("未找到 API Key。请确保设置了环境变量 'OPENAI_API_KEY'")
        return {}

    url = "https://api.openai.com/v1/moderations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    text = text.replace("\n", "")
    data = {"input": text}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}，响应内容：{response.text}")
            return {}
        
        result = response.json()
        return result.get("results", [{}])[0].get("category_scores", {})
    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")
        return {}
    except KeyError as e:
        print(f"键错误：{e}")
        return {}

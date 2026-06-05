import requests
from .config import DEEPSEEK_API_KEY

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_morning_sentence():
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = """你是一个充满智慧且严厉的考研督导智能体。你的任务是每天早晨生成一句用于激励学生的"每日一句"。

要求：
必须是英文长难句，长度在 30-50 词之间，词汇具有一定难度（考研/托福水平）。
主题必须是哲理、自律、奋斗或克服困难。
提供精准、优美的中文翻译。

输出格式必须严格如下：
【英文】：...
【中文】：...
【督导寄语】：（用一两句话结合上面的句子，催促学生立刻起床开始今天的数学/英语/专业课任务，语气要干练直接，不拖泥带水。）"""

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"今日佳句生成失败：{str(e)}"

def generate_review_report(date, focus_time, early_rise, focus_data=None):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    if focus_data:
        detail_lines = []
        for task, minutes in focus_data.items():
            hours = minutes // 60
            mins = minutes % 60
            if hours > 0:
                detail_lines.append(f"{task}：{hours}小时{mins}分钟")
            else:
                detail_lines.append(f"{task}：{mins}分钟")
        focus_detail = "\n".join(detail_lines)
    else:
        focus_detail = "无"

    prompt = f"""你是一个专业的数据分析与学习评价智能体。我会将今天用户的学习数据（包括专注时长、完成的项目）发送给你，请你生成一份简明扼要的复盘报告。

日期：{date}
早起状态：{early_rise}
专注时长：{focus_time}分钟
专注详情：
{focus_detail}

要求：
1. 首先对今天的数据进行客观总结（如：数学专注X小时，英语专注X小时）。
2. 如果总时长超过6小时，请给予适当的鼓励；如果低于1.5小时，请给出严厉的批评和调整建议。
3. 根据用户的完成情况，为明天的学习提出 1-2 条具体的改进建议。
4. 排版请使用 Markdown 格式，要求结构清晰、重点突出。"""

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 400
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"复盘报告生成失败：{str(e)}"
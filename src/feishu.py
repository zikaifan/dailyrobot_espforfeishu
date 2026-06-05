import requests
from .config import FEISHU_BOT_WEBHOOK_URL, FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_TABLE_TOKEN, FEISHU_TABLE_ID

def send_feishu_message(content):
    if not FEISHU_BOT_WEBHOOK_URL:
        return False, "飞书机器人Webhook未配置"
    
    payload = {
        "msg_type": "text",
        "content": {"text": content}
    }
    
    try:
        response = requests.post(FEISHU_BOT_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        return True, "消息发送成功"
    except Exception as e:
        return False, f"消息发送失败：{str(e)}"

def get_feishu_access_token():
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        return None, "飞书App ID或Secret未配置"
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("tenant_access_token"), None
    except Exception as e:
        return None, f"获取Token失败：{str(e)}"

def add_record_to_feishu_table(date, early_rise, focus_time, review=""):
    if not FEISHU_TABLE_TOKEN or not FEISHU_TABLE_ID:
        return False, "飞书表格配置未完成"
    
    token, err = get_feishu_access_token()
    if err:
        return False, err
    
    url = f"https://open.feishu.cn/open-apis/base/v1/tables/{FEISHU_TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": {
            "日期": date,
            "早起状态": early_rise,
            "专注时长": focus_time,
            "复盘总结": review
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return True, "记录添加成功"
    except Exception as e:
        return False, f"添加记录失败：{str(e)}"

def get_today_records_from_feishu(date):
    if not FEISHU_TABLE_TOKEN or not FEISHU_TABLE_ID:
        return None, "飞书表格配置未完成"
    
    token, err = get_feishu_access_token()
    if err:
        return None, err
    
    url = f"https://open.feishu.cn/open-apis/base/v1/tables/{FEISHU_TABLE_ID}/records/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "page_size": 100,
        "field_filter": {
            "field_name": "日期",
            "value": date
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        records = result.get("data", {}).get("items", [])
        return records, None
    except Exception as e:
        return None, f"获取记录失败：{str(e)}"

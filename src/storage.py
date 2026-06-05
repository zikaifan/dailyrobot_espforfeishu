import json
import os
from datetime import date
from .config import DATA_FILE

def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)

def add_record(date_str, early_rise="否", focus_data=None, review=""):
    init_data_file()

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        records = json.load(f)

    if date_str not in records:
        records[date_str] = {
            "早起状态": early_rise,
            "专注数据": {},
            "复盘总结": review
        }
    else:
        records[date_str]["早起状态"] = early_rise
        if focus_data is not None:
            records[date_str]["专注数据"].update(focus_data)
        if review:
            records[date_str]["复盘总结"] = review

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def get_today_record():
    init_data_file()
    today = date.today().strftime("%Y-%m-%d")

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        records = json.load(f)

    if today in records:
        record = records[today]
        total_focus = sum(record.get("专注数据", {}).values())
        return {
            "日期": today,
            "早起状态": record.get("早起状态", "否"),
            "专注时长": total_focus,
            "专注数据": record.get("专注数据", {}),
            "复盘总结": record.get("复盘总结", "")
        }
    return None

def update_focus_time(focus_minutes, task="通用"):
    today = date.today().strftime("%Y-%m-%d")
    record = get_today_record()

    if record:
        focus_data = record.get("专注数据", {})
        current_time = focus_data.get(task, 0)
        focus_data[task] = current_time + focus_minutes
        add_record(today, record.get("早起状态", "否"), focus_data, record.get("复盘总结", ""))
    else:
        add_record(today, "否", {task: focus_minutes}, "")

def update_early_rise():
    today = date.today().strftime("%Y-%m-%d")
    record = get_today_record()

    if record:
        add_record(today, "是", record.get("专注数据", {}), record.get("复盘总结", ""))
    else:
        add_record(today, "是", {}, "")

def update_review(review):
    today = date.today().strftime("%Y-%m-%d")
    record = get_today_record()

    if record:
        add_record(today, record.get("早起状态", "否"), record.get("专注数据", {}), review)
    else:
        add_record(today, "否", {}, review)
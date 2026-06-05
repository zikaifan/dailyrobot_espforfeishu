import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
FEISHU_BOT_WEBHOOK_URL = os.getenv("FEISHU_BOT_WEBHOOK_URL")
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
FEISHU_TABLE_TOKEN = os.getenv("FEISHU_TABLE_TOKEN")
FEISHU_TABLE_ID = os.getenv("FEISHU_TABLE_ID")

COLUMN_DATE = os.getenv("COLUMN_DATE", "日期")
COLUMN_EARLY_RISE = os.getenv("COLUMN_EARLY_RISE", "早起状态")
COLUMN_FOCUS_TIME = os.getenv("COLUMN_FOCUS_TIME", "专注时长")
COLUMN_REVIEW = os.getenv("COLUMN_REVIEW", "复盘总结")

DATA_FILE = "study_data.json"

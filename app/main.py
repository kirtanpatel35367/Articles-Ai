from dotenv import load_dotenv
from fastapi import FastAPI
from apscheduler.schedulers.background import  BackgroundScheduler
import logging
load_dotenv()
from app.news_ingestion.fetch_news_api import fetch_ai_news
from app.delivery.email_sender import send_email
from app.db.database import Base,engine
from app.news_ingestion.article_save import save_article_to_db
from zoneinfo import ZoneInfo
from app.db.models import News

Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Agentic AI",version="0.1")
recipients = ["kp534422@gmail.com", "another@gmail.com", "test@example.com"]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/fetch/news")
def fetch_news():
    articles =  fetch_ai_news()
    save_article_to_db(articles)

def run_daily_digest():
    logging.info("Running daily digest pipeline...")
    articles = fetch_ai_news()
    save_article_to_db(articles)

def send_mail():
    return send_email("kp534422@gmail.com", "Welcome", "Abhi.. !")

# send_mail()
fetch_news()
scheduler = BackgroundScheduler(timezone=ZoneInfo("Asia/Kolkata"))  # Set scheduler tz to IST
scheduler.add_job(run_daily_digest, "cron", hour=8, minute=30)  # 8:30 AM IST
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

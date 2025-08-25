from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import News
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from app.delivery.email_sender import send_email
from dotenv import load_dotenv
import os

load_dotenv()
import asyncio

def save_article_to_db(articles):
    db: Session = SessionLocal()
    new_articles = []  # collect inserted ones
    recipients = os.getenv("MAIL_RECIPIENTS").split(",")

    try:
        for article in articles:
            published_at = None
            if article.get("published_at"):
                try:
                    published_at = datetime.fromisoformat(
                        article["published_at"].replace("Z", "+00:00")
                    )
                except Exception:
                    published_at = None

            stmt = insert(News).values(
                title=article.get("title", "Untitled"),
                description=article.get("description", ""),
                url=article.get("url"),
                source=article.get("source", "Unknown"),
                published_at=published_at,
                points=article.get("points", 0),
                author=article.get("author", "Anonymous"),
            ).on_conflict_do_nothing(index_elements=["url"])

            result = db.execute(stmt)
            if result.rowcount > 0:  # ✅ new record added
                new_articles.append(article)

        db.commit()

        # ✅ Send email only if new articles exist
        if new_articles:
            body = "\n\n".join(
                [f"{a.get('title')} - {a.get('url')}" for a in new_articles[:5]]
            )
            send_email(
                recipients,
                f"{len(new_articles)} New AI Articles",
                body
            )
            print("✅ Email sent with", len(new_articles), "articles")
        else:
            print("⚠️ No new articles, no email sent")

    except Exception as e:
        db.rollback()
        print("DB Error:", e)
    finally:
        db.close()

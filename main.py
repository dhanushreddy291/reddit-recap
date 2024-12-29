from datetime import datetime, timedelta

from generate_audio import generate_audio_from_text
from llm import generate_reddit_news_summary
from reddit import get_reddit_scraping_tasks
from upload import upload_file

subreddits = ["singularity", "LocalLLaMA", "homeautomation"]

if __name__ == "__main__":
    for subreddit in subreddits:
        responses = get_reddit_scraping_tasks(subreddit)

        reddit_text = ""
        for response in responses:
            for post in response:
                url, title, description = (
                    post["url"],
                    post["title"],
                    post["description"],
                )
                text = """========================================
            Title: {title}
            Description: {description}
            """.format(
                    title=title, description=description
                )
                reddit_text += text
                print(text)
            print(
                f"Total number of posts scraped: {len(response)}"
                if response
                else "No posts scraped"
            )

        utc_now = datetime.utcnow()
        # Convert to IST
        ist_now = utc_now + timedelta(hours=5, minutes=30)
        current_time_in_ist = ist_now.strftime("%I %p").split()[0]

        # Subtract 2 hours from IST time
        time_2_hours_ago = (ist_now - timedelta(hours=2)).strftime("%I %p").split()[0]

        reddit_news_summary = generate_reddit_news_summary(
            reddit_text, subreddit, time_2_hours_ago, current_time_in_ist
        )

        audio_path = f"reddit_news_summary_{subreddit}_{str(utc_now)}.mp3"
        generate_audio_from_text(reddit_news_summary["content"], audio_path)

        upload_file(audio_path, "hackathon", audio_path)

        print(f"Reddit news summary for {subreddit} generated and uploaded.")

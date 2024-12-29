import json
import os

from google import genai
from google.genai import types
from pydantic import BaseModel

from generate_audio import generate_audio_from_text

client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))


class News(BaseModel):
    content: str


REDDIT_BASE_PROMPT = """Summarize these reddit news as a professional news report. Say one news after the other as a professional anchor having good connection between sentences as news item changes.
Ignore any news that doesnt have much info and make news so that it condenses all content into easy to assimilate form.
The subreddit name is {subreddit_name}, so we are making this news as a summary for the subreddit and we can say that in the video that this is summary of posts in the past 2 hours from {start_time} to {end_time}.
"""


def generate_reddit_news_summary(contents, subreddit_name, start_time, end_time):
    message = (
        REDDIT_BASE_PROMPT.format(
            subreddit_name=subreddit_name, start_time=start_time, end_time=end_time
        )
        + "\n\n"
        + contents
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=message,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=News,
            system_instruction="You are professional news anchor.",
        ),
    )
    return json.loads(response.text)


if __name__ == "__main__":
    with open("mock_data/reddit_posts.txt") as f:
        contents = f.read()
    subreddit_name = "singularity"
    start_time = "9 AM"
    end_time = "11 AM"
    response = generate_reddit_news_summary(
        contents, subreddit_name, start_time, end_time
    )

    with open("mock_data/reddit_news_summary.json", "w") as f:
        json.dump(response, f, indent=4)
    print("News summary generated successfully!")

    with open("mock_data/reddit_news_summary.json", "r") as f:
        response = json.load(f)
    generate_audio_from_text(response["content"], "mock_data/reddit_news_summary.mp3")
    print("Audio generated successfully!")

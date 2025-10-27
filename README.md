## Reddit Recap: Powered by Thordata!

![Reddit Recap](./images/WebApp.png)

Let's face it, Reddit is a treasure trove of information, entertainment, and community. But keeping up with your favorite subreddits can feel like trying to drink from a firehose. Endless scrolling, sifting through comments, and trying to distill the important stuff takes time and effort.

That's why I built [**Reddit Recap**](https://reddit-recap-woad.vercel.app/), an app designed to cut through the noise and deliver concise summaries of what's happening in your chosen subreddits, all conveniently available in a beautiful web app – and even as an audio briefing you can listen to on the go!

This project is powered by **Thordata**.

![Thordata](./images/Thordata.png)

I wanted to tackle a personal problem I've faced: staying up-to-date with the latest discussions and news in the communities I care about. Reddit, with its dynamic content and robust anti-scraping measures, presented the perfect challenge.

### The Reddit Scraping Hurdle: Why Thordata Was Essential

Anyone who's tried to scrape Reddit knows it's not a walk in the park. The platform actively blocks traditional scraping methods, making it incredibly difficult to reliably collect the data you need. IP blocking, CAPTCHAs, and constantly evolving page structures are just some of the obstacles.

This is where **Thordata** came to the rescue. Their network of fast and reliable residential IPs is specifically designed to overcome these challenges. For Reddit Recap, I leveraged Thordata's proxy network to reliably access Reddit posts and information, bypassing the complexities of building and maintaining my own scraping infrastructure.

This was a game-changer! Instead of spending countless hours battling anti-scraping techniques, I could focus on the core logic of my app: summarizing and presenting the information in a user-friendly way.

Thordata offers a **[Free Trial and a 30% permanent discount](https://www.thordata.com/?ls=EDBORvrR&lk=wb)**, making it incredibly accessible to get started.

### How Reddit Recap Works: A Peek Under the Hood

![Architecture Overview](./images/Architecture.png)

Here's a breakdown of the process behind Reddit Recap, as illustrated in the architecture overview:

1. **Targeted Scraping with Thordata:** Using the [Thordata network](https://www.thordata.com/?ls=EDBORvrR&lk=wb), I can efficiently pull the latest top posts from designated subreddits like [r/singularity](https://www.reddit.com/r/singularity/), [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/), and [r/homeautomation](https://www.reddit.com/r/homeautomation/). Thordata handles the heavy lifting of routing requests through its residential IPs to avoid any blocking mechanisms. This is triggered by a **CRON job that runs every 2 hours**, powered by [GitHub Actions](https://github.com/features/actions).

2. **News Summary with Gemini:** The raw scraped data is then fed into a Python script (`llm.py`) which utilizes **Google Gemini**. A carefully crafted prompt instructs Gemini to summarize the key news and discussions from the scraped posts, acting like a professional news anchor delivering concise updates. The prompt also specifies the subreddit and the time window for the summary, adding valuable context.

3. **From Text to Voice:** To make consuming information even easier, the summarized text is then passed to a Text-to-Speech engine, specifically **edge-tts**. This generates a natural-sounding audio file of the news summary.

4. **Storing the Audio:** The generated audio files are then uploaded to **Amazon S3** for storage. This allows for easy streaming and access within the web application.

5. **Database for Tracking:** The URL of the stored audio file in S3 is then recorded in a **PostgreSQL database**. This helps manage and link the audio summaries within the web app.

6. **Web App:** Finally, the summarized text and the link to the audio file are presented in an intuitive and visually appealing web application. You can read the summary or simply hit play to listen to the latest Reddit recap for your favorite communities.

### The Benefits of Reddit Recap

Reddit Recap offers several key advantages for busy individuals:

- **Stay Informed Effortlessly:** No more endless scrolling! Get the gist of what's happening in your favorite subreddits in minutes.
- **Audio Summaries on the Go:** Listen to your Reddit news during your commute, workout, or while doing chores.
- **Time Savings:** Reclaim valuable time by quickly catching up on relevant discussions.
- **Clean and Organized Presentation:** The web app provides a clear and easy-to-navigate interface for accessing the summaries.

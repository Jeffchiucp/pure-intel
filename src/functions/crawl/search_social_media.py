# import os
# from typing import List, Dict
# from dotenv import load_dotenv
# from openai import OpenAI
# from toolhouse import Toolhouse
# import json
# import re

# # Load environment variables
# load_dotenv()

# # Set API Keys
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# th = Toolhouse(api_key=os.getenv('TOOLHOUSE_API_KEY'), provider="openai")

# # Define the OpenAI model
# MODEL = 'gpt-4'

# def search_tweets(username: str, max_results: int = 10) -> List[Dict[str, str]]:
#     search_query = f"from:{username}"
#     messages = [{
#         "role": "user",
#         "content": f"Search X for the most recent {max_results} tweets {search_query}. Return the results as a JSON array of objects, each with 'id', 'text', and 'date' fields."
#     }]

#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=messages,
#         tools=th.get_tools()
#     )

#     messages += th.run_tools(response)

#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=messages
#     )

#     content = response.choices[0].message.content
#     print("Raw content:")
#     print(content)

#     try:
#         # Try to extract JSON from the content
#         json_match = re.search(r'\[[\s\S]*\]', content)
#         if json_match:
#             tweets = json.loads(json_match.group())
#             if isinstance(tweets, list):
#                 return tweets
#     except json.JSONDecodeError:
#         print("Error decoding JSON. Falling back to text parsing.")

#     # Fallback: Parse text content if JSON extraction fails
#     tweets = []
#     lines = content.split('\n')
#     current_tweet = {}
#     for line in lines:
#         if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
#             if current_tweet:
#                 tweets.append(current_tweet)
#                 current_tweet = {}
#             parts = line.split(': ', 1)
#             if len(parts) > 1:
#                 current_tweet['text'] = parts[1].strip('"')
#         elif 'Date:' in line:
#             current_tweet['date'] = line.split('Date:', 1)[1].strip()
#         elif 'ID:' in line:
#             current_tweet['id'] = line.split('ID:', 1)[1].strip()

#     if current_tweet:
#         tweets.append(current_tweet)

#     return tweets

# def print_tweets(username: str, tweets: List[Dict[str, str]]):
#     print(f"\nHere are some tweets by {username}:")
#     for i, tweet in enumerate(tweets, 1):
#         print(f"{i}. [Tweet](https://twitter.com/{username}/status/{tweet.get('id', 'N/A')}): \"{tweet.get('text', 'N/A')}\"")
#         print(f"   Date: {tweet.get('date', 'N/A')}")
#         print()

#     print(f"\nTotal tweets retrieved: {len(tweets)}")
#     print(f"Search query: from:{username}")

# if __name__ == "__main__":
#     username = input("Enter the Twitter handle (without @): ")
#     max_results = 10
#     tweets = search_tweets(username, max_results)
#     print_tweets(username, tweets)


import os
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from toolhouse import Toolhouse
import json
import re
import asyncio
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Load environment variables
load_dotenv()

# Set API Keys
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
th = Toolhouse(api_key=os.getenv('TOOLHOUSE_API_KEY'), provider="openai")

# Define the OpenAI model
MODEL = 'gpt-4'

# Download NLTK data
nltk.download('vader_lexicon')

def search_social_media(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    messages = [{
        "role": "user",
        "content": f"Search social media for the most recent {max_results} posts related to '{query}'. Include posts from Twitter, Telegram, and relevant RSS feeds. Return the results as a JSON array of objects, each with 'platform', 'id', 'text', 'date', and 'url' fields."
    }]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=th.get_tools()
    )

    messages += th.run_tools(response)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    content = response.choices[0].message.content

    try:
        json_match = re.search(r'\[[\s\S]*\]', content)
        if json_match:
            posts = json.loads(json_match.group())
            if isinstance(posts, list):
                return posts
    except json.JSONDecodeError:
        print("Error decoding JSON. Falling back to text parsing.")

    # Fallback parsing logic here (similar to the original code)
    # ...

def analyze_sentiment(text: str) -> str:
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    if sentiment_score > 0.05:
        return "Positive"
    elif sentiment_score < -0.05:
        return "Negative"
    else:
        return "Neutral"

def identify_topics(texts: List[str], n_topics: int = 3) -> List[str]:
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(tfidf)

    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
        topics.append(", ".join(top_words))

    return topics

def generate_report(posts: List[Dict[str, str]]) -> Dict:
    texts = [post['text'] for post in posts]
    sentiments = [analyze_sentiment(text) for text in texts]
    topics = identify_topics(texts)

    report = {
        "total_posts": len(posts),
        "sentiment_summary": {
            "Positive": sentiments.count("Positive"),
            "Neutral": sentiments.count("Neutral"),
            "Negative": sentiments.count("Negative")
        },
        "top_topics": topics,
        "posts": posts
    }

    return report

async def monitor_conflict_zone(query: str, interval: int = 3600):
    while True:
        posts = search_social_media(query)
        report = generate_report(posts)

        print(f"Report for query: '{query}'")
        print(f"Total posts: {report['total_posts']}")
        print("Sentiment summary:", report['sentiment_summary'])
        print("Top topics:", report['top_topics'])
        print("\nSample posts:")
        for post in report['posts'][:5]:
            print(f"[{post['platform']}] {post['text'][:100]}...")

        print(f"\nWaiting {interval} seconds before next update...")
        await asyncio.sleep(interval)

if __name__ == "__main__":
    query = input("Enter the conflict zone or topic to monitor: ")
    asyncio.run(monitor_conflict_zone(query))
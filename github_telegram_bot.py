import requests
import time
import os

# Telegram Bot Token & Channel ID
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# GitHub Trending API URL
GITHUB_API_URL = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"


def get_trending_repos():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        return response.json()["items"][:5]  # Get top 5 trending repos
    return []


def send_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)


def main():
    trending_repos = get_trending_repos()
    for repo in trending_repos:
        message = f"🔥 *{repo['name']}* by *{repo['owner']['login']}*\n" \
                  f"⭐ Stars: {repo['stargazers_count']}\n" \
                  f"📂 Language: {repo['language']}\n" \
                  f"🔗 [GitHub Link]({repo['html_url']})"
        send_message_to_telegram(message)
        time.sleep(5)  # To avoid rate limiting


if __name__ == "__main__":
    main()

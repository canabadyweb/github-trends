mport requests
import time
import os
import ratelimit

# Telegram Bot Token & Channel ID
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# GitHub Trending API URL
GITHUB_API_URL = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"

# Rate limiting
@ratelimit.limits(calls=60, period=3600)  # 60 calls per hour
def get_trending_repos():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()["items"][:5]  # Get top 5 trending repos
    except requests.RequestException as e:
        print(f"Error: {e}")
        return []

def extract_repo_info(repo):
    return {
        "name": repo["name"],
        "owner": repo["owner"]["login"],
        "stars": repo["stargazers_count"],
        "language": repo["language"],
        "description": repo["description"],
        "topics": repo["topics"],
        "contributors": repo["contributors"],
        "html_url": repo["html_url"]
    }

def format_telegram_message(repo_info):
    message = f"🔥 *{repo_info['name']}* by *{repo_info['owner']}*\n" \
              f"⭐ Stars: {repo_info['stars']}\n" \
              f"📂 Language: {repo_info['language']}\n" \
              f"🔗 [GitHub Link]({repo_info['html_url']})\n" \
              f"{repo_info['description']}\n" \
              f"Topics: {', '.join(repo_info['topics'])}\n" \
              f"Contributors: {', '.join(repo_info['contributors'])}"
    return message

def send_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def main():
    trending_repos = get_trending_repos()
    for repo in trending_repos:
        repo_info = extract_repo_info(repo)
        message = format_telegram_message(repo_info)
        send_message_to_telegram(message)
        time.sleep(5)  # To avoid rate limiting

if __name__ == "__main__":
    main()

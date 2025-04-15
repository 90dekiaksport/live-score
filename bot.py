import requests
import time
from telegram import Bot

# === CONFIGURATION ===
API_KEY = "afa48383dcca41f289cc2b62f675d8fe"
TELEGRAM_TOKEN = "7607642772:AAEYXkLwyP7dfBF3XJyRe9jGMSDRlEteFvg"
CHANNEL_USERNAME = "@football_picture"  # or channel ID like -100123456789

# Track goals to avoid duplicates
previous_goals = {}

# Translate popular teams to Amharic
team_translations = {
    "Real Madrid": "ሪያል ማድሪድ",
    "Barcelona": "ባርሴሎና",
    "Manchester United": "ማንችስተር ዩናይትድ",
    "Manchester City": "ማንችስተር ሲቲ",
    "Chelsea": "ቼልሲ",
    "Liverpool": "ሊቨርፑል",
    "Arsenal": "አርሴናል",
    "Tottenham": "ቶተንሃም",
    "Bayern Munich": "ባየርን ሙኒክ",
    "Paris Saint Germain": "ፓሪስ ሳን ጀርመን",
    "Juventus": "ጁቬንቱስ",
    "Inter": "ኢንተር",
    "AC Milan": "ኤሲ ሚላን",
    "Atletico Madrid": "አትሌቲኮ ማድሪድ",
    "Napoli": "ናፖሊ",
    "Roma": "ሮማ",
    "Borussia Dortmund": "ቦሩስያ ዶርትሙንድ",
    "RB Leipzig": "አርቢ ላይፕዚግ",
    "Ajax": "አያክስ",
    "Porto": "ፖርቶ",
    "Benfica": "ቤንፊካ",
    "aston villa" : "አስቶንቪላ"
}

def translate(name):
    return team_translations.get(name, name)

def get_live_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {
        "x-apisports-key": "afa48383dcca41f289cc2b62f675d8fe"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def send_goal_update(bot, home, away, home_goals, away_goals, league, minute):
    home_am = translate(home)
    away_am = translate(away)

    message = (
        "🥅 ጎልልልልልልልልልልልልልልልልልልል! 🔥🔥\n"
        f"⚽ {home_am} {home_goals} - {away_goals} {away_am}\n"

    )

    bot.send_message(chat_id=CHANNEL_USERNAME, text=message)

def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    print("⚽ Bot is running...")
    while True:
        data = get_live_matches()
        for fixture in data.get("response", []):
            fixture_id = fixture["fixture"]["id"]
            teams = fixture["teams"]
            goals = fixture["goals"]
            league = fixture["league"]["name"]
            minute = fixture["fixture"]["status"].get("elapsed", 0)

            home = teams["home"]["name"]
            away = teams["away"]["name"]
            home_goals = goals["home"]
            away_goals = goals["away"]

            # Filter: Only post for selected teams/leagues (optional)
            important_teams = ["Real Madrid", "Barcelona", "Manchester United", "Arsenal"]
            if home not in important_teams and away not in important_teams:
                continue

            # Only post if new goal
            prev = previous_goals.get(fixture_id, (None, None))
            if (home_goals, away_goals) != prev:
                previous_goals[fixture_id] = (home_goals, away_goals)
                send_goal_update(bot, home, away, home_goals, away_goals, league, minute)

        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    main()

import wikipedia
import datetime
import random
import webbrowser
import platform
import os
import requests
import ast
import operator
from textblob import TextBlob

class SmartBot:
    def __init__(self, name="SmartBot"):
        self.name = name
        self.serpapi_key = "YOUR_SERPAPI_KEY"
        self.weather_api_key = "c02f628f0feaf1227fe1e64b17dbc36c"
        self.news_api_key = "9ca7213b0ac4a815f6b756e9b6c4dbf2"

        self.greetings = [
            "Hello! I’m SmartBot. Ask me anything!",
            "Hi there! Ready to learn something new?",
            "Hey! I'm your assistant. What can I do for you today?"
        ]

        self.welcome_message = "👋 Hello! Type **help** to see what I can do."

    def help(self):
        return (
            "🤖 SmartBot Help Menu:\n"
            "- 'who is [name]' → Wikipedia + fallback\n"
            "- 'weather in [city]' → Weather info\n"
            "- 'news' or 'news about [topic]' → Latest news\n"
            "- 'time' or 'date' → Current time/date\n"
            "- 'open [site]' or 'search [query]' → Browser actions\n"
            "- 'os' → Show system info\n"
            "- 'calculate [expression]' → Math\n"
            "- 'day of [YYYY-MM-DD]' → Find the day\n"
            "- 'my ip' → IP and location\n"
            "- 'quote' → Quote of the day\n"
            "- 'joke' or 'fact' → For fun\n"
            "- 'define [word]' → Dictionary\n"
            "- 'play [song]' → YouTube\n"
            "- 'about me' → Personal info\n"
            "- 'exit' → Quit\n"
        )

    def get_summary(self, query):
        try:
            return wikipedia.summary(query, sentences=3)
        except wikipedia.exceptions.DisambiguationError as e:
            return f"'{query}' is too broad. Try: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return self.google_fallback(query)
        except Exception:
            return self.google_fallback(query)

    def google_fallback(self, query):
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "engine": "google",
                "num": 1
            }
            res = requests.get(url, params=params)
            data = res.json()

            answer_box = data.get("answer_box")
            if answer_box:
                return answer_box.get("answer") or answer_box.get("snippet") or answer_box.get("content", "")
            results = data.get("organic_results", [])
            if results and "snippet" in results[0]:
                return results[0]["snippet"]
            return "Sorry, I couldn't find an answer."
        except Exception as e:
            return f"Google search failed: {str(e)}"

    def get_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": self.weather_api_key, "units": "metric"}
            data = requests.get(url, params=params).json()
            if data["cod"] != 200:
                return f"Weather not found for '{city}'."
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            return (
                f"🌤 Weather in {city.capitalize()}:\n"
                f"- {weather}\n- Temp: {temp}°C (Feels like {feels_like}°C)\n- Humidity: {humidity}%"
            )
        except Exception as e:
            return f"Failed to fetch weather: {str(e)}"

    def get_news(self, topic=""):
        try:
            query = topic if topic else "latest"
            url = "https://gnews.io/api/v4/search"
            params = {
                "q": query,
                "lang": "en",
                "token": self.news_api_key,
                "max": 3
            }
            res = requests.get(url, params=params)
            data = res.json()
            articles = data.get("articles", [])
            if not articles:
                return "No news found."
            response = f"📰 News about {query}:\n"
            for i, article in enumerate(articles, 1):
                response += f"{i}. {article['title']} ({article['source']['name']})\n{article['url']}\n"
            return response
        except Exception as e:
            return f"Error fetching news: {str(e)}"

    def get_time(self):
        return f"🕒 Current time: {datetime.datetime.now().strftime('%H:%M:%S')}"

    def get_date(self):
        return f"🗓️ Today's date: {datetime.date.today().strftime('%Y-%m-%d')}"

    def os_info(self):
        info = {
            "System": platform.system(),
            "Node": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor()
        }
        return "🖥 OS Info:\n" + "\n".join([f"{k}: {v}" for k, v in info.items()])

    def open_website(self, site):
        urls = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://www.github.com"
        }
        site = site.lower()
        if site in urls:
            webbrowser.open(urls[site])
            return f"🔗 Opening {site}..."
        else:
            return f"No shortcut for '{site}'."

    def search_google(self, query):
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"🔍 Searching Google for '{query}'..."

    def calculate(self, expression):
        try:
            allowed_ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.USub: operator.neg
            }

            def eval_node(node):
                if isinstance(node, ast.BinOp):
                    left = eval_node(node.left)
                    right = eval_node(node.right)
                    op_type = type(node.op)
                    if op_type in allowed_ops:
                        return allowed_ops[op_type](left, right)
                elif isinstance(node, ast.UnaryOp):
                    operand = eval_node(node.operand)
                    op_type = type(node.op)
                    if op_type in allowed_ops:
                        return allowed_ops[op_type](operand)
                elif isinstance(node, ast.Num):
                    return node.n
                elif isinstance(node, ast.Constant):
                    return node.value
                raise ValueError("Invalid expression")

            parsed = ast.parse(expression, mode='eval')
            result = eval_node(parsed.body)
            return f"🧮 Result: {result}"
        except Exception:
            return "⚠️ Invalid math expression. Use +, -, *, /, ** only."

    def day_of_date(self, date_str):
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return f"📅 That day was a {date_obj.strftime('%A')}."
        except:
            return "Invalid date format. Use YYYY-MM-DD."

    def get_ip_location(self):
        try:
            res = requests.get("https://ipinfo.io/json").json()
            return (
                f"🌍 IP Info:\nIP: {res.get('ip')}\nCity: {res.get('city')}\n"
                f"Region: {res.get('region')}\nCountry: {res.get('country')}\nOrg: {res.get('org')}"
            )
        except:
            return "Could not retrieve IP info."

    def get_quote(self):
        try:
            res = requests.get("https://zenquotes.io/api/random").json()
            return f"💬 {res[0]['q']} — {res[0]['a']}"
        except:
            return "Could not fetch quote."

    def get_joke(self):
        try:
            res = requests.get("https://official-joke-api.appspot.com/random_joke").json()
            return f"🤣 {res['setup']} — {res['punchline']}"
        except:
            return "No jokes found."

    def get_fact(self):
        try:
            res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
            return f"🧠 Fun Fact: {res['text']}"
        except:
            return "Could not fetch a fact."

    def define_word(self, word):
        try:
            res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}").json()
            definition = res[0]["meanings"][0]["definitions"][0]["definition"]
            example = res[0]["meanings"][0]["definitions"][0].get("example")
            synonyms = res[0]["meanings"][0]["definitions"][0].get("synonyms", [])
            antonyms = res[0]["meanings"][0]["definitions"][0].get("antonyms", [])

            reply = f"📘 Definition of '{word}':\n- {definition}"
            if example:
                reply += f"\n🔍 Example: {example}"
            if synonyms:
                reply += f"\n🔹 Synonyms: {', '.join(synonyms[:5])}"
            if antonyms:
                reply += f"\n🔴 Antonyms: {', '.join(antonyms[:5])}"
            return reply
        except:
            return f"Definition for '{word}' not found."

    def play_youtube(self, query):
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"🎵 Playing '{query}' on YouTube..."

    def about_me(self):
        return (
            "👤 About Aditya:\n"
            "- Age: 19\n"
            "- Branch: CSE student\n"
            "- Birthday: July 22\n"
            "- Hobbies: Coding, blogging, music, tech exploring"
        )

    def handle_input(self, user_input):
        user_input = user_input.strip().lower()
        known_greetings = ["hello", "hi", "hey"]

        if user_input in known_greetings:
            return f"{random.choice(self.greetings)}\n💡 Type 'help' to see what I can do."
        if user_input == "exit":
            return "👋 Goodbye!"
        if user_input == "help":
            return self.help()
        if user_input == "time":
            return self.get_time()
        if user_input == "date":
            return self.get_date()
        if user_input == "os":
            return self.os_info()
        if user_input.startswith("open "):
            return self.open_website(user_input[5:])
        if user_input.startswith("search "):
            return self.search_google(user_input[7:])
        if user_input.startswith("weather in "):
            return self.get_weather(user_input.replace("weather in ", "").strip())
        if user_input.startswith("news about "):
            return self.get_news(user_input.replace("news about ", "").strip())
        if user_input == "news":
            return self.get_news()
        if user_input.startswith("calculate "):
            return self.calculate(user_input.replace("calculate ", ""))
        if user_input.startswith("day of "):
            return self.day_of_date(user_input.replace("day of ", "").strip())
        if user_input == "my ip":
            return self.get_ip_location()
        if user_input == "quote":
            return self.get_quote()
        if user_input == "joke":
            return self.get_joke()
        if user_input == "fact":
            return self.get_fact()
        if user_input.startswith("define "):
            return self.define_word(user_input.replace("define ", "").strip())
        if user_input.startswith("play "):
            return self.play_youtube(user_input.replace("play ", "").strip())
        if user_input in ["who is aditya", "about aditya", "about me"]:
            return self.about_me()
        if user_input == "":
            return f"{self.welcome_message}"

        corrected = str(TextBlob(user_input).correct())
        return self.get_summary(corrected)

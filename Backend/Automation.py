from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import pyautogui
import time
import os

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "z0Lcw", "gsrt vk_bk FzWSb YwPhnf", "pclqee", "tw-Data-text-small tw-ta",
           "IZ6rdc", "o5uR6d LTKOO", "vlzY6d", "Webanswers-webanswers_table_webanswers_table__webanswers_table__table__cell__text",
           "dDoNo ikbBb gsrt", "sXLaOe", "LWkfke", "VQF4g", "qv3Wpe", "gsrt", "gsrt vk_bk FzWSb YwPhnf", "gsrt vk_bk FzWSb YwPhnf"
           ]
usersagent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
client = Groq(api_key=GroqAPIKey)
professional_response = [
    "Your Satisfaction is my top Priority;feel free to reach out to me anything else I can help you with",
    "I'm at your service for any additional questions or support you may need-don't hestitate to ask",
]
messages = []
SystemChatBot = [{"role": "system", "content": f"Hello,Iam {os.environ['UserName']}, you're content  writer.You  have to write  content like  letters"}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    """
    Writes content (e.g., a sick leave letter) and opens it in Notepad.
    """
    def OpenNotepad(File):
        """
        Opens Notepad with the specified file.
        """
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        """
        Generates content using the AI model.
        """
        messages.append({"role": "user", "content": f"{prompt}"})
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    # Generate the content using AI
    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    # Save the content to a file
    file_path = rf"Data\{Topic.lower().replace(' ', '')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    # Open Notepad and type the content
    OpenNotepad(file_path)
    time.sleep(2)  # Wait for Notepad to open
    pyautogui.write(ContentByAI, interval=0.1)  # Type the content into Notepad

    return True

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {'User-Agent': usersagent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to fetch search results")
            return None

        html = search_google(app)
        if html:
            link = extract_links(html)[0]
            webopen(link)
        return True

def CloseApp(app):
    if "chrome" in app.lower():
        return False
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open"):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open"))
                funcs.append(fun)
        elif command.startswith("general"):
            pass
        elif command.startswith("realtime"):
            pass
        elif command.startswith("close"):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close"))
            funcs.append(fun)
        elif command.startswith("play"):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play"))
            funcs.append(fun)
        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)
        elif command.startswith("google search"):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search"))
            funcs.append(fun)
        elif command.startswith("System"):
            fun = asyncio.to_thread(System, command.removeprefix("System"))
            funcs.append(fun)
        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search"))
            funcs.append(fun)
        else:
            print(f"No Function Found for {command}")
    results = await asyncio.gather(*funcs)
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True
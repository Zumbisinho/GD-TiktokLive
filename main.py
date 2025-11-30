import requests
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
import TikTokLive
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
from time import sleep
from interface import set_remove_level_callback
from pygame import mixer
import os
from tkinter import messagebox
from utils.debug import DebugPrint

mixer.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Audios = {
    "Loading": mixer.Sound(os.path.join(BASE_DIR, "static", "crystal01.ogg")),
    "Success": mixer.Sound(os.path.join(BASE_DIR, "static", "playaudio.ogg")),
    "Error": mixer.Sound(os.path.join(BASE_DIR, "static", "quitSound_01.ogg"))
}
# ------------------ Flask + SocketIO ------------------

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route("/")
def index():
    return render_template("overlay.html")


@app.route("/info")
def info():
    return render_template("info.html")
# ------------------ TikTok Live Client ------------------

@socketio.on("connect")
def on_connect():
    if len(Levels) != 0:
        DebugPrint("Client Connected, syncing levels...")
        for i in range(len(Levels)):
            socketio.emit("AddLevel",Levels[i])


LevelIds = []
Levels = []
class GeometryDashLevel:
    def __init__(self, Req:dict, UserInfo):
        if type(Req) is int:
            DebugPrint('Invalid Requesition (Level not found!)')
        else:
            self.name = Req.get("name", "Desconhecido")
            self.id = Req.get("id", "676767")
            self.author = Req.get("author", "Desconhecido")
            self.difficulty = Req.get("difficulty", "Unknown")
            self.downloads = Req.get("downloads", 0)
            self.likes = Req.get("likes", 0)
            self.length = Req.get("length", "Unknown")
            self.stars = Req.get("stars", 0)
            self.coins = Req.get("coins", 0)
            self.difficultyFace = Req.get("difficultyFace", "")
            self.songName = Req.get("songName", "Unknown")
            self.objectCount = Req.get("objects", "N/A")
            self.UserName = UserInfo[0]
            self.UserAvatarURL = UserInfo[1] 
        

    @property
    def json(self):
        return {
            "name": self.name,
            "id": self.id,
            "author": self.author,
            "difficulty": self.difficulty,
            "downloads": self.downloads,
            "likes": self.likes,
            "length": self.length,
            "stars": self.stars,
            "coins": self.coins,
            "difficultyFace": self.difficultyFace,
            "songName": self.songName,
            "userName" : self.UserName,
            "userAvatarURL": self.UserAvatarURL
        }

# ------------------ Eventos TikTok ------------------

currentList = []



def showTikTokErrorPopup(tipo,username):
    body = ''
    if tipo == "UserNotFoundError":
        body = f"The TikTok user @{username} was not found (typo?) or user can be offline(Restart TikTokServer can fix it)"
    if tipo == "UserOfflineError":
        body = f"The TikTok user @{username} was found offline (Not streaming), try later when the stream starts!"
    messagebox.showerror('TikTok WebSocket Cannot Inicialize',body)

def RemoveLevel(Number:list):
    DebugPrint('Trying to remove ',Number[0], Number[1])
    socketio.emit("RemoveLevel", int(Number[0]))
    LevelIds.remove(str(Number[1]))
    Levels.pop(int(Number[0])-1)
    
def ResetHTML():
    socketio.emit("Reset","reset")
    Levels.clear()
    LevelIds.clear()


    
# ------------------ Threads ------------------

def run_flask(port:int):
    DebugPrint("Starting Flask SocketIO...")
    print("\nFlask Startup message:\n")
    socketio.run(app, host="0.0.0.0", port=port)

def run_tiktok(ttkuser):
    DebugPrint("Starting TikTok Live client...")
    try:
        client = TikTokLiveClient(unique_id=ttkuser)

        @client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            from interface import CreateCard
            comment_text = event.comment
            DebugPrint(f"{event.user.display_id}: {comment_text}")
            TextoManipulavel = str(comment_text).lower()
            
            if TextoManipulavel.startswith('!id ') and len(TextoManipulavel.split(" ")) == 2 and TextoManipulavel.split(" ")[1].isdigit() and TextoManipulavel.split(" ")[1] not in LevelIds:
                socketio.emit("RunningRequest", event.user.display_id)
                Audios['Loading'].play()
                _, LevelId = TextoManipulavel.split()
                Req = requests.get(f'https://gdbrowser.com/api/level/{LevelId}')
                data = Req.json()
                if type(data) is int:
                    socketio.emit("InvalidRequest", event.user.display_id)
                    Audios['Error'].play()
                    DebugPrint('Invalid Requesition (Level not found!)')
                    return 0
                avatar = None
                try:
                    avatar = event.user.avatar_thumb['mUrls'][0]
                except:
                    avatar = getattr(event.user.avatar_thumb, "m_urls", [None])[0]
                Classe = GeometryDashLevel(data,[event.user.display_id,avatar])
                CreateCard(Classe)
                LevelIds.append(Classe.id)
                sleep(2)
                Levels.append(Classe.json)
                socketio.emit("AddLevel", Classe.json)
                Audios['Success'].play()
        client.run()
        messagebox.showinfo(f"Connected to {ttkuser}",f"Successfully connected to {ttkuser}, now listening to user chat!")
    except Exception as e:
        DebugPrint('Fatal Error',e)
        exception_name = type(e).__name__
        showTikTokErrorPopup(exception_name,ttkuser)


# ------------------ Main ------------------

def startTikTok(username:str):
    tiktok_thread = threading.Thread(target=lambda x=username: run_tiktok(x), daemon=True)
    tiktok_thread.start()

def startServer(username:str,port:int):
    
    flask_thread = threading.Thread(target=lambda x=port: run_flask(x), daemon=True)
    
    
    flask_thread.start()
    #startTikTok(username)

    # Tkinter precisa rodar na thread principal
    DebugPrint("Starting control panel...")
    set_remove_level_callback(RemoveLevel)
    for _ in range(10):
        ResetHTML()
        sleep(1)


if __name__ == "__main__":
    startServer('zumbisinho_',5000)
    #startTikTok('zumbisinho_')
    sleep(9999999)
    
   
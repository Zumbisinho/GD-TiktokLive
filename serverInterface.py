import tkinter as tk
from tkinter import font, ttk
from tkinter import filedialog
import os
from PIL import ImageTk,Image
import json
import re
import threading
from interface import open_levels_window
from server import get_link,startCloudFlare
from tkinter import messagebox
from main import startServer,startTikTok

CMDStartUpText = r'''
 ____         _                     ____                       _
|  _ \   ___ | |__   _   _   __ _  |  _ \   __ _  _ __    ___ | |
| | | | / _ \| '_ \ | | | | / _` | | |_) | / _` || '_ \  / _ \| |
| |_| ||  __/| |_) || |_| || (_| | |  __/ | (_| || | | ||  __/| |
|____/  \___||_.__/  \__,_| \__, | |_|     \__,_||_| |_| \___||_|
                            |___/


'''


#------------------------------------
# TODO: Criar arquivo para iniciar dentro do env virtual
#------------------------------------
root = tk.Tk()
root.title("Geometry Dash Level Request Server Setup")
root.geometry("1366x768")
root.configure(bg="#1C2227")
root.iconbitmap("static/GDLR.ico")

CMDCommand = 'cloudflared tunnel --url http://localhost:'
profilePath = os.path.expanduser(r'~\AppData\Roaming\TikTok LIVE Studio\TTStore\services.json')
AceptableScenes = []
startUpSettings = []
startUpFile = None
with open('startupSettings.json','r',encoding='UTF-8') as File:
    content = json.load(File)
    startUpFile = content
    startUpSettings.append(content["username"])
    startUpSettings.append(content['port'])
    startUpSettings.append(content["debug"])

with open(profilePath,'r',encoding='UTF-8') as File:
    class Widgets():
            def __init__(self, uuid, name, url):
                self.uuid = uuid
                self.name = name
                self.url = url
    class SceneInfo:
        def __init__(self, uuid:str, name:str, widgets:list):
            self.uuid = uuid
            self.name = name
            self.widgets = []
            for widget in widgets:
                self.widgets.append(Widgets(widget[0],widget[1],widget[2]))
                
        def getInfo(self):
            toreturn = {
                'uuid': self.uuid,
                'name': self.name,
                'widgets': self.widgets
            }
            return toreturn
                
    content = json.load(File)
    sceneData = content["SourceService"]["state"]["sceneSource"]
    for scene in sceneData.items():
        Valid = False
        Id = scene[0]
        SceneName = ''
        scene = scene[1]
        data = scene['data']
        widgets = []           
        for chunk in data.items():
            
            WGId = chunk[0]
            chunk = chunk[1]
            if chunk['type'] == 'browser':
                Valid = True
                WGname = chunk['name']
                WGUrl = chunk['payload']['url']
                

                widgets.append((WGId,WGname,WGUrl))
            else:
                pass    
        if Valid:
            scenesHead = content["SourceService"]["state"]["scenes"]
            for cena in scenesHead:
                 if cena['id'] == Id:
                      SceneName = cena['name']
            SceneOBJ =SceneInfo(Id,SceneName,widgets)
            AceptableScenes.append(SceneOBJ)
SelectSceneId = ''
def selectScene(scene):
    global SelectSceneId
    SelectSceneId = scene
    render_ui()

class scene_widget():
    def __init__(self, id:int, name:str, number:int):
        self.widget = tk.Frame(scene_list_frame, bg="black", bd=0)
        self.widget.pack(fill="x", pady=10, padx=20,anchor='center')
        tk.Label(self.widget, text=id, fg="#3b3b3b", bg="black", font=("Poppins", 14, "bold")).pack(anchor="w")
        tk.Label(self.widget, text=name, fg="white", bg="black", font=("Poppins", 18, "bold")).pack(anchor="w")
        ttk.Separator(self.widget,orient="horizontal").pack(fill="x", pady=10)
        tk.Label(self.widget, text=f"widgets avaliable: {number}", fg="white", bg="black", font=("Poppins", 12)).pack(anchor="e", pady=8)
        def bind_all_children(widget):
            widget.bind("<Button-1>", lambda event, x=id: selectScene(x))
            for child in widget.winfo_children():
                bind_all_children(child)
        bind_all_children(self.widget)
class widget():
    def __init__(self, uuid, name, url):
        self.widget = tk.Frame(right_frame, bg="#2B343C", bd=0, relief="flat")
        self.widget.pack(fill="x", pady=15, padx=20)
        tk.Label(self.widget, text=uuid, fg="white", bg="#2B343C", font=("Poppins", 14, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        tk.Label(self.widget, text=name, fg="white", bg="#2B343C", font=("Poppins", 20, "bold")).pack(anchor="w", padx=20)
        ttk.Separator(self.widget, orient="horizontal").pack(fill="x", padx=20, pady=10)
        urlsection = tk.Frame(self.widget,bg="#2B343C", bd=0, relief="flat")
        urlsection.pack(fill='x', padx=15,pady=5 ,anchor='center')
        tk.Label(urlsection, text='cloudflare.random.ip/', fg="white", bg="#2B343C", font=("Poppins", 18, "bold")).grid(column=1,row=0)
        e =tk.Entry(urlsection, bg="#262E35", fg="white", relief="flat", width=41, font=("Poppins", 18))
        pattern = re.compile(r'^(?:https?:\/\/)?[^\/]+(?:\/(.*))?$')
        subdomain = pattern.match(url) 
        SubDom = subdomain.group(1) if subdomain and subdomain.group(1) else ""
        e.grid(column=2,row=0)
        if subdomain:
            e.insert(0,SubDom)
        else:
            e.insert(0,'/')
        tk.Button(self.widget, text="Change", bg="#39444E", fg="white",
                      font=("Poppins", 18, "bold"), relief="flat", command=lambda  x=uuid: ChangeURLCommmand(x,e.get())).pack(anchor="w", padx=20)

def ChangeURLCommmand(uuid, pos):
    pattern = re.compile(r'^[A-Za-z0-9._~-]+(?:\/[A-Za-z0-9._~-]+)*\/?$')

    if pattern.match(pos) or not pos:
        pass
    else:
        raise ValueError("Pos-Domain is not valid!")
    link = get_link()
    if link:
        change_url(pos,uuid,SelectSceneId)
    else:
        messagebox.showerror("Server Offline", "You need to start Flask Server to be able to change Dynamic WebWidget Link (A.K.A CloudFlare Tunnel link)")
def change_url(posdomain, id, scene):
    with open(profilePath, 'r',encoding='UTF-8') as File:
        content = json.load(File)

    sceneData = content["SourceService"]["state"]["sceneSource"]
    Widget = sceneData[scene]['data'][id]
    domain = get_link()
    newUrl = domain + '/' + posdomain
    Widget['payload']['url'] = newUrl

    with open(profilePath, 'w',encoding='UTF-8') as File:
        json.dump(content, File, indent=4)



def render_ui():
    
    message.destroy()
    for WG in right_frame.winfo_children():
        WG.destroy()
    for scene in AceptableScenes:
        scene = scene.getInfo()
        if scene['uuid'] == SelectSceneId:
            Data = scene['widgets']
            for wg in Data:
                uuid = wg.uuid
                name = wg.name
                url = wg.url
                widget(uuid,name,url)
    
def changeStartUpSettings(username,port):
    with open('startupSettings.json','w',encoding='UTF-8') as File:
        startUpFile["username"] = username
        startUpFile["port"] = port
        json.dump(startUpFile,File,indent=4)

# =========================
# LAYOUT GERAL
# =========================
# Frame esquerdo

img = Image.open("static/GDLR Banner.png").convert("RGBA")  # mantém alpha
img = img.resize((150, 150), Image.LANCZOS)  # qualidade melhor
img = ImageTk.PhotoImage(img)
left_frame = tk.Frame(root, bg="#111518", width=450)
left_frame.pack(side="left", fill="y")

# Frame direito
right_frame = tk.Frame(root, bg="#1C2227")
right_frame.pack(side="right", fill="both", expand=True)

# Área da imagem (vazia)
image_box = tk.Label(left_frame,image=img,bg="#111518")
image_box.pack(pady=20)

# Inputs
tk.Label(left_frame, text="Username:", bg="#111518", fg="white", font=("Poppins", 14, "bold"),).pack(anchor="w", padx=20)
usr = tk.Entry(left_frame, bg="#1C2227", fg="white", relief="flat", font=("Poppins", 12),width=50)
usr.pack(anchor="w", padx=20)

tk.Label(left_frame, text="Port:", bg="#111518", fg="white", font=("Poppins", 14, "bold")).pack(anchor="w", padx=20)
port = tk.Entry(left_frame, bg="#1C2227", fg="white", relief="flat", font=("Poppins", 12),width=50)
port.pack(anchor="w", padx=20)

def startTikTokCommand():
    try:
        Port = int(port.get())
    except :
        messagebox.showerror("Port Needs to be a Integer",'You cannot input text to a website port')
        return
    User = usr.get()
    if Port and User:
        tiktok = threading.Thread(target= lambda x=User:startTikTok(x),daemon=True)
        tiktok.start()
        tiktok_start.config(text='Running TikTok',state=tk.NORMAL)
    else:
        messagebox.showerror("Missing Arguments","To start a Instance, you need to input a valid TikTokUsername and a Valid Port!")

def startButtonCommand():
    try:
        Port = int(port.get())
    except :
        messagebox.showerror("Port Needs to be a Integer",'You cannot input text to a website port')
        return
    User = usr.get()
    if Port and User:
        Main = threading.Thread(target=lambda Y=User,x=Port: startServer(Y,x), daemon=True)
        CloudFlare = threading.Thread(target=startCloudFlare, daemon=True)
        with open('static/runServer.bat','w') as file:
            file.write(CMDCommand+str(Port))
        
        CloudFlare.start()
        Main.start()
        open_levels_window()
        start_btn.config(text='Running Flask')
        tiktok_start.config(state=tk.NORMAL)
        start_btn.config(state=tk.DISABLED)
        changeStartUpSettings(User,Port)
    else:
        messagebox.showerror("Missing Arguments","To start a Instance, you need to input a valid TikTokUsername and a Valid Port!")
        
        
# Botão Start
Labubu = tk.Label(left_frame, height=5, background="#111518")
Labubu.pack(pady=10, anchor='center')
start_btn = tk.Button(Labubu, text="Flask Start", bg="#5A6872", fg="white",
                      font=("Poppins", 18, "bold"), relief="flat" ,command=startButtonCommand)
start_btn.pack(pady=10, anchor='center')
tiktok_start = tk.Button(Labubu, text="TikTok Start", bg="#5A6872", fg="white",
                      font=("Poppins", 18, "bold"), relief="flat" ,command=startTikTokCommand, state=tk.DISABLED)
tiktok_start.pack(pady=10, anchor='center')




ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=10)

# Cena disponível
tk.Label(left_frame, text="Avaliable Scenes:", bg="#111518", fg="white", font=("Poppins", 18, "bold")).pack(anchor="w", padx=10)

scene_canvas = tk.Canvas(left_frame, bg="black", highlightthickness=0)
scene_scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=scene_canvas.yview)
scene_list_frame = tk.Frame(scene_canvas, bg="black")

    
message = tk.Label(right_frame,
                           text="Select a Scene to edit the\ndynamic overlay link!",
                           fg="white", bg="#1C2227",
                           font=("Poppins", 38, "bold"),
                           justify="center")
message.pack(expand=True)

# Cria a janela do frame dentro do canvas
window_id = scene_canvas.create_window((0, 0), window=scene_list_frame, anchor="nw")

def on_frame_configure(event):
    scene_canvas.configure(scrollregion=scene_canvas.bbox("all"))

def on_canvas_configure(event):
    # Faz o frame ocupar toda a largura do canvas
    scene_canvas.itemconfig(window_id, width=event.width)

scene_list_frame.bind("<Configure>", on_frame_configure)
scene_canvas.bind("<Configure>", on_canvas_configure)

scene_canvas.configure(yscrollcommand=scene_scrollbar.set)
scene_canvas.pack(side="left", fill="both", expand=True, padx=5)
scene_scrollbar.pack(side="right", fill="y")

if startUpSettings[0]:
    usr.insert(0,startUpSettings[0])
if startUpSettings[1]:
    port.insert(0,str(startUpSettings[1]))


for scene in AceptableScenes:
        info = scene.getInfo()
        scene_widget(info['uuid'],info['name'],len(info['widgets']))


print(CMDStartUpText)
print("Dont close this cmd, just minimize it, it just keep the python script running")
if startUpSettings[2]:
    print('\nDebug mode enabled, now the terminal will display info for adicional information about the running')
else:
    print("If you wanna enable DebugMode, change the \"debug\" in <startupSettings.json> to true")    
root.mainloop()

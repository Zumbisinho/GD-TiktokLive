import os
import json
from tkinter import messagebox

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(PROJECT_ROOT, "startupSettings.json")
debugMode = None
with open(FILE_PATH, "r", encoding="utf-8") as f:
    conteudo = json.load(f)
    if conteudo['debug']:
        debugMode = True

def DebugPrint(*args):
    if debugMode:
        print(args)

if __name__ == "__main__":
    messagebox.showerror("Dont open this file","This file is not mean to be open\nExecute the GD Level Requests shortcut to open GD TikTokLive")
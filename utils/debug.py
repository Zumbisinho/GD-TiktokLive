import os
import json

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


import tkinter as tk
from tkinter import font,messagebox
from pyperclip import copy as copytoCB

_remove_level_callback = None
def set_remove_level_callback(func):
    global _remove_level_callback
    _remove_level_callback = func
    

listLen = 0
List = {}

class LevelCard(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#A85C2A", bd=3, relief="flat")
        self.pack(padx=10, pady=10, fill="x")
        self.LevelId = 0

        global listLen
        listLen += 1

        # FONTES
        self.title_font = font.Font(family="Comic Sans MS", size=20, weight="bold")
        self.subtitle_font = font.Font(family="Comic Sans MS", size=14, weight="bold")
        self.small_font = font.Font(family="Comic Sans MS", size=10, weight="bold")

        header = tk.Frame(self, bg="#A85C2A")
        header.pack(anchor="w", pady=(5, 0), padx=10)

        self.rank_label = tk.Label(header, text=f"{listLen}º ", bg="#A85C2A", fg="white", font=self.title_font)
        self.rank_label.pack(side="left")

        self.name_label = tk.Label(header, text="VAI MORRER", bg="#A85C2A", fg="white", font=self.title_font)
        self.name_label.pack(side="left", padx=(15, 0))

        author_frame = tk.Frame(self, bg="#A85C2A")
        author_frame.pack(anchor="w", padx=20)
        self.author_label = tk.Label(author_frame, text="BY ZUMBISINHO", bg="#A85C2A", fg="#FFD700", font=self.subtitle_font)
        self.author_label.pack(side="left")

        info_frame = tk.Frame(self, bg="#A85C2A")
        info_frame.pack(anchor="w", padx=20, pady=(5, 0))
        self.diff_label = tk.Label(info_frame, text="HARDER", bg="#A85C2A", fg="#B0C4DE", font=self.small_font)
        self.diff_label.pack(side="left", padx=(0, 10))
        self.star_label = tk.Label(info_frame, text="⭐ 10", bg="#A85C2A", fg="white", font=self.small_font)
        self.star_label.pack(side="left")

        music_frame = tk.Frame(self, bg="#A85C2A")
        music_frame.pack(anchor="w", padx=20, pady=(5, 0))
        self.music_label = tk.Label(music_frame, text="🎵 VAI MORRER / VALE VALE", bg="#A85C2A", fg="#FFB6C1", font=self.small_font)
        self.music_label.pack(side="left")

        details_frame = tk.Frame(self, bg="#A85C2A")
        details_frame.pack(anchor="w", padx=20, pady=(5, 10))

        self.coins_label = tk.Label(details_frame, text="🪙🪙🪙", bg="#A85C2A", fg="white", font=self.small_font)
        self.coins_label.pack(side="left", padx=(0, 15))

        self.length_label = tk.Label(details_frame, text="⏰ LONG", bg="#A85C2A", fg="white", font=self.small_font)
        self.length_label.pack(side="left", padx=(0, 10))

        self.objects = tk.Label(details_frame, text="🧊 45 OBJECTS", bg="#A85C2A", fg="white", font=self.small_font)
        self.objects.pack(side="left", padx=(0, 10))

        self.downloads_label = tk.Label(details_frame, text="🡳 445", bg="#A85C2A", fg="#7CFC00", font=self.small_font)
        self.downloads_label.pack(side="left", padx=(0, 10))

        self.likes_label = tk.Label(details_frame, text="👍 45", bg="#A85C2A", fg="yellow", font=self.small_font)
        self.likes_label.pack(side="left")

        self.req_label = tk.Label(self, text="REQUESTED BY ZUMBISINHO 🙂", bg="#A85C2A", fg="white", font=self.small_font)
        self.req_label.pack(anchor="e", padx=20, pady=(0, 5))

        self.id_label = tk.Label(self, text="123234402", bg="#A85C2A", fg="#FFD700", font=self.small_font)
        self.id_label.pack(anchor="e", padx=20, pady=(0, 5))

        self.copy = tk.Button(self, text="Copy ID", bg="#A85C2A", fg="#FFD700", font=self.small_font,
                              command=lambda: copytoCB(str(self.LevelId)))
        self.copy.pack(anchor='se', padx=20, pady=(0, 10))

        def Delete():
            global listLen
            listLen -= 1
            lista = list(List.keys())
            IndexDoLevel = lista.index(str(self.LevelId)) + 1

            if _remove_level_callback:
                _remove_level_callback([IndexDoLevel, self.LevelId])

            List.pop(str(self.LevelId))
            for index, Level in enumerate(List.values()):
                Level.rank_label.config(text=f'{index + 1}º')

            self.destroy()

        self.delete = tk.Button(self, text="Delete", bg="#A85C2A", fg="#FFD700", font=self.small_font, command=Delete)
        self.delete.pack(anchor='se', padx=20, pady=(0, 10))

    def set_info(self, **kwargs):
        if "nome" in kwargs:
            self.name_label.config(text=kwargs["nome"].upper())
        if "autor" in kwargs:
            self.author_label.config(text=f"BY {kwargs['autor'].upper()}")
        if "dificuldade" in kwargs:
            self.diff_label.config(text=kwargs["dificuldade"].upper())
        if "estrelas" in kwargs:
            self.star_label.config(text=f"⭐ {kwargs['estrelas']}")
        if "musica" in kwargs:
            self.music_label.config(text=f"🎵 {kwargs['musica']}")
        if "coins" in kwargs:
            self.coins_label.config(text="🪙" * kwargs["coins"])
        if "length" in kwargs:
            self.length_label.config(text=f"⏰ {kwargs['length'].upper()}")
        if "downloads" in kwargs:
            self.downloads_label.config(text=f"🡳 {kwargs['downloads']}")
        if "likes" in kwargs:
            self.likes_label.config(text=f"👍 {kwargs['likes']}")
        if "requested" in kwargs:
            self.req_label.config(text=f"REQUESTED BY {kwargs['requested'].upper()}")
        if "id" in kwargs:
            self.id_label.config(text=str(kwargs["id"]))
            self.LevelId = kwargs["id"]
        if "objects" in kwargs:
            self.objects.config(text=f"🧊{kwargs['objects']} OBJ")

# AQUI É O IMPORTANTE:
def open_levels_window():
    global root
    root = tk.Toplevel()
    root.title("GDLive Request Mod Panel")
    root.configure(bg="#3E1E07")
    root.geometry("1200x500")
    root.iconbitmap("static/GDLR.ico")

    main_frame = tk.Frame(root, bg="#3E1E07")
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg="#3E1E07", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(canvas, bg="#3E1E07")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    root.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    global CreateCard
    def CreateCard(data):
        Level = LevelCard(scrollable_frame)
        Level.set_info(
            nome=data.name,
            autor=data.author,
            dificuldade=data.difficulty,
            estrelas=int(data.stars),
            musica=data.songName,
            coins=int(data.coins),
            length=data.length,
            downloads=int(data.downloads),
            likes=int(data.likes),
            requested=data.UserName,
            id=int(data.id),
            objects=data.objectCount
        )
        List[str(data.id)] = Level

    return CreateCard

CreateCard = None

if __name__ == "__main__":
    messagebox.showerror("Dont open this file","This file is not mean to be open\nExecute the GD Level Requests shortcut to open GD TikTokLive")
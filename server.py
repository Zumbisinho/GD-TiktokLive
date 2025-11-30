import subprocess
import threading
import queue
import time
import asyncio
from typing import Callable, Optional
import re
import os
from tkinter import messagebox



class BatController:
    def __init__(self, bat_path: str, on_stdout: Optional[Callable[[str], None]]=None,
                 on_stderr: Optional[Callable[[str], None]]=None):
        """
        bat_path: caminho completo para o .bat
        on_stdout/on_stderr: callbacks que recebem cada linha produzida pelo processo
        """
        self.bat_path = bat_path
        self.on_stdout = on_stdout
        self.on_stderr = on_stderr

        self.proc: Optional[subprocess.Popen] = None
        self._stdout_thread: Optional[threading.Thread] = None
        self._stderr_thread: Optional[threading.Thread] = None
        self._watcher_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._stdout_queue = queue.Queue()

    def start(self):
        if self.proc is not None:
            raise RuntimeError("Processo já iniciado")
        # Em Windows, execute via cmd /c para rodar .bat corretamente.
        # text=True (Python 3.7+) converte bytes -> str automaticamente.
        self.proc = subprocess.Popen(
            ["cmd.exe", "/c", self.bat_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,               # trabalhar com strings
            bufsize=1,               # line buffered
            universal_newlines=True
        )

        self._stop_event.clear()
        self._stdout_thread = threading.Thread(target=self._read_stdout_loop, daemon=True)
        self._stderr_thread = threading.Thread(target=self._read_stderr_loop, daemon=True)
        self._watcher_thread = threading.Thread(target=self._wait_for_exit, daemon=True)

        self._stdout_thread.start()
        self._stderr_thread.start()
        self._watcher_thread.start()

    def _read_stdout_loop(self):
        assert self.proc and self.proc.stdout
        for line in self.proc.stdout:
            # remove newline mas preserve se quiser
            if line is None:
                break
            line = line.rstrip('\r\n')
            if self.on_stdout:
                try:
                    self.on_stdout(line)
                except Exception as e:
                    # garantir que callback não mate a thread
                    print("Erro on on_stdout:", e)
        # quando o loop terminar, sinalize
        # print("stdout ended")

    def _read_stderr_loop(self):
        assert self.proc and self.proc.stderr
        for line in self.proc.stderr:
            if line is None:
                break
            line = line.rstrip('\r\n')
            if self.on_stderr:
                try:
                    self.on_stderr(line)
                except Exception as e:
                    print("Erro on on_stderr:", e)

    def _wait_for_exit(self):
        assert self.proc
        self.proc.wait()
        self._stop_event.set()

    def send_input(self, text: str):
        """Envia texto para stdin do processo (não esquecer newline se necessário)."""
        if not self.proc or self.proc.stdin is None:
            raise RuntimeError("Processo não iniciado ou stdin não disponível")
        try:
            self.proc.stdin.write(text)
            self.proc.stdin.flush()
        except BrokenPipeError:
            raise RuntimeError("O processo fechou stdin (pipe quebrado)")

    def is_running(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def stop(self, force: bool = False):
        """Tenta terminar graciosamente; com force=True mata o processo."""
        if not self.proc:
            return
        if force:
            try:
                self.proc.kill()
            except Exception:
                pass
        else:
            try:
                # envia Ctrl+C ao processo se suportado - somente exemplo; em Windows requer PROCESS_GROUP
                self.proc.terminate()
            except Exception:
                pass

        # esperar um pouco para liberar recursos
        self._stop_event.wait(timeout=3)
        # fechar pipes
        if self.proc.stdin:
            try:
                self.proc.stdin.close()
            except Exception:
                pass
        if self.proc.stdout:
            try:
                self.proc.stdout.close()
            except Exception:
                pass
        if self.proc.stderr:
            try:
                self.proc.stderr.close()
            except Exception:
                pass
        self.proc = None

def on_stdout(line):
    pass

link = ''
def get_link():
    if link:
        return link
    else:
        return False
def on_stderr(line):
    global link
    line = str(line)
    m = re.search(r"(https?://\S+?)(?=\s*\|)", line)
    
    if m:
        link = m.group(1)
        print("CloudFlare link generated!:",link)


bat_path = os.path.join(os.getcwd(), "static", "runServer.bat")
def startCloudFlare():
    ctl = BatController(bat_path, on_stdout=on_stdout, on_stderr=on_stderr)
    ctl.start()
    time.sleep(1)

    # Criar loop novo para essa thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Iniciar o loop async dessa thread
    loop.run_forever()

if __name__ == "__main__":
    messagebox.showerror("Dont open this file","This file is not mean to be open\nExecute the GD Level Requests shortcut to open GD TikTokLive")
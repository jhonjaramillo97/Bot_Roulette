"""
Orquestador principal de la GUI de Roulette Sniper Pro.
Maneja transiciones entre pantallas, servicios de fondo y limpieza.
"""
import os
import sys
import time
import queue
import threading
import subprocess
import platform
import customtkinter as ctk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.diagnostics import attach_gui_queue, get_logger
from backend.notifier.tunnel import run_tunnel, TUNNEL_FILE
from backend.desktop.screens import (
    PrerequisitesScreen, LoginScreen, LoadingScreen, DashboardScreen, UpdateScreen
)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

log = get_logger("gui")


def _resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class RouletteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Roulette Sniper Pro")
        self.geometry("800x750")
        self.minsize(800, 750)

        icon_path = _resource_path("icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

        if platform.system() == "Windows":
            try:
                import ctypes
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
                value = ctypes.c_int(2)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), 4)
            except Exception:
                pass

        self.log_queue = queue.Queue()
        self.bot_thread = None
        self.cf_proc = None
        self.stop_event = threading.Event()
        self.dashboard_proc = None
        self.public_url = "Generando..."

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.frames = {}
        for F in (PrerequisitesScreen, LoginScreen, LoadingScreen, DashboardScreen, UpdateScreen):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        attach_gui_queue(self.log_queue)
        self.after(100, self._process_log_queue)
        self.show_frame(PrerequisitesScreen)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def _process_log_queue(self):
        while not self.log_queue.empty():
            try:
                msg_type, level, msg = self.log_queue.get_nowait()
                if msg_type == "log":
                    self.frames[DashboardScreen].append_log(level, msg)
            except queue.Empty:
                break
        self.after(100, self._process_log_queue)

    def start_background_services(self):
        try:
            creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            if getattr(sys, 'frozen', False):
                cmd = [sys.executable, "--run-dashboard"]
            else:
                gui_app_path = os.path.join(os.path.dirname(__file__), "..", "app.py")
                cmd = [sys.executable, os.path.abspath(gui_app_path), "--run-dashboard"]
            self.dashboard_proc = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=creationflags
            )
        except Exception:
            pass

        self.cf_watchdog_thread = threading.Thread(target=self._cloudflared_watchdog, daemon=True)
        self.cf_watchdog_thread.start()

    def _cloudflared_watchdog(self):
        def _on_url(url):
            if url == "__error:no_instalado__":
                log.error("cloudflared no esta instalado")
                self.frames[DashboardScreen].update_cf_url("ERROR: No instalado")
                return

            old_url = self.public_url
            self.public_url = url
            self.frames[DashboardScreen].update_cf_url(url)

            if url != old_url:
                from backend.notifier.tunnel import notify_tunnel_url
                notify_tunnel_url(url, old_url)

        run_tunnel(on_url=_on_url, stop_event=self.stop_event)

    def on_closing(self):
        self.stop_event.set()
        if self.dashboard_proc:
            try:
                self.dashboard_proc.terminate()
            except Exception:
                pass
        if self.cf_proc:
            try:
                self.cf_proc.terminate()
            except Exception:
                pass
        self.destroy()

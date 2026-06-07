import os
import threading
import webbrowser
import customtkinter as ctk

from bot_ruleta.debug_logger import get_logger
from bot_ruleta.scanner import run_bot

log = get_logger("gui")


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=10)

        self.lbl_status = ctk.CTkLabel(top_frame, text="● INICIANDO...", font=ctk.CTkFont(size=18, weight="bold"),
                                       text_color="#FFCC00")
        self.lbl_status.pack(side="left", padx=10)

        btn_stop = ctk.CTkButton(top_frame, text="⏹ DETENER", width=120, height=40, fg_color="#FF4444",
                                 hover_color="#CC0000", corner_radius=20, font=ctk.CTkFont(size=13, weight="bold"),
                                 command=self.stop_bot)
        btn_stop.pack(side="right", padx=10)

        cf_frame = ctk.CTkFrame(self, corner_radius=15)
        cf_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(cf_frame, text="Link Web:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10)
        self.ent_cf_url = ctk.CTkEntry(cf_frame, width=300, state="normal")
        self.ent_cf_url.insert(0, "Generando link...")
        self.ent_cf_url.configure(state="readonly")
        self.ent_cf_url.pack(side="left", padx=10, pady=10)

        btn_copy = ctk.CTkButton(cf_frame, text="📋 Copiar", width=80, command=self.copy_url)
        btn_copy.pack(side="left", padx=5, pady=10)

        self.btn_open = ctk.CTkButton(cf_frame, text="🌐 Abrir", width=80, fg_color="#3B82F6", hover_color="#2563EB",
                                      command=self.open_url)

        self.btn_toggle_logs = ctk.CTkButton(self, text="▼ Ver Logs", width=120, fg_color="transparent", border_width=1,
                                             text_color="gray", command=self.toggle_logs)
        self.btn_toggle_logs.pack(pady=(10, 0))

        self.log_frame = ctk.CTkFrame(self)

        ctk.CTkLabel(self.log_frame, text="Logs del Sistema", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10,
                                                                                                    pady=5)

        self.textbox = ctk.CTkTextbox(self.log_frame, wrap="word", font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.textbox.tag_config("INFO", foreground="#FFFFFF")
        self.textbox.tag_config("DEBUG", foreground="#AAAAAA")
        self.textbox.tag_config("WARNING", foreground="#FFCC00")
        self.textbox.tag_config("ERROR", foreground="#FF4444")
        self.textbox.tag_config("CRITICAL", foreground="#FF0000", background="#FFCCCC")

        self.logs_visible = False

    def toggle_logs(self):
        if self.logs_visible:
            self.log_frame.pack_forget()
            self.btn_toggle_logs.configure(text="▼ Ver Logs")
            self.logs_visible = False
        else:
            self.log_frame.pack(fill="both", expand=True, padx=20, pady=10)
            self.btn_toggle_logs.configure(text="▲ Ocultar Logs")
            self.logs_visible = True

    def update_cf_url(self, url):
        self.ent_cf_url.configure(state="normal")
        self.ent_cf_url.delete(0, "end")
        self.ent_cf_url.insert(0, url)
        self.ent_cf_url.configure(state="readonly")

        self.btn_open.pack_forget()
        if url.startswith("http"):
            self.after(10000, self._show_open_button)

    def _show_open_button(self):
        self.btn_open.pack(side="left", padx=5, pady=10)

    def copy_url(self):
        url = self.ent_cf_url.get()
        if url and "http" in url:
            self.clipboard_clear()
            self.clipboard_append(url)

    def open_url(self):
        url = self.ent_cf_url.get()
        if url and "http" in url:
            browsers_to_try = [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            ]

            opened = False
            for browser_path in browsers_to_try:
                if os.path.exists(browser_path):
                    try:
                        webbrowser.register('alt_browser', None, webbrowser.BackgroundBrowser(browser_path))
                        webbrowser.get('alt_browser').open(url)
                        opened = True
                        break
                    except Exception:
                        pass

            if not opened:
                webbrowser.open(url)

    def append_log(self, level, msg):
        self.textbox.insert("end", msg + "\n", level)
        self.textbox.see("end")

        if "REINICIANDO BOT" in msg:
            self.lbl_status.configure(text="● REINICIANDO...", text_color="#FFCC00")
        elif "Comienza escaneo continuo" in msg:
            self.lbl_status.configure(text="● BOT ACTIVO", text_color="#00FF88")

    def start_services(self):
        self.controller.start_background_services()
        self.controller.stop_event.clear()
        self.controller.bot_thread = threading.Thread(
            target=run_bot, args=(self.controller.stop_event,), daemon=True
        )
        self.controller.bot_thread.start()

    def stop_bot(self):
        self.lbl_status.configure(text="● DETENIENDO...", text_color="#FF4444")
        self.controller.stop_event.set()
        log.info("Señal de detencion enviada. El bot se detendra en breve.")

import os
import threading
import subprocess
import webbrowser
import platform
import urllib.request
import urllib.error
import customtkinter as ctk
import tkinter.messagebox as messagebox

from backend.updater import check_for_updates


class PrerequisitesScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl_title = ctk.CTkLabel(self, text="Verificacion del Sistema", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.pack(pady=(40, 20))

        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.pack(pady=20, padx=50, fill="x")

        self.lbl_chrome = ctk.CTkLabel(self.status_frame, text="⏳ Comprobando Chrome...", font=ctk.CTkFont(size=16))
        self.lbl_chrome.pack(pady=10, anchor="w")

        self.lbl_cf = ctk.CTkLabel(self.status_frame, text="⏳ Comprobando Cloudflared...", font=ctk.CTkFont(size=16))
        self.lbl_cf.pack(pady=10, anchor="w")

        self.lbl_net = ctk.CTkLabel(self.status_frame, text="⏳ Comprobando Internet...", font=ctk.CTkFont(size=16))
        self.lbl_net.pack(pady=10, anchor="w")

        from backend.desktop.screens.login import LoginScreen
        from backend.desktop.screens.update import UpdateScreen

        self.btn_continue = ctk.CTkButton(self, text="Continuar", state="disabled", width=220, height=45,
                                          corner_radius=25, font=ctk.CTkFont(size=14, weight="bold"),
                                          command=lambda: controller.show_frame(LoginScreen))
        self.btn_continue.pack(pady=40)

        self.btn_download_cf = ctk.CTkButton(self, text="Descargar Cloudflared", width=220, height=45,
                                             corner_radius=25, font=ctk.CTkFont(size=14, weight="bold"),
                                             fg_color="#ff9900", hover_color="#cc7a00",
                                             command=lambda: webbrowser.open(
                                                 "https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"))

    def on_show(self):
        threading.Thread(target=self.run_checks, daemon=True).start()

    def run_checks(self):
        all_ok = True

        chrome_ok = False
        try:
            if platform.system() == "Windows":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                version, _ = winreg.QueryValueEx(key, "version")
                self.lbl_chrome.configure(text=f"✅ Chrome instalado (v{version})", text_color="#00FF88")
                chrome_ok = True
            else:
                self.lbl_chrome.configure(text="✅ Sistema no-Windows (Asumiendo Chrome OK)", text_color="#00FF88")
                chrome_ok = True
        except Exception:
            self.lbl_chrome.configure(text="❌ Chrome NO encontrado", text_color="#FF4444")
            all_ok = False

        try:
            subprocess.run(["cloudflared", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
            self.lbl_cf.configure(text="Cloudflared instalado", text_color="#00FF88")
        except Exception:
            self.lbl_cf.configure(text="Cloudflared NO encontrado (solo acceso remoto)", text_color="#FFAA00")
            self.btn_download_cf.pack(pady=10, before=self.btn_continue)

        try:
            try:
                urllib.request.urlopen("https://stake.com.co", timeout=5)
                self.lbl_net.configure(text="✅ Conexion a Internet OK", text_color="#00FF88")
            except urllib.error.HTTPError as e:
                if e.code in (403, 401, 503):
                    self.lbl_net.configure(text="✅ Conexion a Internet OK (Protegido)", text_color="#00FF88")
                else:
                    raise e
        except Exception:
            try:
                urllib.request.urlopen("https://google.com", timeout=5)
                self.lbl_net.configure(text="✅ Conexion a Internet OK (Google)", text_color="#00FF88")
            except Exception:
                self.lbl_net.configure(text="❌ Sin conexion a Internet", text_color="#FF4444")
                all_ok = False

        from backend.desktop.screens.login import LoginScreen
        from backend.desktop.screens.update import UpdateScreen

        def on_update_checked(new_version):
            if new_version:
                res = messagebox.askyesno("Actualizacion Disponible",
                                          f"¡Hay una nueva version disponible (v{new_version})!\n\n¿Deseas descargarla e instalarla ahora?")
                if res:
                    self.controller.show_frame(UpdateScreen)
                    self.controller.frames[UpdateScreen].start_update(new_version)
                    return
            if all_ok:
                self.btn_continue.configure(state="normal")
                self.after(2000, lambda: self.controller.show_frame(LoginScreen))

        check_for_updates(lambda v: self.after(0, on_update_checked, v))

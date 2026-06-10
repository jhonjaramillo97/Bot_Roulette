import os
import customtkinter as ctk
from PIL import Image

from backend.diagnostics import get_logger
from backend.auth.gui_credentials import save_credentials, load_saved_credentials, delete_saved_credentials
from backend.auth.credentials import set_runtime_config
from backend.diagnostics import set_diagnostics

log = get_logger("gui")


def _resource_path(relative_path):
    try:
        import sys
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.form_container = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=0)
        self.form_container.grid(row=0, column=0, sticky="nsew")

        self.form = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.form.place(relx=0.5, rely=0.5, anchor="center")

        try:
            logo_path = _resource_path(os.path.join("dashboard", "static", "logo.png"))
            img = Image.open(logo_path)
            self.logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(70, 70))
            lbl_logo = ctk.CTkLabel(self.form, image=self.logo_image, text="")
            lbl_logo.pack(anchor="center", pady=(0, 8))
        except Exception as e:
            log.debug(f"Error loading logo: {e}")

        lbl_title = ctk.CTkLabel(self.form, text="Welcome Back!", font=ctk.CTkFont(size=26, weight="bold"),
                                 text_color="#00C853")
        lbl_title.pack(anchor="center", pady=(0, 2))

        lbl_subtitle = ctk.CTkLabel(self.form, text="Sign in to your bot instance", font=ctk.CTkFont(size=12),
                                    text_color="gray")
        lbl_subtitle.pack(anchor="center", pady=(0, 10))

        lbl_email = ctk.CTkLabel(self.form, text="Email de Stake:", font=ctk.CTkFont(size=12, weight="bold"),
                                 text_color="#00C853")
        lbl_email.pack(anchor="w", pady=(0, 2))
        self.ent_email = ctk.CTkEntry(self.form, placeholder_text="ejemplo@correo.com", width=320, height=38,
                                       corner_radius=8, border_width=1)
        self.ent_email.pack(anchor="w", pady=(0, 8))

        lbl_pass = ctk.CTkLabel(self.form, text="Contraseña:", font=ctk.CTkFont(size=12, weight="bold"),
                                text_color="#00C853")
        lbl_pass.pack(anchor="w", pady=(0, 2))
        self.ent_pass = ctk.CTkEntry(self.form, placeholder_text="••••••••", width=320, height=38, corner_radius=8,
                                      border_width=1, show="*")
        self.ent_pass.pack(anchor="w", pady=(0, 8))

        lbl_tg = ctk.CTkLabel(self.form, text="Telegram (Token / ID):", font=ctk.CTkFont(size=11, weight="bold"),
                              text_color="gray")
        lbl_tg.pack(anchor="w", pady=(0, 2))

        tg_frame = ctk.CTkFrame(self.form, fg_color="transparent")
        tg_frame.pack(anchor="w", pady=(0, 8))
        self.ent_token = ctk.CTkEntry(tg_frame, placeholder_text="Token", width=155, height=32, corner_radius=8,
                                       border_width=1)
        self.ent_token.pack(side="left", padx=(0, 10))
        self.ent_chat_id = ctk.CTkEntry(tg_frame, placeholder_text="Chat ID", width=155, height=32, corner_radius=8,
                                         border_width=1)
        self.ent_chat_id.pack(side="left")

        chk_frame = ctk.CTkFrame(self.form, fg_color="transparent")
        chk_frame.pack(anchor="w", pady=(0, 8), fill="x")

        self.chk_headless = ctk.CTkSwitch(chk_frame, text="Oculto", width=90, progress_color="#00C853",
                                          button_color="#FFFFFF", font=ctk.CTkFont(size=11))
        self.chk_headless.select()
        self.chk_headless.pack(side="left")

        self.chk_diagnostics = ctk.CTkSwitch(chk_frame, text="Logs", width=80, progress_color="#00C853",
                                             button_color="#FFFFFF", font=ctk.CTkFont(size=11))
        self.chk_diagnostics.deselect()
        self.chk_diagnostics.pack(side="left", padx=8)

        self.chk_remember = ctk.CTkSwitch(chk_frame, text="Recordar", width=100, progress_color="#00C853",
                                          button_color="#FFFFFF", font=ctk.CTkFont(size=11))
        self.chk_remember.select()
        self.chk_remember.pack(side="right")

        sliders_frame = ctk.CTkFrame(self.form, fg_color="transparent")
        sliders_frame.pack(anchor="center", pady=(0, 10), fill="x")

        self.lbl_threshold = ctk.CTkLabel(sliders_frame, text="Tercios: 12", font=ctk.CTkFont(size=10), text_color="gray")
        self.lbl_threshold.pack(anchor="center", pady=(0, 0))
        self.slider_thresh = ctk.CTkSlider(sliders_frame, from_=5, to=25, number_of_steps=20, width=320,
                                           command=self._update_thresh_lbl, progress_color="#00C853",
                                           button_color="#00C853", height=12)
        self.slider_thresh.set(12)
        self.slider_thresh.pack(anchor="center", pady=(0, 4))

        self.lbl_color_thresh = ctk.CTkLabel(sliders_frame, text="Color: 5", font=ctk.CTkFont(size=10), text_color="gray")
        self.lbl_color_thresh.pack(anchor="center", pady=(0, 0))
        self.slider_color_thresh = ctk.CTkSlider(sliders_frame, from_=3, to=15, number_of_steps=12, width=320,
                                                  command=self._update_color_thresh_lbl, progress_color="#FF6B6B",
                                                  button_color="#FF6B6B", height=12)
        self.slider_color_thresh.set(5)
        self.slider_color_thresh.pack(anchor="center", pady=(0, 4))

        self.lbl_number_thresh = ctk.CTkLabel(sliders_frame, text="Numeros: 20", font=ctk.CTkFont(size=10),
                                              text_color="gray")
        self.lbl_number_thresh.pack(anchor="center", pady=(0, 0))
        self.slider_number_thresh = ctk.CTkSlider(sliders_frame, from_=20, to=150, number_of_steps=130, width=320,
                                                   command=self._update_number_thresh_lbl, progress_color="#3B82F6",
                                                   button_color="#3B82F6", height=12)
        self.slider_number_thresh.set(50)
        self.slider_number_thresh.pack(anchor="center", pady=(0, 6))

        self.btn_start = ctk.CTkButton(self.form, text="INICIAR BOT", width=320, height=42,
                                       font=ctk.CTkFont(size=14, weight="bold"), corner_radius=25,
                                       fg_color="#00C853", hover_color="#00E676", text_color="black",
                                       command=self.start_bot)
        self.btn_start.pack(anchor="center", pady=(0, 0))

    def on_show(self):
        creds = load_saved_credentials()
        if creds:
            self.ent_email.insert(0, creds.get("email", ""))
            self.ent_pass.insert(0, creds.get("password", ""))
            self.ent_token.insert(0, creds.get("tg_token", ""))
            self.ent_chat_id.insert(0, creds.get("tg_chat_id", ""))

            thresh = creds.get("threshold", 12)
            self.slider_thresh.set(thresh)
            self._update_thresh_lbl(thresh)

            color_thresh = creds.get("color_streak_threshold", 5)
            self.slider_color_thresh.set(color_thresh)
            self._update_color_thresh_lbl(color_thresh)

            number_thresh = creds.get("number_delay_threshold", 20)
            self.slider_number_thresh.set(number_thresh)
            self._update_number_thresh_lbl(number_thresh)

            if not creds.get("headless", True):
                self.chk_headless.deselect()

            if creds.get("diagnostics", False):
                self.chk_diagnostics.select()

    def _update_thresh_lbl(self, val):
        self.lbl_threshold.configure(text=f"Tercios: {int(val)}")

    def _update_color_thresh_lbl(self, val):
        self.lbl_color_thresh.configure(text=f"Color: {int(val)}")

    def _update_number_thresh_lbl(self, val):
        self.lbl_number_thresh.configure(text=f"Numeros: {int(val)}")

    def start_bot(self):
        email = self.ent_email.get().strip()
        password = self.ent_pass.get().strip()
        tg_token = self.ent_token.get().strip()
        tg_chat_id = self.ent_chat_id.get().strip()
        threshold = int(self.slider_thresh.get())
        color_streak_threshold = int(self.slider_color_thresh.get())
        number_delay_threshold = int(self.slider_number_thresh.get())
        headless = bool(self.chk_headless.get())
        diagnostics = bool(self.chk_diagnostics.get())

        if not email or not password:
            log.error("Por favor ingresa correo y contraseña.")
            return

        if self.chk_remember.get():
            save_credentials(email, password, tg_token, tg_chat_id, threshold, headless, diagnostics,
                             color_streak_threshold, number_delay_threshold)
        else:
            delete_saved_credentials()

        set_runtime_config(
            email=email, password=password, tg_token=tg_token, tg_chat_id=tg_chat_id,
            threshold=threshold, headless=headless,
            color_streak_threshold=color_streak_threshold,
            number_delay_threshold=number_delay_threshold
        )

        set_diagnostics(diagnostics)

        from backend.desktop.screens.loading import LoadingScreen
        self.controller.show_frame(LoadingScreen)
        self.controller.frames[LoadingScreen].start_loading()

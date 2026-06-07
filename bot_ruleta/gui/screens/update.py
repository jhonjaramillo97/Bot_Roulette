import customtkinter as ctk

from bot_ruleta.updater import perform_update


class UpdateScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0)

        self.lbl_title = ctk.CTkLabel(container, text="Descargando Actualizacion...",
                                      font=ctk.CTkFont(size=24, weight="bold"), text_color="#00C853")
        self.lbl_title.pack(pady=(0, 20))

        self.progressbar = ctk.CTkProgressBar(container, width=350, progress_color="#00C853")
        self.progressbar.set(0)
        self.progressbar.pack()

        self.lbl_percent = ctk.CTkLabel(container, text="0%", font=ctk.CTkFont(size=14))
        self.lbl_percent.pack(pady=(10, 0))

        self.lbl_status = ctk.CTkLabel(container, text="Conectando con GitHub...", font=ctk.CTkFont(size=12),
                                       text_color="gray")
        self.lbl_status.pack(pady=(5, 0))

    def start_update(self, new_version):
        self.lbl_title.configure(text=f"Descargando v{new_version}...")

        def update_progress(percent):
            self.progressbar.set(percent / 100.0)
            self.lbl_percent.configure(text=f"{percent}%")
            self.lbl_status.configure(text="Descargando ejecutable...")

        def update_complete(success, message):
            if success:
                self.lbl_status.configure(text="Reiniciando...", text_color="#FFCC00")
                self.lbl_title.configure(text="Bot Actualizado", text_color="#00FF88")
            else:
                self.lbl_status.configure(text=f"Error: {message}", text_color="#FF4444")
                self.lbl_title.configure(text="Actualizacion Fallida", text_color="#FF4444")

        perform_update(new_version,
                       lambda p: self.after(0, update_progress, p),
                       lambda s, m: self.after(0, update_complete, s, m))

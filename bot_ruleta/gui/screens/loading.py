import customtkinter as ctk

from bot_ruleta.gui.screens.dashboard import DashboardScreen


class LoadingScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0)

        self.lbl_info = ctk.CTkLabel(container, text="Inicializando sistema y conectando servidor...",
                                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#00C853")
        self.lbl_info.pack(pady=(0, 20))

        self.progressbar = ctk.CTkProgressBar(container, width=300, progress_color="#00C853")
        self.progressbar.set(0)
        self.progressbar.pack()

        self.lbl_percent = ctk.CTkLabel(container, text="0%", font=ctk.CTkFont(size=14))
        self.lbl_percent.pack(pady=(10, 0))

        self.progress = 0
        self.timer_id = None

    def start_loading(self):
        self.progress = 0
        self.progressbar.set(0)
        self.lbl_percent.configure(text="0%")
        self.update_progress()

    def update_progress(self):
        self.progress += 0.02
        if self.progress > 1.0:
            self.progress = 1.0

        self.progressbar.set(self.progress)
        self.lbl_percent.configure(text=f"{int(self.progress * 100)}%")

        if self.progress < 1.0:
            self.timer_id = self.after(200, self.update_progress)
        else:
            self.controller.show_frame(DashboardScreen)
            self.controller.frames[DashboardScreen].start_services()

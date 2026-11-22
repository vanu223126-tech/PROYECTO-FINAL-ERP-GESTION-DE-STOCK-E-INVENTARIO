import customtkinter as ctk

from frontend.config import COLORS


class AppSidebar(ctk.CTkFrame):

    def __init__(self, master, on_navigate):
        super().__init__(
            master,
            width=200,
            corner_radius=0,
            fg_color=COLORS["bg_card"],
        )
        self.on_navigate = on_navigate
        self.buttons = {}

        title_label = ctk.CTkLabel(
            self,
            text="Menú",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["muted_text"],
        )
        title_label.pack(padx=20, pady=(20, 12))

        nav_items = [
            ("Artículos", "articles"),
            ("Clientes", "customers"),
            ("Facturas", "invoices"),
        ]

        for text, key in nav_items:
            btn = ctk.CTkButton(
                self,
                text=text,
                fg_color="transparent",
                text_color="#F8FAFC",
                hover_color=COLORS["cancel_hover"],
                anchor="w",
                corner_radius=8,
                command=lambda k=key: self.on_navigate(k),
            )
            btn.pack(fill="x", padx=12, pady=5)
            self.buttons[key] = btn

    def set_active_button(self, view_name: str):
        for key, btn in self.buttons.items():
            if key == view_name:
                btn.configure(
                    fg_color=COLORS["primary"],
                    hover_color=COLORS["primary_hover"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    hover_color=COLORS["cancel_hover"],
                )
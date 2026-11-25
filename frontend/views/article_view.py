import customtkinter as ctk

from frontend.components.cards import ArticleCard
from frontend.components.forms import ArticleForm
from frontend.config import COLORS
from frontend.services.articles_service import ArticleService


class ArticleView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))

        title_label = ctk.CTkLabel(
            top_bar,
            text="Gestión de Artículos",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.pack(side="left")

        self.status_label = ctk.CTkLabel(
            top_bar,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.status_label.pack(side="right", padx=10)

        refresh_btn = ctk.CTkButton(
            top_bar,
            text="Refrescar",
            width=95,
            fg_color=COLORS["info"],
            hover_color=COLORS["info_hover"],
            corner_radius=8,
            command=self.refresh,
        )
        refresh_btn.pack(side="right")

        left_panel = ctk.CTkFrame(self, fg_color="transparent")
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left_panel.grid_rowconfigure(1, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        search_bar = ctk.CTkFrame(left_panel, fg_color="transparent")
        search_bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.search_entry = ctk.CTkEntry(
            search_bar,
            placeholder_text="Buscar artículo por nombre...",
            fg_color=COLORS["bg_card"],
            border_color=COLORS["cancel"],
            corner_radius=8,
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.search_entry.bind("<KeyRelease>", lambda _e: self.apply_filter())

        clear_search_btn = ctk.CTkButton(
            search_bar,
            text="Limpiar",
            width=80,
            fg_color=COLORS["cancel"],
            hover_color=COLORS["cancel_hover"],
            corner_radius=8,
            command=self.clear_search,
        )
        clear_search_btn.pack(side="right")

        self.scroll_frame = ctk.CTkScrollableFrame(
            left_panel,
            fg_color=COLORS["bg_card"],
            corner_radius=10,
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.form = ArticleForm(self, on_save=self.handle_save)
        self.form.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)

        self._all_articles = []

    def refresh(self):
        self._all_articles = ArticleService.get_all()
        self.apply_filter()

    def clear_search(self):
        self.search_entry.delete(0, "end")
        self.apply_filter()

    def apply_filter(self):
        query = self.search_entry.get().strip()
        if query:
            filtered = ArticleService.search_by_name(query)
        else:
            filtered = self._all_articles
        self._render_cards(filtered)


    def _render_cards(self, articles: list):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not articles:
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="No hay artículos para mostrar.",
                text_color=COLORS["muted_text"],
            )
            empty_label.pack(pady=20)
            return

        for article in articles:
            card = ArticleCard(
                self.scroll_frame,
                article=article,
                on_edit=self.form.load_for_edit,
                on_delete=self.handle_delete,
            )
            card.pack(fill="x", pady=4, padx=2)

    def handle_save(self, payload: dict, editing_id):
        if editing_id is None:
            ok, err = ArticleService.create(payload)
            msg = "Artículo creado correctamente." if ok else (err or "Error al crear artículo.")
        else:
            ok, err = ArticleService.update(editing_id, payload)
            msg = "Artículo actualizado." if ok else (err or "Error al actualizar artículo.")

        self._set_status(msg, success=ok)
        if ok:
            self.refresh()

    def handle_delete(self, article_id):
        if not article_id:
            return
        ok, err = ArticleService.delete(article_id)
        msg = "Artículo eliminado." if ok else (err or "Error al eliminar artículo.")
        self._set_status(msg, success=ok)
        if ok:
            if self.form.current_editing_id == article_id:
                self.form.clear()
            self.refresh()

    def _set_status(self, text: str, success: bool):
        color = COLORS["status_ok"] if success else COLORS["status_err"]
        self.status_label.configure(text=text, text_color=color)
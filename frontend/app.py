import customtkinter as ctk

from frontend.components.sidebar import AppSidebar
from frontend.config import (
    COLOR_THEME,
    MIN_WINDOW_SIZE,
    THEME_MODE,
    WINDOW_SIZE,
    WINDOW_TITLE,
)
from frontend.views.article_view import ArticleView
from frontend.views.branch_view import BranchView
from frontend.views.category_view import CategoryView
from frontend.views.customer_view import CustomerView
from frontend.views.deposit_view import DepositView
from frontend.views.invoice_view import InvoiceView
from frontend.views.stock_movement_view import StockMovementView
from frontend.views.supplier_view import SupplierView

ctk.set_appearance_mode(THEME_MODE)
ctk.set_default_color_theme(COLOR_THEME)


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = AppSidebar(self, on_navigate=self.show_view)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content_area = ctk.CTkFrame(self)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.views = {
            "articles": ArticleView(self.content_area),
            "customers": CustomerView(self.content_area),
            "invoices": InvoiceView(self.content_area),
            "categories": CategoryView(self.content_area),
            "suppliers": SupplierView(self.content_area),
            "branches": BranchView(self.content_area),
            "deposits": DepositView(self.content_area),
            "stock_movements": StockMovementView(self.content_area),
        }

        self.show_view("articles")

    def show_view(self, view_name: str):
        for view in self.views.values():
            view.pack_forget()

        self.sidebar.set_active_button(view_name)

        selected_view = self.views.get(view_name)
        if selected_view:
            selected_view.pack(fill="both", expand=True)
            if hasattr(selected_view, "refresh"):
                selected_view.refresh()
            elif hasattr(selected_view, "load_data"):
                selected_view.load_data()
            elif hasattr(selected_view, "load_customers"):
                selected_view.load_customers()   
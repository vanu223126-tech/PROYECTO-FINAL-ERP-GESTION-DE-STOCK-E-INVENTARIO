import customtkinter as ctk

from frontend.config import COLORS


class ArticleForm(ctk.CTkFrame):

    def __init__(self, master, on_save):
        super().__init__(master)
        self.on_save = on_save
        self.current_editing_id = None

        self.title_label = ctk.CTkLabel(
            self,
            text="Nuevo Artículo",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.title_label.pack(pady=10)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Nombre del Artículo")
        self.name_entry.pack(fill="x", padx=10, pady=5)

        self.description_entry = ctk.CTkEntry(self, placeholder_text="Descripción")
        self.description_entry.pack(fill="x", padx=10, pady=5)

        self.unit_price_entry = ctk.CTkEntry(self, placeholder_text="Precio Unitario")
        self.unit_price_entry.pack(fill="x", padx=10, pady=5)

        self.sale_price_entry = ctk.CTkEntry(self, placeholder_text="Precio de Venta")
        self.sale_price_entry.pack(fill="x", padx=10, pady=5)

        self.stock_entry = ctk.CTkEntry(self, placeholder_text="Stock")
        self.stock_entry.pack(fill="x", padx=10, pady=5)

        self.category_id_entry = ctk.CTkEntry(
            self, placeholder_text="ID Categoría (opcional)"
        )
        self.category_id_entry.pack(fill="x", padx=10, pady=5)

        self.supplier_id_entry = ctk.CTkEntry(
            self, placeholder_text="ID Proveedor (opcional)"
        )
        self.supplier_id_entry.pack(fill="x", padx=10, pady=5)

        self.feedback_label = ctk.CTkLabel(
            self, text="", text_color=COLORS["status_err"]
        )
        self.feedback_label.pack(pady=(2, 0))

        self.save_btn = ctk.CTkButton(
            self,
            text="Guardar",
            fg_color=COLORS["success"],
            hover_color=COLORS["success_hover"],
            command=self.submit,
        )
        self.save_btn.pack(fill="x", padx=10, pady=5)

        self.cancel_btn = ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color=COLORS["cancel"],
            hover_color=COLORS["cancel_hover"],
            command=self.clear,
        )

    def submit(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        if not name:
            self.feedback_label.configure(text="El nombre es obligatorio.")
            return

        try:
            unit_price = float(self.unit_price_entry.get())
            sale_price = float(self.sale_price_entry.get())
            stock = int(self.stock_entry.get())
        except ValueError:
            self.feedback_label.configure(
                text="Precios deben ser numéricos y el stock entero."
            )
            return

        cat_raw = self.category_id_entry.get().strip()
        sup_raw = self.supplier_id_entry.get().strip()

        id_category = None
        id_supplier = None
        if cat_raw:
            try:
                id_category = int(cat_raw)
            except ValueError:
                self.feedback_label.configure(text="ID Categoría debe ser entero.")
                return
        if sup_raw:
            try:
                id_supplier = int(sup_raw)
            except ValueError:
                self.feedback_label.configure(text="ID Proveedor debe ser entero.")
                return

        payload = {
            "name": name,
            "description": description,
            "unit_price": unit_price,
            "sale_price": sale_price,
            "stock": stock,
            "id_Category": id_category,
            "id_Supplier": id_supplier,
        }

        self.feedback_label.configure(text="")
        self.on_save(payload, self.current_editing_id)
        self.clear()

    def load_for_edit(self, article: dict):
        self.current_editing_id = article.get("id")
        self.title_label.configure(text="Editar Artículo")
        self.feedback_label.configure(text="")

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, str(article.get("name", "")))

        self.description_entry.delete(0, "end")
        self.description_entry.insert(0, str(article.get("description", "")))

        self.unit_price_entry.delete(0, "end")
        self.unit_price_entry.insert(0, str(article.get("unit_price", "")))

        self.sale_price_entry.delete(0, "end")
        self.sale_price_entry.insert(0, str(article.get("sale_price", "")))

        self.stock_entry.delete(0, "end")
        self.stock_entry.insert(0, str(article.get("stock", "")))

        self.category_id_entry.delete(0, "end")
        if article.get("id_Category") is not None:
            self.category_id_entry.insert(0, str(article.get("id_Category")))

        self.supplier_id_entry.delete(0, "end")
        if article.get("id_Supplier") is not None:
            self.supplier_id_entry.insert(0, str(article.get("id_Supplier")))

        self.cancel_btn.pack(fill="x", padx=10, pady=5)

    def clear(self):
        self.current_editing_id = None
        self.title_label.configure(text="Nuevo Artículo")
        self.feedback_label.configure(text="")
        for entry in (
            self.name_entry,
            self.description_entry,
            self.unit_price_entry,
            self.sale_price_entry,
            self.stock_entry,
            self.category_id_entry,
            self.supplier_id_entry,
        ):
            entry.delete(0, "end")
        self.cancel_btn.pack_forget()
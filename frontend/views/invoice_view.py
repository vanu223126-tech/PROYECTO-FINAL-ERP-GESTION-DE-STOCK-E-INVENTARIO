from datetime import date
import customtkinter as ctk
from frontend.config import COLORS
from frontend.services.articles_service import ArticleService
from frontend.services.customer_service import CustomerService
from frontend.services.invoices_service import InvoiceService


class InvoiceView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.articles = []
        self.selected_customer = None
        self.cart_items = []

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            header,
            text="Facturación y Ventas",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(header, text="")
        self.status_label.pack(side="right", padx=10)

        ctk.CTkButton(
            header,
            text="Refrescar Catálogo",
            width=125,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self.refresh,
        ).pack(side="right")

        left_col = ctk.CTkFrame(self, fg_color="transparent")
        left_col.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left_col.grid_rowconfigure(2, weight=1)
        left_col.grid_columnconfigure(0, weight=1)

        customer_box = ctk.CTkFrame(left_col, fg_color=COLORS["bg_card"], corner_radius=8)
        customer_box.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkLabel(
            customer_box,
            text="1. Cliente (búsqueda por Email)",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(anchor="w", padx=10, pady=(8, 4))

        cust_row = ctk.CTkFrame(customer_box, fg_color="transparent")
        cust_row.pack(fill="x", padx=10, pady=(0, 4))

        self.cust_email_entry = ctk.CTkEntry(
            cust_row, placeholder_text="Ingrese email del cliente..."
        )
        self.cust_email_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.cust_email_entry.bind("<Return>", lambda _e: self.find_customer())

        ctk.CTkButton(
            cust_row,
            text="Buscar Cliente",
            width=110,
            fg_color=COLORS["info"],
            hover_color=COLORS["info_hover"],
            command=self.find_customer,
        ).pack(side="right")

        self.customer_info_label = ctk.CTkLabel(
            customer_box,
            text="Cliente no seleccionado.",
            text_color=COLORS["muted_text"],
        )
        self.customer_info_label.pack(anchor="w", padx=10, pady=(0, 8))

        art_search_row = ctk.CTkFrame(left_col, fg_color="transparent")
        art_search_row.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        self.article_query_entry = ctk.CTkEntry(
            art_search_row,
            placeholder_text="2. Buscar artículo por nombre (coincidencia parcial)...",
        )
        self.article_query_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.article_query_entry.bind("<KeyRelease>", lambda _e: self.render_articles())

        self.qty_entry = ctk.CTkEntry(art_search_row, width=75, placeholder_text="Cant.")
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="right")

        self.articles_scroll = ctk.CTkScrollableFrame(left_col, fg_color="transparent")
        self.articles_scroll.grid(row=2, column=0, sticky="nsew")

        # Columna derecha: Detalle de factura / Carrito
        right_col = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=8)
        right_col.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_col.grid_rowconfigure(2, weight=1)
        right_col.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            right_col,
            text="Detalle de Factura",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, pady=(12, 6))

        branch_row = ctk.CTkFrame(right_col, fg_color="transparent")
        branch_row.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 6))

        ctk.CTkLabel(branch_row, text="ID Sucursal:").pack(side="left", padx=(0, 6))
        self.branch_id_entry = ctk.CTkEntry(branch_row, width=80)
        self.branch_id_entry.insert(0, "1")
        self.branch_id_entry.pack(side="left")

        self.cart_scroll = ctk.CTkScrollableFrame(right_col, fg_color="transparent")
        self.cart_scroll.grid(row=2, column=0, sticky="nsew", padx=10)

        footer = ctk.CTkFrame(right_col, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        self.total_label = ctk.CTkLabel(
            footer,
            text="Total: $0.00",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.total_label.pack(anchor="w", pady=(0, 6))

        ctk.CTkButton(
            footer,
            text="Emitir Factura",
            fg_color=COLORS["success"],
            hover_color=COLORS["success_hover"],
            command=self.submit_invoice,
        ).pack(fill="x", pady=(0, 4))

        ctk.CTkButton(
            footer,
            text="Vaciar Detalle",
            fg_color=COLORS["cancel"],
            hover_color=COLORS["cancel_hover"],
            command=self.clear_cart,
        ).pack(fill="x")

        self.refresh()

    def refresh(self):
        loaded = ArticleService.get_all()
        self.articles = [a for a in loaded if isinstance(a, dict)] if isinstance(loaded, list) else []
        self.render_articles()
        self.render_cart()

    def find_customer(self):
        email = self.cust_email_entry.get().strip()
        if not email:
            self.selected_customer = None
            self.customer_info_label.configure(
                text="Ingrese un email válido.",
                text_color=COLORS["status_err"],
            )
            return

        customers, err = CustomerService.search_by_email(email)
        if err or not customers:
            self.selected_customer = None
            msg = str(err) if err else "Cliente no encontrado."
            self.customer_info_label.configure(
                text=msg,
                text_color=COLORS["status_err"],
            )
            return

        exactos = [
            c for c in customers
            if isinstance(c, dict) and str(c.get("email", "")).lower() == email.lower()
        ]
        elegido = exactos[0] if len(exactos) == 1 else (customers[0] if len(customers) == 1 else None)

        if elegido is None:
            self.selected_customer = None
            self.customer_info_label.configure(
                text=f"Hay {len(customers)} clientes parecidos. Ingresá el email completo.",
                text_color=COLORS["status_err"],
            )
            return

        self.selected_customer = elegido
        self.customer_info_label.configure(
            text=f"Cliente #{elegido.get('id')}: {elegido.get('name')} ({elegido.get('email')})",
            text_color=COLORS["status_ok"],
        )

    def render_articles(self):
        for w in self.articles_scroll.winfo_children():
            w.destroy()

        needle = self.article_query_entry.get().strip()
        matches = ArticleService.search_by_name(needle) if needle else self.articles


        if not matches:
            empty_msg = (
                "No hay artículos cargados. Pulsa Refrescar Catálogo."
                if not self.articles
                else "No se encontraron artículos con ese nombre."
            )
            ctk.CTkLabel(
                self.articles_scroll,
                text=empty_msg,
                text_color=COLORS["muted_text"],
            ).pack(pady=16)
            return

        for art in matches:
            row = ctk.CTkFrame(self.articles_scroll, fg_color=COLORS["bg_card"], corner_radius=8)
            row.pack(fill="x", pady=3, padx=2)

            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=10, pady=6)

            price = float(art.get("sale_price", art.get("unit_price", 0.0)) or 0.0)
            stock = art.get("stock", 0)

            ctk.CTkLabel(
                info,
                text=f"{art.get('name', '')} (${price:.2f})",
                font=ctk.CTkFont(size=13, weight="bold"),
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=f"ID: {art.get('id')} | Stock disponible: {stock}",
                text_color=COLORS["muted_text"],
            ).pack(anchor="w")

            ctk.CTkButton(
                row,
                text="Agregar",
                width=80,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                command=lambda item=art: self.add_to_cart(item),
            ).pack(side="right", padx=10, pady=6)

    def add_to_cart(self, article: dict):
        try:
            qty = int(self.qty_entry.get().strip())
        except ValueError:
            self._set_status("La cantidad debe ser un número entero.", success=False)
            return

        if qty <= 0:
            self._set_status("La cantidad debe ser mayor a 0.", success=False)
            return

        stock = int(article.get("stock", 0) or 0)
        if qty > stock:
            self._set_status(
                f"Stock insuficiente para {article.get('name')} (disponible: {stock}).",
                success=False,
            )
            return

        unit_price = float(article.get("sale_price", article.get("unit_price", 0.0)) or 0.0)
        art_id = article.get("id")

        for item in self.cart_items:
            if item["id_article"] == art_id:
                new_qty = item["amount"] + qty
                if new_qty > stock:
                    self._set_status(
                        f"Stock máximo superado ({stock} unidades).",
                        success=False,
                    )
                    return
                item["amount"] = new_qty
                self.render_cart()
                return

        self.cart_items.append(
            {
                "id_article": art_id,
                "name": article.get("name", ""),
                "amount": qty,
                "unit_price": unit_price,
            }
        )
        self.render_cart()

    def remove_from_cart(self, index: int):
        if 0 <= index < len(self.cart_items):
            self.cart_items.pop(index)
            self.render_cart()

    def clear_cart(self):
        self.cart_items = []
        self.render_cart()

    def render_cart(self):
        for w in self.cart_scroll.winfo_children():
            w.destroy()

        total = 0.0
        for idx, item in enumerate(self.cart_items):
            subtotal = item["amount"] * item["unit_price"]
            total += subtotal

            line = ctk.CTkFrame(self.cart_scroll, fg_color="#0f172a", corner_radius=6)
            line.pack(fill="x", pady=3)

            ctk.CTkLabel(
                line,
                text=f"{item['name']} x{item['amount']} = ${subtotal:.2f}",
            ).pack(side="left", padx=8, pady=6)

            ctk.CTkButton(
                line,
                text="X",
                width=28,
                fg_color=COLORS["danger"],
                hover_color=COLORS["danger_hover"],
                command=lambda i=idx: self.remove_from_cart(i),
            ).pack(side="right", padx=6, pady=4)

        self.total_label.configure(text=f"Total: ${total:.2f}")

    def submit_invoice(self):
        if not self.selected_customer:
            self._set_status("Primero selecciona un cliente válido.", success=False)
            return

        if not self.cart_items:
            self._set_status("Agrega al menos un artículo a la factura.", success=False)
            return

        try:
            branch_id = int(self.branch_id_entry.get().strip())
        except ValueError:
            self._set_status("El ID de sucursal debe ser entero.", success=False)
            return

        payload = {
            "date": date.today().isoformat(),
            "id_customer": self.selected_customer.get("id"),
            "id_branch": branch_id,
            "items": [
                {
                    "id_article": it["id_article"],
                    "amount": it["amount"],
                    "unit_price": it["unit_price"],
                }
                for it in self.cart_items
            ],
        }

        ok, err = InvoiceService.create_invoice(payload)
        if ok:
            self._set_status("Factura emitida y stock actualizado.", success=True)
            self.clear_cart()
            self.refresh()
        else:
            self._set_status(str(err) if err else "No se pudo emitir la factura.", success=False)

    def _set_status(self, text: str, success: bool):
        color = COLORS["status_ok"] if success else COLORS["status_err"]
        self.status_label.configure(text=text, text_color=color)
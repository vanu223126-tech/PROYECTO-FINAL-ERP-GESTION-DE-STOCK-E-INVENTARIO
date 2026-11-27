import customtkinter as ctk
from frontend.config import COLORS
from frontend.services.customer_service import CustomerService
from datetime import date



class CustomerView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.editing_customer_id = None 
        self.editing_registration_date = None
        self.selected_customer = None

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            header,
            text="Gestión de Clientes",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.status_label.pack(side="right", padx=10)

        ctk.CTkButton(
            header,
            text="Refrescar",
            width=95,
            fg_color=COLORS["info"],
            hover_color=COLORS["info_hover"],
            corner_radius=8,
            command=self.refresh,
        ).pack(side="right")

        
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        search_box = ctk.CTkFrame(left_frame, fg_color=COLORS["bg_card"], corner_radius=10)
        search_box.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkLabel(
            search_box,
            text="Búsqueda por dato unívoco (Email)",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(anchor="w", padx=10, pady=(8, 4))

        search_row = ctk.CTkFrame(search_box, fg_color="transparent")
        search_row.pack(fill="x", padx=10, pady=(0, 8))

        self.email_search_entry = ctk.CTkEntry(
            search_row,
            placeholder_text="Ej: cliente@correo.com",
            border_color=COLORS["cancel"],
            corner_radius=8,
        )
        self.email_search_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.email_search_entry.bind("<Return>", lambda _e: self.search_customer())

        ctk.CTkButton(
            search_row,
            text="Buscar",
            width=80,
            fg_color=COLORS["info"],
            hover_color=COLORS["info_hover"],
            corner_radius=8,
            command=self.search_customer,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            search_row,
            text="Todos",
            width=70,
            fg_color=COLORS["cancel"],
            hover_color=COLORS["cancel_hover"],
            corner_radius=8,
            command=self.refresh,
        ).pack(side="left")

        self.search_result_label = ctk.CTkLabel(
            left_frame,
            text="",
            text_color=COLORS["muted_text"],
            anchor="w",
        )
        self.search_result_label.grid(row=1, column=0, sticky="ew", pady=(0, 4))

        self.list_frame = ctk.CTkScrollableFrame(left_frame, fg_color="transparent")
        self.list_frame.grid(row=2, column=0, sticky="nsew")

        
        form_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=10)
        form_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)

        self.form_title = ctk.CTkLabel(
            form_frame,
            text="Nuevo Cliente",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.form_title.pack(pady=(12, 8))

        self.name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Nombre y Apellido",
            border_color=COLORS["cancel"],
            corner_radius=8,
        )
        self.name_entry.pack(fill="x", padx=12, pady=5)

        self.email_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Email (único)",
            border_color=COLORS["cancel"],
            corner_radius=8,
        )
        self.email_entry.pack(fill="x", padx=12, pady=5)

        self.phone_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Teléfono",
            border_color=COLORS["cancel"],
            corner_radius=8,
        )
        self.phone_entry.pack(fill="x", padx=12, pady=5)

        self.address_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Dirección",
            border_color=COLORS["cancel"],
            corner_radius=8,
        )
        self.address_entry.pack(fill="x", padx=12, pady=5)

        self.form_err_label = ctk.CTkLabel(
            form_frame,
            text="",
            text_color=COLORS["status_err"],
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.form_err_label.pack(pady=(2, 0))

        ctk.CTkButton(
            form_frame,
            text="Guardar Cliente",
            fg_color=COLORS["success"],
            hover_color=COLORS["success_hover"],
            corner_radius=8,
            command=self.save_customer,
        ).pack(fill="x", padx=12, pady=6)

        self.cancel_btn = ctk.CTkButton(
            form_frame,
            text="Cancelar Edición",
            fg_color=COLORS["cancel"],
            hover_color=COLORS["cancel_hover"],
            corner_radius=8,
            command=self.clear_form,
        )

    def refresh(self):
        result = CustomerService.get_all()
        if isinstance(result, tuple):
            customers, _err = result
        else:
            customers = result
        self._all_customers = [c for c in customers if isinstance(c, dict)] if isinstance(customers, list) else []
        self.apply_filter()

    def search_customer(self):
        email = self.email_search_entry.get().strip()
        if not email:
            self._all_customers = getattr(self, "_all_customers", [])
            self._render_customers([])
            self.search_result_label.configure(text="Ingresa un email para buscar.")
            return

        customers, err = CustomerService.search_by_email(email)
        if err or not customers:
            self.selected_customer = None
            self.search_result_label.configure(
                text=err or "Cliente no encontrado.",
                text_color=COLORS["status_err"],
            )
            self._render_customers([])
            return

        self.selected_customer = customers[0]
        if len(customers) == 1:
            customer = customers[0]
            self.search_result_label.configure(
                text=f"Encontrado: {customer.get('name')} ({customer.get('email')})",
                text_color=COLORS["status_ok"],
            )
        else:
            self.search_result_label.configure(
                text=f"Se encontraron {len(customers)} clientes. Elegí uno de la lista.",
                text_color=COLORS["status_ok"],
            )
        self._render_customers(customers)

    def _render_customers(self, customers: list):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not customers:
            ctk.CTkLabel(
                self.list_frame,
                text="Sin resultados.",
                text_color=COLORS["muted_text"],
            ).pack(pady=16)
            return

        for cust in customers:
            card = ctk.CTkFrame(self.list_frame, fg_color=COLORS["bg_card"], corner_radius=8)
            card.pack(fill="x", pady=4, padx=2)

            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=10, pady=8)

            ctk.CTkLabel(
                info,
                text=f"#{cust.get('id', '')} - {cust.get('name', '')}",
                font=ctk.CTkFont(size=14, weight="bold"),
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=f"Email: {cust.get('email', '')} | Tel: {cust.get('phone', '-')}",
                text_color=COLORS["muted_text"],
            ).pack(anchor="w")

            if cust.get("address"):
                ctk.CTkLabel(
                    info,
                    text=f"Dir: {cust.get('address')}",
                    text_color=COLORS["muted_text"],
                ).pack(anchor="w")

            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(side="right", padx=10, pady=8)

            ctk.CTkButton(
                actions,
                text="Editar",
                width=60,
                fg_color=COLORS["info"],
                hover_color=COLORS["info_hover"],
                corner_radius=8,
                command=lambda c=cust: self.load_customer(c),
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                actions,
                text="Eliminar",
                width=65,
                fg_color=COLORS["danger"],
                hover_color=COLORS["danger_hover"],
                corner_radius=8,
                command=lambda cid=cust.get("id"): self.delete_customer(cid),
            ).pack(side="left", padx=2)

    def load_customer(self, customer: dict):
        self.editing_customer_id = customer.get("id")
        self.form_title.configure(text="Editar Cliente")
        self.form_err_label.configure(text="")
        self.editing_registration_date = customer.get("registration_date")

        for entry, key in (
            (self.name_entry, "name"),
            (self.email_entry, "email"),
            (self.phone_entry, "phone"),
            (self.address_entry, "address"),
            
        ):
            entry.delete(0, "end")
            entry.insert(0, str(customer.get(key) or ""))

        self.cancel_btn.pack(fill="x", padx=12, pady=4)

    def clear_form(self):
        self.editing_customer_id = None
        self.editing_registration_date = None
        self.form_title.configure(text="Nuevo Cliente")
        self.form_err_label.configure(text="")
        for entry in (
            self.name_entry,
            self.email_entry,
            self.phone_entry,
            self.address_entry,
        ):
            entry.delete(0, "end")
        self.cancel_btn.pack_forget()

    def save_customer(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not email or not phone or not address:
            self.form_err_label.configure(
                text="Nombre, email, teléfono y dirección son obligatorios."
            )
            return

        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "registration_date": self.editing_registration_date or date.today().isoformat(),
        }

        if self.editing_customer_id is None:
            ok, err = CustomerService.create(payload)
            msg = "Cliente creado." if ok else (err or "Error al crear cliente.")
        else:
            ok, err = CustomerService.update(self.editing_customer_id, payload)
            msg = "Cliente actualizado." if ok else (err or "Error al actualizar cliente.")

        if ok:
            self.status_label.configure(text=msg, text_color=COLORS["status_ok"])
            self.clear_form()
            self.refresh()
        else:
            self.form_err_label.configure(text=msg)

    def delete_customer(self, customer_id):
        if not customer_id:
            return
        ok, err = CustomerService.delete(customer_id)
        if ok:
            self.status_label.configure(text="Cliente eliminado.", text_color=COLORS["status_ok"])
            if self.editing_customer_id == customer_id:
                self.clear_form()
            self.refresh()
        else:
            self.status_label.configure(
                text=err or "Error al eliminar cliente.",
                text_color=COLORS["status_err"],
            )
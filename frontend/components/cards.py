import customtkinter as ctk
from frontend.config import COLORS


class ArticleCard(ctk.CTkFrame):

    def __init__(self, master, article: dict, on_edit, on_delete):
        super().__init__(
            master,
            fg_color=COLORS["bg_card"],
            border_width=1,
            border_color=COLORS["cancel"],
            corner_radius=10,
        )
        self.article = article
        self.on_edit = on_edit
        self.on_delete = on_delete

        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        article_id = article.get("id", "")
        name = article.get("name", "")
        title_text = f"#{article_id} - {name}" if article_id else name
        name_label = ctk.CTkLabel(
            info_frame,
            text=title_text,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        name_label.pack(anchor="w")

        description = article.get("description", "")
        if description:
            desc_label = ctk.CTkLabel(
                info_frame,
                text=description,
                text_color=COLORS["muted_text"],
            )
            desc_label.pack(anchor="w")

        unit_price = float(article.get("unit_price", 0.0) or 0.0)
        sale_price = float(article.get("sale_price", 0.0) or 0.0)
        stock = article.get("stock", 0)

        meta_parts = [
            f"Costo: ${unit_price:.2f}",
            f"Venta: ${sale_price:.2f}",
            f"Stock: {stock}",
        ]
        if article.get("id_Category") is not None:
            meta_parts.append(f"Cat: #{article.get('id_Category')}")
        if article.get("id_Supplier") is not None:
            meta_parts.append(f"Prov: #{article.get('id_Supplier')}")

        stock_num = int(stock or 0)
        details_color = COLORS["danger"] if stock_num <= 0 else COLORS["muted_text"]

        details_label = ctk.CTkLabel(
            info_frame,
            text=" | ".join(meta_parts),
            text_color=details_color,
        )
        details_label.pack(anchor="w")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="right", padx=10, pady=10)

        edit_btn = ctk.CTkButton(
            btn_frame,
            text="Editar",
            width=62,
            fg_color=COLORS["info"],
            hover_color=COLORS["info_hover"],
            corner_radius=8,
            command=lambda: self.on_edit(self.article),
        )
        edit_btn.pack(side="left", padx=2)

        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Eliminar",
            width=68,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            corner_radius=8,
            command=lambda: self.on_delete(self.article.get("id")),
        )
        delete_btn.pack(side="left", padx=2)
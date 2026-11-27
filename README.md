# Control de Stock & Inventario

Sistema de gestión de inventario, clientes y facturación desarrollado con **FastAPI**, **CustomTkinter** y **SQLite**.

## Requisitos previos

- **Python 3.11** o superior.
- **Git** (para clonar el repositorio).

## Instalación y configuración del entorno

1. Clona el repositorio y entra a la carpeta del proyecto:

```bash
git clone (https://github.com/vanu223126-tech/PROYECTO-FINAL-ERP-GESTION-DE-STOCK-E-INVENTARIO/)

1-Crea y activa el entorno virtual:
python -m venv .venv
.venv\Scripts\Activate.ps1

2-Instala las dependencias:

Bash
pip install --upgrade pip
pip install -r requirements.txt

Base de datos
El proyecto incluye la base de datos SQLite stock_e_inventory.db para trabajar con los datos iniciales de artículos, clientes y facturación.

Cómo ejecutar el servidor y la interfaz gráfica
Ejecutar aplicación completa (launcher.py)
Con el entorno virtual activado en la raíz del proyecto:
python launcher.py

Levantar únicamente el servidor FastAPI (opcional)
Bash
uvicorn app.main:app --reload

Documentación interactiva disponible en http://127.0.0.1:8000/docs mientras el servidor esté en ejecución.

Compilación del ejecutable en Windows (opcional)
Bash
pyinstaller --noconfirm --clean --name GestionInventario --collect-all customtkinter --collect-all uvicorn --collect-submodules app --collect-submodules frontend launcher.py
El ejecutable se genera en dist\GestionInventario\GestionInventario.exe (excluido del control de versiones mediante .gitignore).


### Cómo pegarlo en GitHub
1. Entra a tu repositorio en **GitHub** y haz clic en **Add file** > **Create new file**.
2. Escribe `README.md` como nombre de archivo.
3. Pega el contenido del bloque anterior, haz clic en **Commit changes...** y confirma el guardado.

<ElicitationsGroup message="Si quieres ajustar algún dato antes de confirmar en GitHub:">
  <Elicitation label="Poner URL exacta" query="Te paso la URL exacta de mi repositorio de GitHub para dejarla lista en el README."/>
  <Elicitation label="Ajustar comando uvicorn" query="Te digo el nombre exacto de mi archivo principal de FastAPI para el README."/>
  <Elicitation label="Revisar requirements.txt" query="¿Cómo creo un requirements.txt limpio para incluir en el repositorio?"/>
</ElicitationsGroup>


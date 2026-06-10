import os
import subprocess
import sys
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ModuleNotFoundError:
    tk = None
    filedialog = None
    messagebox = None
    ttk = None

from app_paths import EXPORTS_DIR, JOBS_DIR, LINUX_ICON_FILE, LOGS_DIR, ROOT_DIR, SAMPLE_IMAGES_DIR, ensure_app_dirs, get_version
from catalog_manager import CatalogManager
from image_processor import EXPORT_TARGETS, ImageProcessor
from license_manager import LicenseManager
from print_manager import PrintManager
from project_manager import ProjectManager
from support_info import SUPPORT_EMAIL, WEBSITE, build_support_info, format_support_info


APP_NAME = "PuzzleProof Studio"
SUBTITLE = "Artist-to-Puzzle Production Utility"
COPYRIGHT = "© 2026 Wonder Piece Studio. All Rights Reserved."
DEFAULT_COPYRIGHT_TEXT = COPYRIGHT
BRAND_LINE = "BayouFinds / Wonder Piece Studio"
THEME = {
    "green": "#1D3A37",
    "green_hover": "#294B47",
    "gold": "#D1A24A",
    "ivory": "#F5F0E6",
    "panel": "#FFF9EE",
    "panel_alt": "#EFE6D6",
    "text": "#1A1A1A",
    "muted": "#665E52",
    "border": "#D8CBB8",
    "white": "#FFFFFF",
}

APPROVAL_STATUSES = ("Draft", "Pending", "Non-Licensed", "Approved", "Revoked")
PROJECT_ORIGINS = (
    "Artist Submission",
    "Company Project",
    "BayouFinds Original",
    "Wonder Piece Studio Original",
)
PLACEMENTS = ("Bottom Right", "Bottom Left", "Bottom Center")


def display_version(version):
    version = str(version).strip()
    if not version:
        return "v0.1.0-EarlyAccess"
    return version if version.lower().startswith("v") else f"v{version}"


def open_folder(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(path))  # noqa: S606 - user-requested local folder open
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except OSError as exc:
        messagebox.showwarning("Open Folder", f"Could not open folder:\n{path}\n\n{exc}")


class PuzzleProofApp:
    def __init__(self, root):
        self.root = root
        self.version = get_version()
        self.license_status = LicenseManager().load_license()
        self.catalog = CatalogManager()
        self.projects = ProjectManager()
        self.images = ImageProcessor()
        self.printing = PrintManager()
        self.display_version = display_version(self.version)
        self.source_image = tk.StringVar()
        self.license_text = tk.StringVar(value=f"License: {self.license_status.display}")
        self.status_text = tk.StringVar(value="Ready.")
        self.project_vars = {}

        self._configure_window()
        self._configure_theme()
        self._show_splash_then_main()

    def _configure_window(self):
        self.root.title(f"{APP_NAME} {self.display_version}")
        self.root.geometry("1160x760")
        self.root.minsize(960, 660)
        self.root.configure(bg=THEME["ivory"])
        self._set_window_icon()

    def _set_window_icon(self):
        if not LINUX_ICON_FILE.exists():
            return
        try:
            self.root.iconbitmap(f"@{LINUX_ICON_FILE}")
        except tk.TclError:
            pass

    def _configure_theme(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        default_font = ("TkDefaultFont", 10)
        style.configure(".", font=default_font, background=THEME["ivory"], foreground=THEME["text"])
        style.configure("TFrame", background=THEME["ivory"])
        style.configure("App.TFrame", background=THEME["ivory"])
        style.configure("Card.TFrame", background=THEME["panel"], relief="solid", borderwidth=1)
        style.configure("InfoCard.TFrame", background=THEME["panel_alt"], relief="solid", borderwidth=1)
        style.configure("TLabel", background=THEME["ivory"], foreground=THEME["text"])
        style.configure("TButton", padding=(12, 7), background=THEME["green"], foreground=THEME["white"], bordercolor=THEME["green"], focusthickness=2, focuscolor=THEME["gold"])
        style.map(
            "TButton",
            background=[("active", THEME["green_hover"]), ("pressed", THEME["green"])],
            foreground=[("disabled", THEME["muted"]), ("active", THEME["white"])],
        )
        style.configure("Secondary.TButton", background=THEME["panel_alt"], foreground=THEME["green"], bordercolor=THEME["border"])
        style.map(
            "Secondary.TButton",
            background=[("active", "#E4D8C5"), ("pressed", THEME["panel_alt"])],
            foreground=[("active", THEME["green"])],
        )
        style.configure("TEntry", fieldbackground=THEME["white"], foreground=THEME["text"])
        style.configure("TCombobox", fieldbackground=THEME["white"], foreground=THEME["text"])
        style.configure("TSpinbox", fieldbackground=THEME["white"], foreground=THEME["text"])
        style.configure("TLabelframe", background=THEME["panel"], foreground=THEME["text"], bordercolor=THEME["border"])
        style.configure("TLabelframe.Label", background=THEME["panel"], foreground=THEME["green"], font=("TkDefaultFont", 10, "bold"))
        style.configure("TNotebook", background=THEME["ivory"], borderwidth=0)
        style.configure("TNotebook.Tab", padding=(18, 10), background=THEME["panel_alt"], foreground=THEME["text"], borderwidth=0)
        style.map(
            "TNotebook.Tab",
            background=[("selected", THEME["panel"]), ("active", "#E4D8C5")],
            foreground=[("selected", THEME["green"]), ("active", THEME["green"])],
        )
        style.configure("Treeview", background=THEME["white"], fieldbackground=THEME["white"], foreground=THEME["text"], rowheight=26)
        style.configure("Treeview.Heading", background=THEME["green"], foreground=THEME["white"], font=("TkDefaultFont", 10, "bold"))
        style.configure("Header.TFrame", background=THEME["green"])
        style.configure("HeaderTitle.TLabel", background=THEME["green"], foreground=THEME["gold"], font=("TkDefaultFont", 25, "bold"))
        style.configure("HeaderMeta.TLabel", background=THEME["green"], foreground=THEME["white"], font=("TkDefaultFont", 11))
        style.configure("HeaderEyebrow.TLabel", background=THEME["green"], foreground="#EADFCB", font=("TkDefaultFont", 9, "bold"))
        style.configure("License.TLabel", background=THEME["panel_alt"], foreground=THEME["green"], padding=(12, 6), font=("TkDefaultFont", 9, "bold"))
        style.configure("Footer.TLabel", background=THEME["green"], foreground=THEME["white"], font=("TkDefaultFont", 9))
        style.configure("FooterMuted.TLabel", background=THEME["green"], foreground="#EADFCB", font=("TkDefaultFont", 9))
        style.configure("Muted.TLabel", background=THEME["ivory"], foreground=THEME["muted"])
        style.configure("CardMuted.TLabel", background=THEME["panel"], foreground=THEME["muted"])
        style.configure("CardTitle.TLabel", background=THEME["panel"], foreground=THEME["green"], font=("TkDefaultFont", 12, "bold"))
        style.configure("InfoTitle.TLabel", background=THEME["panel_alt"], foreground=THEME["green"], font=("TkDefaultFont", 11, "bold"))
        style.configure("InfoText.TLabel", background=THEME["panel_alt"], foreground=THEME["muted"])
        style.configure("Splash.TFrame", background=THEME["green"])
        style.configure("SplashTitle.TLabel", background=THEME["green"], foreground=THEME["gold"], font=("TkDefaultFont", 23, "bold"))
        style.configure("SplashMeta.TLabel", background=THEME["green"], foreground=THEME["gold"])
        style.configure("SplashText.TLabel", background=THEME["green"], foreground=THEME["white"])
        style.configure("AboutTitle.TLabel", background=THEME["ivory"], foreground=THEME["green"], font=("TkDefaultFont", 16, "bold"))

    def _show_splash_then_main(self):
        self.splash = tk.Toplevel(self.root)
        self.splash.overrideredirect(True)
        self.splash.configure(bg=THEME["green"])
        self.splash.geometry("560x330+260+180")
        frame = ttk.Frame(self.splash, padding=28, style="Splash.TFrame")
        frame.pack(fill="both", expand=True)
        self._draw_brand_mark(frame, size=78, background=THEME["green"]).pack(anchor="center", pady=(0, 12))
        ttk.Label(frame, text=APP_NAME, style="SplashTitle.TLabel").pack(anchor="center", pady=(8, 4))
        ttk.Label(frame, text=SUBTITLE, style="SplashText.TLabel", font=("TkDefaultFont", 12)).pack(anchor="center")
        ttk.Label(frame, text=BRAND_LINE, style="SplashText.TLabel").pack(anchor="center", pady=(9, 0))
        ttk.Label(frame, text=self.display_version, style="SplashMeta.TLabel").pack(anchor="center", pady=(13, 0))
        ttk.Label(frame, text=f"License: {self.license_status.display}", style="SplashText.TLabel", wraplength=480).pack(anchor="center", pady=(10, 0))
        ttk.Label(frame, text=f"Copyright: {COPYRIGHT}", style="SplashText.TLabel").pack(anchor="center", pady=(18, 0))
        self.root.withdraw()
        self.root.after(2300, self._build_main_window)

    def _draw_brand_mark(self, parent, size=58, background=None):
        bg = background or THEME["ivory"]
        canvas = tk.Canvas(parent, width=size, height=size, bg=bg, highlightthickness=0, bd=0)
        pad = max(5, size // 10)
        canvas.create_oval(pad, pad, size - pad, size - pad, fill=THEME["green"], outline=THEME["gold"], width=3)
        canvas.create_oval(size * 0.26, size * 0.24, size * 0.73, size * 0.64, fill=THEME["panel_alt"], outline=THEME["gold"], width=2)
        canvas.create_oval(size * 0.36, size * 0.35, size * 0.43, size * 0.42, fill=THEME["green"], outline="")
        canvas.create_oval(size * 0.48, size * 0.31, size * 0.55, size * 0.38, fill=THEME["gold"], outline="")
        canvas.create_oval(size * 0.59, size * 0.39, size * 0.66, size * 0.46, fill=THEME["muted"], outline="")
        canvas.create_polygon(
            size * 0.39,
            size * 0.50,
            size * 0.68,
            size * 0.72,
            size * 0.62,
            size * 0.79,
            size * 0.33,
            size * 0.57,
            fill=THEME["gold"],
            outline=THEME["text"],
        )
        canvas.create_rectangle(size * 0.34, size * 0.70, size * 0.52, size * 0.84, fill=THEME["green"], outline=THEME["gold"], width=2)
        canvas.create_oval(size * 0.45, size * 0.65, size * 0.57, size * 0.77, fill=THEME["green"], outline=THEME["gold"], width=2)
        return canvas

    def _build_main_window(self):
        self.splash.destroy()
        self.root.deiconify()

        container = ttk.Frame(self.root, padding=16, style="App.TFrame")
        container.pack(fill="both", expand=True)
        header = ttk.Frame(container, style="Header.TFrame", padding=(20, 18))
        header.pack(fill="x", pady=(0, 12))

        self._draw_brand_mark(header, size=74, background=THEME["green"]).pack(side="left", padx=(0, 18))

        title_group = ttk.Frame(header, style="Header.TFrame")
        title_group.pack(side="left", fill="x", expand=True)
        ttk.Label(title_group, text=BRAND_LINE.upper(), style="HeaderEyebrow.TLabel").pack(anchor="w")
        ttk.Label(title_group, text=APP_NAME, style="HeaderTitle.TLabel").pack(anchor="w", pady=(2, 0))
        ttk.Label(title_group, text=f"{SUBTITLE} | {self.display_version}", style="HeaderMeta.TLabel").pack(anchor="w", pady=(4, 0))
        ttk.Label(header, textvariable=self.license_text, style="License.TLabel").pack(side="right", padx=(16, 0))

        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)
        self._build_project_tab(notebook)
        self._build_image_tab(notebook)
        self._build_catalog_tab(notebook)
        self._build_printing_tab(notebook)
        self._build_support_tab(notebook)
        self._build_about_tab(notebook)

        footer = ttk.Frame(container, style="Header.TFrame", padding=(10, 7))
        footer.pack(fill="x", pady=(10, 0))
        ttk.Label(footer, textvariable=self.status_text, style="Footer.TLabel").pack(side="left")
        ttk.Label(footer, textvariable=self.license_text, style="FooterMuted.TLabel").pack(side="left", padx=(18, 0))
        ttk.Label(footer, text=f"{WEBSITE} | {SUPPORT_EMAIL}", style="Footer.TLabel").pack(side="right")

    def _card(self, parent, padding=14, style="Card.TFrame"):
        card = ttk.Frame(parent, padding=padding, style=style)
        return card

    def _build_info_panel(self, parent, title, body):
        panel = self._card(parent, padding=14, style="InfoCard.TFrame")
        ttk.Label(panel, text=title, style="InfoTitle.TLabel").pack(anchor="w")
        ttk.Label(panel, text=body, style="InfoText.TLabel", wraplength=260, justify="left").pack(anchor="w", pady=(6, 0))
        return panel

    def _build_action_card(self, parent, title, description, button_text, command, button_style="TButton"):
        card = self._card(parent, padding=14)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text=description, style="CardMuted.TLabel", wraplength=250, justify="left").pack(anchor="w", pady=(6, 12))
        ttk.Button(card, text=button_text, command=command, style=button_style).pack(anchor="w", fill="x")
        return card

    def _build_project_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=14)
        notebook.add(tab, text="Project")
        form = ttk.LabelFrame(tab, text="Project Details", padding=14)
        form.pack(fill="both", expand=True)

        fields = (
            ("artist_name", "Artist Name"),
            ("artwork_title", "Artwork Title"),
            ("contact_information", "Contact Information"),
            ("copyright_owner", "Copyright Owner"),
            ("company_name", "Company Name"),
            ("catalog_number", "Catalog Number"),
        )
        for row, (key, label) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=4)
            var = tk.StringVar()
            self.project_vars[key] = var
            ttk.Entry(form, textvariable=var).grid(row=row, column=1, sticky="ew", pady=4, padx=(12, 24))

        ttk.Label(form, text="Approval Status").grid(row=0, column=2, sticky="w", pady=4)
        self.project_vars["approval_status"] = tk.StringVar(value="Draft")
        ttk.Combobox(form, textvariable=self.project_vars["approval_status"], values=APPROVAL_STATUSES, state="readonly").grid(row=0, column=3, sticky="ew", pady=4, padx=(12, 0))

        ttk.Label(form, text="Project Origin").grid(row=1, column=2, sticky="w", pady=4)
        self.project_vars["project_origin"] = tk.StringVar(value="Artist Submission")
        ttk.Combobox(form, textvariable=self.project_vars["project_origin"], values=PROJECT_ORIGINS, state="readonly").grid(row=1, column=3, sticky="ew", pady=4, padx=(12, 0))

        ttk.Label(form, text="Project Notes").grid(row=6, column=0, sticky="nw", pady=(12, 4))
        self.notes_text = tk.Text(
            form,
            height=8,
            wrap="word",
            bg=THEME["white"],
            fg=THEME["text"],
            insertbackground=THEME["text"],
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=THEME["border"],
            highlightcolor=THEME["gold"],
        )
        self.notes_text.grid(row=6, column=1, columnspan=3, sticky="nsew", pady=(12, 4), padx=(12, 0))

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)
        form.rowconfigure(6, weight=1)

        ttk.Label(tab, text="Required before manufacturing: approved status, source artwork, copyright owner, and at least one export.", style="Muted.TLabel").pack(anchor="w", pady=(10, 0))

        buttons = ttk.Frame(tab)
        buttons.pack(fill="x", pady=(14, 0))
        project_actions = (
            ("New Project", self.new_project),
            ("Save Project", lambda: self.save_project(show_confirmation=True)),
            ("Open Project Folder", lambda: open_folder(self.current_project_folder())),
            ("Generate Artist Release", lambda: self.generate_print_document("Artist Release")),
            ("Mark Manufacturing Ready", self.mark_manufacturing_ready),
        )
        for index, (label, command) in enumerate(project_actions):
            ttk.Button(buttons, text=label, command=command).grid(row=0, column=index, sticky="ew", padx=(0 if index == 0 else 8, 0), pady=2)
            buttons.columnconfigure(index, weight=1)

    def _build_image_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=14)
        notebook.add(tab, text="Image Conversion")

        source = ttk.LabelFrame(tab, text="Source Artwork", padding=12)
        source.pack(fill="x")
        ttk.Entry(source, textvariable=self.source_image).pack(side="left", fill="x", expand=True)
        ttk.Button(source, text="Import Artwork", command=self.import_artwork).pack(side="left", padx=(8, 0))

        options = ttk.LabelFrame(tab, text="Export Options", padding=12)
        options.pack(fill="x", pady=14)
        self.export_type = tk.StringVar(value="Puzzle")
        self.export_format = tk.StringVar(value="PNG")
        self.copyright_text = tk.StringVar(value=DEFAULT_COPYRIGHT_TEXT)
        self.placement = tk.StringVar(value="Bottom Right")
        self.font_size = tk.IntVar(value=42)
        self.opacity = tk.IntVar(value=180)

        rows = (
            ("Export Type", ttk.Combobox(options, textvariable=self.export_type, values=tuple(EXPORT_TARGETS.keys()), state="readonly")),
            ("Format", ttk.Combobox(options, textvariable=self.export_format, values=("PNG", "JPEG"), state="readonly")),
            ("Copyright Text", ttk.Entry(options, textvariable=self.copyright_text)),
            ("Placement", ttk.Combobox(options, textvariable=self.placement, values=PLACEMENTS, state="readonly")),
            ("Font Size", ttk.Spinbox(options, from_=14, to=96, textvariable=self.font_size)),
            ("Opacity", ttk.Spinbox(options, from_=40, to=255, textvariable=self.opacity)),
        )
        for row, (label, widget) in enumerate(rows):
            ttk.Label(options, text=label).grid(row=row, column=0, sticky="w", pady=4)
            widget.grid(row=row, column=1, sticky="ew", pady=4, padx=(10, 0))
        options.columnconfigure(1, weight=1)

        ttk.Button(tab, text="Apply Crop/Resize and Export", command=self.export_image).pack(anchor="w")
        self.sample_label = ttk.Label(tab, text=self.sample_artwork_status(), padding=(0, 18, 0, 0))
        self.sample_label.pack(anchor="w")

    def _build_catalog_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=14)
        notebook.add(tab, text="Catalog")
        search = ttk.LabelFrame(tab, text="Search Catalog", padding=12)
        search.pack(fill="x")
        self.catalog_search_vars = {
            "artist_name": tk.StringVar(),
            "artwork_title": tk.StringVar(),
            "catalog_number": tk.StringVar(),
        }
        search_fields = (
            ("artist_name", "Artist Name"),
            ("artwork_title", "Artwork Title"),
            ("catalog_number", "Catalog ID"),
        )
        for column, (key, label) in enumerate(search_fields):
            ttk.Label(search, text=label).grid(row=0, column=column, sticky="w", padx=(0 if column == 0 else 12, 0))
            ttk.Entry(search, textvariable=self.catalog_search_vars[key]).grid(row=1, column=column, sticky="ew", padx=(0 if column == 0 else 12, 0), pady=(4, 0))
            search.columnconfigure(column, weight=1)
        actions = ttk.Frame(search)
        actions.grid(row=1, column=3, sticky="e", padx=(12, 0), pady=(4, 0))
        ttk.Button(actions, text="Search", command=self.refresh_catalog).pack(side="left")
        ttk.Button(actions, text="Show All", command=self.clear_catalog_search).pack(side="left", padx=(8, 0))

        self.catalog_result_text = tk.StringVar(value="Catalog records: 0")
        ttk.Label(tab, textvariable=self.catalog_result_text, style="Muted.TLabel").pack(anchor="w", pady=(10, 0))

        columns = ("catalog", "artist", "artwork", "approval", "ready", "updated")
        self.catalog_tree = ttk.Treeview(tab, columns=columns, show="headings", height=16)
        headings = {
            "catalog": "Catalog ID",
            "artist": "Artist",
            "artwork": "Artwork",
            "approval": "Approval",
            "ready": "Manufacturing Ready",
            "updated": "Updated",
        }
        for column, heading in headings.items():
            self.catalog_tree.heading(column, text=heading)
        self.catalog_tree.column("catalog", width=150, minwidth=120)
        self.catalog_tree.column("artist", width=180, minwidth=140)
        self.catalog_tree.column("artwork", width=220, minwidth=160)
        self.catalog_tree.column("approval", width=120, minwidth=90)
        self.catalog_tree.column("ready", width=160, minwidth=120)
        self.catalog_tree.column("updated", width=150, minwidth=120)
        self.catalog_tree.pack(fill="both", expand=True, pady=12)
        ttk.Button(tab, text="Refresh Catalog", command=self.refresh_catalog).pack(anchor="w")
        self.refresh_catalog()

    def _build_printing_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=16)
        notebook.add(tab, text="Printing")
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=0)
        tab.rowconfigure(1, weight=1)

        intro = self._card(tab, padding=(16, 14))
        intro.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        ttk.Label(intro, text="Printing Command Center", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            intro,
            text="Create print-ready HTML files for production records, artist paperwork, packaging inserts, and release handoff.",
            style="CardMuted.TLabel",
            wraplength=820,
            justify="left",
        ).pack(anchor="w", pady=(5, 0))

        actions = ttk.Frame(tab)
        actions.grid(row=1, column=0, sticky="nsew", padx=(0, 14))
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)

        document_cards = (
            (
                "Artist Release",
                "Permission record for artwork reproduction and project approval.",
                "Print Artist Release",
                lambda: self.generate_print_document("Artist Release"),
            ),
            (
                "Copyright Form",
                "Ownership and copyright notes for cleaner manufacturing records.",
                "Print Copyright Form",
                lambda: self.generate_print_document("Copyright Form"),
            ),
            (
                "Production Sheet",
                "Internal production details for puzzle sizing, approvals, and export notes.",
                "Print Production Sheet",
                lambda: self.generate_print_document("Production Sheet"),
            ),
            (
                "Sticker",
                "Print-ready sticker copy for package labeling and shop workflow.",
                "Print Sticker",
                lambda: self.generate_print_document("Sticker"),
            ),
            (
                "Insert",
                "Customer insert content for puzzle packaging and creator attribution.",
                "Print Insert",
                lambda: self.generate_print_document("Insert"),
            ),
            (
                "Puzzle Cover",
                "Front cover reference sheet for proofing, packaging, and production.",
                "Print Puzzle Cover",
                lambda: self.generate_print_document("Puzzle Cover"),
            ),
        )
        for index, (title, description, button_text, command) in enumerate(document_cards):
            row = index // 2
            column = index % 2
            card = self._build_action_card(actions, title, description, button_text, command)
            card.grid(row=row, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 0), pady=(0, 10))
            actions.rowconfigure(row, weight=1)

        sidebar = ttk.Frame(tab)
        sidebar.grid(row=1, column=1, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)

        self._build_info_panel(
            sidebar,
            "Output Location",
            f"Generated files are saved in:\n{EXPORTS_DIR}",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self._build_info_panel(
            sidebar,
            "Before You Print",
            "Confirm approval status, copyright owner, source artwork, and export files before packaging.",
        ).grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self._build_info_panel(
            sidebar,
            "License Status",
            self.license_status.display,
        ).grid(row=2, column=0, sticky="ew", pady=(0, 10))

        package = self._card(sidebar, padding=14)
        package.grid(row=3, column=0, sticky="ew")
        ttk.Label(package, text="Production Package", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            package,
            text="Generate the full paperwork set or open the export folder for review.",
            style="CardMuted.TLabel",
            wraplength=260,
            justify="left",
        ).pack(anchor="w", pady=(6, 12))
        ttk.Button(package, text="Print Production Package", command=self.generate_production_package).pack(fill="x")
        ttk.Button(package, text="Open Exports Folder", command=lambda: open_folder(EXPORTS_DIR), style="Secondary.TButton").pack(fill="x", pady=(8, 0))

    def _build_support_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=14)
        notebook.add(tab, text="Support")
        self.support_info = build_support_info(self.license_status)
        ttk.Label(tab, text=format_support_info(self.support_info), justify="left").pack(anchor="w")
        buttons = ttk.Frame(tab)
        buttons.pack(anchor="w", pady=16)
        ttk.Button(buttons, text="Open Logs Folder", command=lambda: open_folder(LOGS_DIR)).pack(side="left")
        ttk.Button(buttons, text="Open Project Folder", command=lambda: open_folder(JOBS_DIR)).pack(side="left", padx=8)
        ttk.Button(buttons, text="Copy Support Info", command=self.copy_support_info).pack(side="left")

    def _build_about_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=18)
        notebook.add(tab, text="About")
        header = ttk.Frame(tab)
        header.pack(anchor="nw", fill="x", pady=(0, 14))
        self._draw_brand_mark(header, size=64).pack(side="left", padx=(0, 14))
        title_block = ttk.Frame(header)
        title_block.pack(side="left", fill="x", expand=True)
        ttk.Label(title_block, text=APP_NAME, style="AboutTitle.TLabel").pack(anchor="w")
        ttk.Label(title_block, text=f"{SUBTITLE} | {self.display_version}", style="Muted.TLabel").pack(anchor="w", pady=(3, 0))
        text = (
            "Built for Sean's artist-to-puzzle workflow.\n\n"
            "Developed by BayouFinds / Wonder Piece Studio.\n\n"
            f"Website: {WEBSITE}\n"
            f"Support: {SUPPORT_EMAIL}\n\n"
            f"Copyright: {COPYRIGHT}\n\n"
            "License: Offline yearly license using license.json."
        )
        ttk.Label(tab, text=text, justify="left", font=("TkDefaultFont", 11)).pack(anchor="nw")

    def collect_project(self):
        project = {key: var.get().strip() for key, var in self.project_vars.items()}
        project["project_notes"] = self.notes_text.get("1.0", "end").strip()
        project["source_image"] = self.source_image.get().strip()
        project["export_files"] = getattr(self, "export_files", [])
        project["manufacturing_ready"] = getattr(self, "manufacturing_ready", False)
        return project

    def new_project(self):
        for var in self.project_vars.values():
            var.set("")
        self.project_vars["approval_status"].set("Draft")
        self.project_vars["project_origin"].set("Artist Submission")
        self.notes_text.delete("1.0", "end")
        self.source_image.set("")
        self.export_files = []
        self.manufacturing_ready = False
        self.status_text.set("New draft project started.")

    def save_project(self, show_confirmation=False):
        project = self.collect_project()
        if not project.get("catalog_number"):
            project["catalog_number"] = self.catalog.next_catalog_id()
            self.project_vars["catalog_number"].set(project["catalog_number"])
        saved_project = self.catalog.upsert(project)
        path = self.projects.save(saved_project)
        self.status_text.set(f"Project saved: {path}")
        self.refresh_catalog()
        if show_confirmation:
            messagebox.showinfo(
                "Project Saved",
                f"Saved project JSON:\n{path}\n\nUpdated catalog:\n{self.catalog.catalog_file}",
            )
        return saved_project

    def current_project_folder(self):
        project = self.collect_project()
        if project.get("project_folder"):
            return Path(project["project_folder"])
        return self.projects.project_folder(project)

    def import_artwork(self):
        path = filedialog.askopenfilename(
            title="Import Artwork",
            filetypes=(("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")),
        )
        if path:
            self.source_image.set(path)
            self.status_text.set(f"Imported artwork: {path}")

    def export_image(self):
        if not self.source_image.get():
            messagebox.showwarning("Image Conversion", "Import a source image before exporting.")
            return
        try:
            output_path = self.images.export(
                self.source_image.get(),
                self.export_type.get(),
                self.export_format.get(),
                self.copyright_text.get(),
                self.placement.get(),
                self.opacity.get(),
                self.font_size.get(),
            )
        except Exception as exc:  # noqa: BLE001 - GUI should report and continue
            messagebox.showerror("Image Conversion", str(exc))
            return
        self.export_files = list(dict.fromkeys(getattr(self, "export_files", []) + [str(output_path)]))
        self.status_text.set(f"Export created: {output_path}")
        self.save_project()

    def mark_manufacturing_ready(self):
        project = self.collect_project()
        errors = self.projects.manufacturing_ready_errors(project)
        if errors:
            messagebox.showwarning("Manufacturing Ready", "\n".join(errors))
            return
        self.manufacturing_ready = True
        self.status_text.set("Project marked Manufacturing Ready.")
        self.save_project()

    def refresh_catalog(self):
        if not hasattr(self, "catalog_tree"):
            return
        self.catalog.records = self.catalog.load_records()
        self.catalog_tree.delete(*self.catalog_tree.get_children())
        if hasattr(self, "catalog_search_vars"):
            records = self.catalog.search_fields(
                artist_name=self.catalog_search_vars["artist_name"].get(),
                artwork_title=self.catalog_search_vars["artwork_title"].get(),
                catalog_number=self.catalog_search_vars["catalog_number"].get(),
            )
        else:
            records = list(self.catalog.records)
        for record in records:
            self.catalog_tree.insert(
                "",
                "end",
                values=(
                    record.get("catalog_number", ""),
                    record.get("artist_name", ""),
                    record.get("artwork_title", ""),
                    record.get("approval_status", ""),
                    "Yes" if record.get("manufacturing_ready") else "No",
                    record.get("updated_at", ""),
                ),
            )
        if hasattr(self, "catalog_result_text"):
            self.catalog_result_text.set(f"Matching records: {len(records)}")

    def clear_catalog_search(self):
        for var in self.catalog_search_vars.values():
            var.set("")
        self.refresh_catalog()

    def generate_print_document(self, document_type):
        project = self.save_project()
        path = self.printing.create_document(document_type, project)
        self.status_text.set(f"Print-ready file created: {path}")
        messagebox.showinfo("Printing", f"Created print-ready file:\n{path}")

    def generate_production_package(self):
        project = self.save_project()
        paths = self.printing.create_production_package(project)
        self.status_text.set(f"Production package created with {len(paths)} files.")
        messagebox.showinfo("Printing", f"Created {len(paths)} print-ready files in:\n{EXPORTS_DIR}")

    def copy_support_info(self):
        text = format_support_info(self.support_info)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_text.set("Support information copied to clipboard.")

    def sample_artwork_status(self):
        sample = SAMPLE_IMAGES_DIR / "bayou-sunset-sample.png"
        if sample.exists():
            return f"Sample artwork installed: {sample}"
        return "Bayou Sunset sample image not installed yet."


def main():
    if tk is None:
        print(
            "PuzzleProof Studio requires Tkinter. On Fedora, install it with: sudo dnf install python3-tkinter",
            file=sys.stderr,
        )
        sys.exit(1)
    ensure_app_dirs()
    root = tk.Tk()
    PuzzleProofApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

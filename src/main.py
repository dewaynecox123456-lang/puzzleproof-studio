import logging
import os
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ModuleNotFoundError:
    tk = None
    filedialog = None
    messagebox = None
    ttk = None

from app_paths import (
    EXPORTS_DIR,
    JOBS_DIR,
    LINUX_ICON_FILE,
    LOGS_DIR,
    RESOURCE_ROOT,
    ROOT_DIR,
    SAMPLE_IMAGES_DIR,
    ensure_app_dirs,
    get_version,
)
from catalog_manager import CatalogManager
from image_processor import EXPORT_TARGETS, OUTPUT_FORMATS, ImageProcessor
from license_manager import LicenseManager
from print_manager import PrintManager
from project_manager import ProjectManager
from support_info import SUPPORT_EMAIL, WEBSITE, build_support_info, format_support_info


APP_NAME = "PuzzleProof Studio"
SUBTITLE = "Artist-to-Puzzle Production Utility"
COPYRIGHT = "© 2026 Wonder Piece Studio. All Rights Reserved."
DEFAULT_COPYRIGHT_TEXT = COPYRIGHT
BRAND_LINE = "BayouFinds / Wonder Piece Studio"
PRODUCT_WEBSITE = "https://puzzleproof-studio.netlify.app/"
BAYOUFINDS_WEBSITE = "https://www.bayoufinds.com"
GITHUB_REPOSITORY = "https://github.com/dewaynecox123456-lang/puzzleproof-studio"
BUG_REPORTS_URL = "https://github.com/dewaynecox123456-lang/puzzleproof-studio/issues"
DOCUMENTATION_URL = GITHUB_REPOSITORY
FAQ_SOURCE_FILE = RESOURCE_ROOT / "docs" / "FAQ.md"
LOGGER = logging.getLogger(__name__)
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
PRINTER_GUIDANCE = {
    "Puzzle Print": "Sublimation printer / sublimation paper",
    "Box Insert": "Standard printer / regular paper",
    "Box Sticker / Label": "Sticker paper or label printer",
}
DEFAULT_FAQ = {
    "Getting Started": [
        (
            "What is PuzzleProof Studio?",
            "PuzzleProof Studio is a desktop production tool for managing artist approvals, puzzle project records, image exports, catalog data, and print-ready production documents.",
        ),
        (
            "What should I do first?",
            "Start in the Project tab, enter the artist and artwork details, confirm the approval status, then save the project before exporting images or printing documents.",
        ),
    ],
    "Licensing": [
        (
            "How does licensing work?",
            "PuzzleProof Studio uses an offline yearly license file. During Early Access, the app can fall back to the included sample license so testing is not blocked.",
        ),
        (
            "Where do I put license.json?",
            "Place a private license file at licenses/license.json. Do not share or commit private license files.",
        ),
    ],
    "Projects": [
        (
            "Where are project records saved?",
            "Saved project JSON files are stored under the jobs folder, with catalog metadata also written to catalog/catalog.json.",
        ),
        (
            "What is Manufacturing Ready?",
            "Manufacturing Ready means the project has the required approval, artwork, copyright owner, and export information needed before production.",
        ),
    ],
    "Catalog": [
        (
            "How do I find a saved project?",
            "Use the Catalog tab to search by artist name, artwork title, or catalog ID. Use Show All to reset filters.",
        ),
        (
            "Can multiple users edit the catalog at once?",
            "Not in this Early Access build. Catalog storage is local JSON, so treat it as a single-user workflow.",
        ),
    ],
    "Printing": [
        (
            "What does the Printing tab create?",
            "It creates print-ready HTML files for artist releases, copyright forms, production sheets, stickers, inserts, puzzle covers, and production packages.",
        ),
        (
            "Does it print directly to my printer?",
            "The current workflow creates print-ready files and opens folders for review. Native printer selection can be added later.",
        ),
    ],
    "Production Packages": [
        (
            "What is a production package?",
            "A production package generates the full set of print-ready production documents for the current project.",
        ),
        (
            "Where are production package files saved?",
            "Generated files are saved in the exports folder.",
        ),
    ],
    "Troubleshooting": [
        (
            "The app will not open. What should I check?",
            "Confirm Python and Tkinter are installed for source runs, or use the Windows packaged executable after it has been built and tested on Windows.",
        ),
        (
            "My export failed. What should I check?",
            "Confirm a source image is selected and that the image file still exists at the path shown in the Image Conversion tab.",
        ),
    ],
    "Support": [
        (
            "How do I contact support?",
            "Use Help > Contact Support, copy the Support tab information, and include the project steps that led to the problem.",
        ),
        (
            "Where do I report a bug?",
            "Use Help > Report Issue to open the GitHub issue tracker.",
        ),
    ],
}


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


def open_file(path):
    path = Path(path)
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(path))  # noqa: S606 - user-requested local file open
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except OSError as exc:
        messagebox.showwarning("Open File", f"Could not open file:\n{path}\n\n{exc}")


def configure_logging():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"puzzleproof-studio-{datetime.now():%Y%m%d-%H%M%S}.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.captureWarnings(True)
    LOGGER.info("Starting %s", APP_NAME)
    LOGGER.info("Version: %s", get_version())
    LOGGER.info("App folder: %s", ROOT_DIR)
    LOGGER.info("Resource folder: %s", RESOURCE_ROOT)
    LOGGER.info("Logs folder: %s", LOGS_DIR)
    return log_file


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
        self.root.geometry("1120x720")
        self.root.minsize(900, 560)
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
        style.configure("TButton", padding=(10, 5), background=THEME["green"], foreground=THEME["white"], bordercolor=THEME["green"], focusthickness=2, focuscolor=THEME["gold"])
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
        style.configure("TNotebook.Tab", padding=(14, 7), background=THEME["panel_alt"], foreground=THEME["text"], borderwidth=0)
        style.map(
            "TNotebook.Tab",
            background=[("selected", THEME["panel"]), ("active", "#E4D8C5")],
            foreground=[("selected", THEME["green"]), ("active", THEME["green"])],
        )
        style.configure("Treeview", background=THEME["white"], fieldbackground=THEME["white"], foreground=THEME["text"], rowheight=26)
        style.configure("Treeview.Heading", background=THEME["green"], foreground=THEME["white"], font=("TkDefaultFont", 10, "bold"))
        style.configure("Header.TFrame", background=THEME["green"])
        style.configure("HeaderTitle.TLabel", background=THEME["green"], foreground=THEME["gold"], font=("TkDefaultFont", 21, "bold"))
        style.configure("HeaderMeta.TLabel", background=THEME["green"], foreground=THEME["white"], font=("TkDefaultFont", 10))
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
        style.configure("SplashCream.TFrame", background=THEME["ivory"])
        style.configure("SplashFooter.TFrame", background=THEME["green"])
        style.configure("SplashTitle.TLabel", background=THEME["ivory"], foreground=THEME["green"], font=("TkDefaultFont", 28, "bold"))
        style.configure("SplashSubtitle.TLabel", background=THEME["ivory"], foreground=THEME["muted"], font=("TkDefaultFont", 12, "bold"))
        style.configure("SplashMeta.TLabel", background=THEME["ivory"], foreground=THEME["green"], font=("TkDefaultFont", 10, "bold"))
        style.configure("SplashText.TLabel", background=THEME["ivory"], foreground=THEME["text"])
        style.configure("SplashFooter.TLabel", background=THEME["green"], foreground=THEME["white"], font=("TkDefaultFont", 9))
        style.configure("SplashFooterMuted.TLabel", background=THEME["green"], foreground="#EADFCB", font=("TkDefaultFont", 9))
        style.configure("Splash.Horizontal.TProgressbar", troughcolor=THEME["panel_alt"], background=THEME["gold"], bordercolor=THEME["border"], lightcolor=THEME["gold"], darkcolor=THEME["gold"])
        style.configure("AboutTitle.TLabel", background=THEME["ivory"], foreground=THEME["green"], font=("TkDefaultFont", 16, "bold"))

    def _show_splash_then_main(self):
        self.splash = tk.Toplevel(self.root)
        self.splash.overrideredirect(True)
        self.splash.configure(bg=THEME["green"])
        self.splash.geometry("680x460")
        self.splash.update_idletasks()
        self._center_splash(680, 460)

        frame = ttk.Frame(self.splash, padding=8, style="Splash.TFrame")
        frame.pack(fill="both", expand=True)
        inner = ttk.Frame(frame, padding=(30, 24, 30, 0), style="SplashCream.TFrame")
        inner.pack(fill="both", expand=True)

        self._draw_splash_puzzle_icon(inner, size=112).pack(anchor="center", pady=(0, 12))
        ttk.Label(inner, text=APP_NAME, style="SplashTitle.TLabel").pack(anchor="center")
        ttk.Label(inner, text="Professional Puzzle Production Suite", style="SplashSubtitle.TLabel").pack(anchor="center", pady=(4, 0))

        badge = tk.Label(
            inner,
            text=self.display_version,
            bg=THEME["green"],
            fg=THEME["gold"],
            padx=14,
            pady=5,
            font=("TkDefaultFont", 9, "bold"),
        )
        badge.pack(anchor="center", pady=(14, 10))

        ttk.Label(inner, text=BRAND_LINE, style="SplashMeta.TLabel").pack(anchor="center")

        license_card = tk.Frame(inner, bg=THEME["panel"], highlightbackground=THEME["border"], highlightcolor=THEME["gold"], highlightthickness=1, bd=0)
        license_card.pack(anchor="center", fill="x", padx=64, pady=(16, 14))
        tk.Label(
            license_card,
            text="LICENSE STATUS",
            bg=THEME["panel"],
            fg=THEME["muted"],
            font=("TkDefaultFont", 8, "bold"),
        ).pack(anchor="center", pady=(10, 2))
        tk.Label(
            license_card,
            text=self.license_status.display,
            bg=THEME["panel"],
            fg=THEME["green"],
            font=("TkDefaultFont", 12, "bold"),
        ).pack(anchor="center", pady=(0, 10))

        self.splash_loading_text = tk.StringVar(value="Loading project tools...")
        ttk.Label(inner, textvariable=self.splash_loading_text, style="SplashText.TLabel").pack(anchor="center")
        progress = ttk.Progressbar(inner, mode="indeterminate", length=300, style="Splash.Horizontal.TProgressbar")
        progress.pack(anchor="center", pady=(8, 14))
        progress.start(14)

        footer_canvas = tk.Canvas(inner, height=58, bg=THEME["green"], highlightthickness=0, bd=0)
        footer_canvas.pack(fill="x", side="bottom")
        self._draw_bayou_footer(footer_canvas)
        footer = ttk.Frame(inner, padding=(12, 7), style="SplashFooter.TFrame")
        footer.pack(fill="x", side="bottom")
        ttk.Label(footer, text="BayouFinds / Wonder Piece Studio", style="SplashFooter.TLabel").pack(side="left")
        ttk.Label(footer, text=COPYRIGHT, style="SplashFooterMuted.TLabel").pack(side="right")

        self.root.after(800, lambda: self.splash_loading_text.set("Checking license and catalog..."))
        self.root.after(1500, lambda: self.splash_loading_text.set("Preparing production workspace..."))
        self.root.withdraw()
        self.root.after(2400, self._build_main_window)

    def _center_splash(self, width, height):
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = max(0, int((screen_width - width) / 2))
        y = max(0, int((screen_height - height) / 2))
        self.splash.geometry(f"{width}x{height}+{x}+{y}")

    def _draw_splash_puzzle_icon(self, parent, size=112):
        canvas = tk.Canvas(parent, width=size, height=size, bg=THEME["ivory"], highlightthickness=0, bd=0)
        pad = 10
        canvas.create_oval(pad, pad, size - pad, size - pad, fill=THEME["panel_alt"], outline=THEME["gold"], width=3)
        piece_left = size * 0.25
        piece_top = size * 0.30
        piece_right = size * 0.72
        piece_bottom = size * 0.76
        canvas.create_rectangle(piece_left, piece_top, piece_right, piece_bottom, fill=THEME["green"], outline=THEME["gold"], width=3)
        canvas.create_oval(size * 0.43, size * 0.18, size * 0.57, size * 0.34, fill=THEME["green"], outline=THEME["gold"], width=3)
        canvas.create_oval(size * 0.64, size * 0.47, size * 0.80, size * 0.61, fill=THEME["ivory"], outline=THEME["gold"], width=3)
        canvas.create_oval(size * 0.18, size * 0.48, size * 0.34, size * 0.62, fill=THEME["green"], outline=THEME["gold"], width=3)
        canvas.create_text(size * 0.49, size * 0.55, text="P", fill=THEME["gold"], font=("TkDefaultFont", 32, "bold"))
        return canvas

    def _draw_bayou_footer(self, canvas):
        def paint():
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            canvas.delete("all")
            canvas.create_rectangle(0, 0, width, height, fill=THEME["green"], outline="")
            canvas.create_polygon(0, height * 0.68, width * 0.20, height * 0.50, width * 0.42, height * 0.66, width * 0.64, height * 0.47, width, height * 0.64, width, height, 0, height, fill="#102724", outline="")
            for x in (width * 0.16, width * 0.52, width * 0.78):
                canvas.create_rectangle(x - 2, height * 0.26, x + 2, height * 0.74, fill="#102724", outline="")
                canvas.create_polygon(x, height * 0.12, x - 26, height * 0.44, x + 24, height * 0.44, fill="#102724", outline="")
            canvas.create_arc(-60, height * 0.38, width * 0.42, height * 1.18, start=18, extent=26, outline=THEME["gold"], width=2, style="arc")
            canvas.create_arc(width * 0.30, height * 0.44, width + 70, height * 1.24, start=18, extent=25, outline=THEME["gold"], width=2, style="arc")

        canvas.after_idle(paint)
        canvas.bind("<Configure>", lambda _event: paint())

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
        self._build_menu()

        container = ttk.Frame(self.root, padding=10, style="App.TFrame")
        container.pack(fill="both", expand=True)
        header = ttk.Frame(container, style="Header.TFrame", padding=(14, 10))
        header.pack(fill="x", pady=(0, 8))

        self._draw_brand_mark(header, size=54, background=THEME["green"]).pack(side="left", padx=(0, 12))

        title_group = ttk.Frame(header, style="Header.TFrame")
        title_group.pack(side="left", fill="x", expand=True)
        ttk.Label(title_group, text=BRAND_LINE.upper(), style="HeaderEyebrow.TLabel").pack(anchor="w")
        ttk.Label(title_group, text=APP_NAME, style="HeaderTitle.TLabel").pack(anchor="w", pady=(2, 0))
        ttk.Label(title_group, text=f"{SUBTITLE} | {self.display_version}", style="HeaderMeta.TLabel").pack(anchor="w", pady=(4, 0))
        ttk.Label(header, textvariable=self.license_text, style="License.TLabel").pack(side="right", padx=(16, 0))

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)
        self._build_project_tab(self.notebook)
        self._build_image_tab(self.notebook)
        self._build_catalog_tab(self.notebook)
        self._build_printing_tab(self.notebook)
        self._build_support_tab(self.notebook)
        self._build_about_tab(self.notebook)

        footer = ttk.Frame(container, style="Header.TFrame", padding=(8, 5))
        footer.pack(fill="x", pady=(8, 0))
        ttk.Label(footer, textvariable=self.status_text, style="Footer.TLabel").pack(side="left")
        ttk.Label(footer, textvariable=self.license_text, style="FooterMuted.TLabel").pack(side="left", padx=(18, 0))
        ttk.Label(footer, text=f"{WEBSITE} | {SUPPORT_EMAIL}", style="Footer.TLabel").pack(side="right")

    def _build_menu(self):
        menu_bar = tk.Menu(self.root)
        help_menu = tk.Menu(menu_bar, tearoff=False)
        help_menu.add_command(label="FAQ", command=self.show_faq_window)
        help_menu.add_separator()
        help_menu.add_command(label="Contact Support", command=self.contact_support)
        help_menu.add_command(label="Report Issue", command=lambda: self.open_link(BUG_REPORTS_URL))
        help_menu.add_command(label="Open Logs Folder", command=lambda: open_folder(LOGS_DIR))
        help_menu.add_separator()
        help_menu.add_command(label="Product Website", command=lambda: self.open_link(PRODUCT_WEBSITE))
        help_menu.add_command(label="Documentation", command=lambda: self.open_link(DOCUMENTATION_URL))
        help_menu.add_separator()
        help_menu.add_command(label="About PuzzleProof Studio", command=self.show_about_tab)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menu_bar)

    def open_link(self, url):
        try:
            webbrowser.open(url, new=2)
            self.status_text.set(f"Opened: {url}")
        except Exception as exc:  # noqa: BLE001 - GUI should report and continue
            messagebox.showwarning("Open Link", f"Could not open link:\n{url}\n\n{exc}")

    def contact_support(self):
        subject = "PuzzleProof Studio Support"
        body = f"Version: {self.display_version}%0D%0ALicense: {self.license_status.display}%0D%0A"
        self.open_link(f"mailto:{SUPPORT_EMAIL}?subject={subject.replace(' ', '%20')}&body={body}")

    def show_about_tab(self):
        if hasattr(self, "notebook"):
            self.notebook.select(5)
            self.status_text.set("About PuzzleProof Studio opened.")

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

    def _add_scrollable_tab(self, notebook, title, padding=10):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=title)
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)

        canvas = tk.Canvas(tab, bg=THEME["ivory"], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        content = ttk.Frame(canvas, padding=padding, style="App.TFrame")
        content_id = canvas.create_window((0, 0), window=content, anchor="nw")

        def refresh_scroll_region(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_content(event):
            canvas.itemconfigure(content_id, width=event.width)

        def on_mousewheel(event):
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
            else:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def bind_wheel(_event):
            canvas.bind_all("<MouseWheel>", on_mousewheel)
            canvas.bind_all("<Button-4>", on_mousewheel)
            canvas.bind_all("<Button-5>", on_mousewheel)

        def unbind_wheel(_event):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        content.bind("<Configure>", refresh_scroll_region)
        canvas.bind("<Configure>", resize_content)
        canvas.bind("<Enter>", bind_wheel)
        canvas.bind("<Leave>", unbind_wheel)
        return content

    def load_faq_content(self):
        if not FAQ_SOURCE_FILE.exists():
            return DEFAULT_FAQ

        categories = {}
        current_category = None
        current_question = None
        answer_lines = []

        def flush_question():
            if current_category and current_question:
                answer = "\n".join(answer_lines).strip()
                categories.setdefault(current_category, []).append((current_question, answer or "No answer has been added yet."))

        for raw_line in FAQ_SOURCE_FILE.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line.startswith("## "):
                flush_question()
                current_category = line[3:].strip()
                current_question = None
                answer_lines = []
                categories.setdefault(current_category, [])
            elif line.startswith("### "):
                flush_question()
                current_question = line[4:].strip()
                answer_lines = []
            elif current_question:
                answer_lines.append(raw_line)
        flush_question()

        return categories or DEFAULT_FAQ

    def show_faq_window(self):
        faq = self.load_faq_content()
        window = tk.Toplevel(self.root)
        window.title("PuzzleProof Studio FAQ")
        window.geometry("820x560")
        window.minsize(720, 480)
        window.configure(bg=THEME["ivory"])
        window.transient(self.root)

        header = ttk.Frame(window, padding=(16, 14), style="Header.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text="Help Center", style="HeaderTitle.TLabel").pack(anchor="w")
        ttk.Label(header, text="PuzzleProof Studio FAQ and customer support links", style="HeaderMeta.TLabel").pack(anchor="w", pady=(3, 0))

        body = ttk.Frame(window, padding=14)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        category_frame = self._card(body, padding=10)
        category_frame.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        ttk.Label(category_frame, text="Categories", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))
        category_list = tk.Listbox(
            category_frame,
            height=16,
            width=24,
            bg=THEME["white"],
            fg=THEME["text"],
            selectbackground=THEME["green"],
            selectforeground=THEME["white"],
            highlightthickness=1,
            highlightbackground=THEME["border"],
            bd=0,
            activestyle="none",
        )
        category_list.pack(fill="both", expand=True)

        answer_frame = self._card(body, padding=12)
        answer_frame.grid(row=0, column=1, sticky="nsew")
        answer_frame.rowconfigure(0, weight=1)
        answer_frame.columnconfigure(0, weight=1)
        text = tk.Text(
            answer_frame,
            wrap="word",
            bg=THEME["panel"],
            fg=THEME["text"],
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=8,
            font=("TkDefaultFont", 10),
        )
        text.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(answer_frame, orient="vertical", command=text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text.configure(yscrollcommand=scrollbar.set)
        text.tag_configure("question", foreground=THEME["green"], font=("TkDefaultFont", 11, "bold"), spacing1=8)
        text.tag_configure("answer", foreground=THEME["text"], spacing3=10)

        def render_category(category):
            text.configure(state="normal")
            text.delete("1.0", "end")
            for question, answer in faq.get(category, []):
                text.insert("end", f"{question}\n", "question")
                text.insert("end", f"{answer.strip()}\n\n", "answer")
            text.configure(state="disabled")

        def on_select(_event=None):
            selection = category_list.curselection()
            if selection:
                render_category(category_list.get(selection[0]))

        for category in faq:
            category_list.insert("end", category)
        category_list.bind("<<ListboxSelect>>", on_select)
        if faq:
            category_list.selection_set(0)
            render_category(next(iter(faq)))

        links = ttk.Frame(window, padding=(14, 0, 14, 14))
        links.pack(fill="x")
        ttk.Button(links, text="Product Website", command=lambda: self.open_link(PRODUCT_WEBSITE), style="Secondary.TButton").pack(side="left")
        ttk.Button(links, text="BayouFinds", command=lambda: self.open_link(BAYOUFINDS_WEBSITE), style="Secondary.TButton").pack(side="left", padx=(8, 0))
        ttk.Button(links, text="GitHub Repository", command=lambda: self.open_link(GITHUB_REPOSITORY), style="Secondary.TButton").pack(side="left", padx=(8, 0))
        ttk.Button(links, text="Bug Reports", command=lambda: self.open_link(BUG_REPORTS_URL)).pack(side="right")
        self.status_text.set("FAQ opened.")

    def _build_project_tab(self, notebook):
        tab = self._add_scrollable_tab(notebook, "Project", padding=10)
        form = ttk.LabelFrame(tab, text="Project Details", padding=10)
        form.pack(fill="x")

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
            height=4,
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

        ttk.Label(tab, text="Required before manufacturing: approved status, source artwork, copyright owner, and at least one export.", style="Muted.TLabel").pack(anchor="w", pady=(8, 0))

        buttons = ttk.Frame(tab)
        buttons.pack(fill="x", pady=(12, 18))
        project_actions = (
            ("New Project", self.new_project),
            ("Save Project", lambda: self.save_project(show_confirmation=True)),
            ("Send Project to Catalog", self.send_project_to_catalog),
            ("Open Project Folder", lambda: open_folder(self.current_project_folder())),
            ("Generate Artist Release", lambda: self.generate_print_document("Artist Release")),
            ("Mark Manufacturing Ready", self.mark_manufacturing_ready),
        )
        for index, (label, command) in enumerate(project_actions):
            row = index // 3
            column = index % 3
            ttk.Button(buttons, text=label, command=command).grid(row=row, column=column, sticky="ew", padx=(0 if column == 0 else 6, 0), pady=2)
        for column in range(3):
            buttons.columnconfigure(column, weight=1)
        ttk.Frame(tab, height=12).pack(fill="x")

    def _build_image_tab(self, notebook):
        tab = self._add_scrollable_tab(notebook, "Image Conversion", padding=10)

        source = ttk.LabelFrame(tab, text="Source Artwork", padding=10)
        source.pack(fill="x")
        ttk.Entry(source, textvariable=self.source_image).pack(side="left", fill="x", expand=True)
        ttk.Button(source, text="Import Artwork", command=self.import_artwork).pack(side="left", padx=(8, 0))

        options = ttk.LabelFrame(tab, text="Export Options", padding=10)
        options.pack(fill="x", pady=10)
        self.export_type = tk.StringVar(value="Puzzle Print")
        self.export_format = tk.StringVar(value="DOCX")
        self.last_output_preset = tk.StringVar(value="Selected output preset: Puzzle Print")
        self.last_output_format = tk.StringVar(value="Output format: DOCX")
        self.last_output_path = tk.StringVar(value="Saved file path: Not exported yet")
        self.last_output_printer = tk.StringVar(value=f"Suggested printer: {PRINTER_GUIDANCE['Puzzle Print']}")
        self.last_output_file = None
        self.copyright_text = tk.StringVar(value=DEFAULT_COPYRIGHT_TEXT)
        self.placement = tk.StringVar(value="Bottom Right")
        self.font_size = tk.IntVar(value=42)
        self.opacity = tk.IntVar(value=180)

        rows = (
            ("Output Preset", ttk.Combobox(options, textvariable=self.export_type, values=tuple(EXPORT_TARGETS.keys()), state="readonly")),
            ("Output Format", ttk.Combobox(options, textvariable=self.export_format, values=OUTPUT_FORMATS, state="readonly")),
            ("Copyright Text", ttk.Entry(options, textvariable=self.copyright_text)),
            ("Placement", ttk.Combobox(options, textvariable=self.placement, values=PLACEMENTS, state="readonly")),
            ("Font Size", ttk.Spinbox(options, from_=14, to=96, textvariable=self.font_size)),
            ("Opacity", ttk.Spinbox(options, from_=40, to=255, textvariable=self.opacity)),
        )
        for row, (label, widget) in enumerate(rows):
            ttk.Label(options, text=label).grid(row=row, column=0, sticky="w", pady=4)
            widget.grid(row=row, column=1, sticky="ew", pady=4, padx=(10, 0))
        options.columnconfigure(1, weight=1)

        self.export_type.trace_add("write", self.update_export_summary)
        self.export_format.trace_add("write", self.update_export_summary)

        ttk.Button(tab, text="Apply Preset Crop/Resize and Export", command=self.export_image).pack(anchor="w")
        summary = ttk.LabelFrame(tab, text="Latest Output", padding=10)
        summary.pack(fill="x", pady=(10, 0))
        ttk.Label(summary, textvariable=self.last_output_preset).pack(anchor="w")
        ttk.Label(summary, textvariable=self.last_output_format).pack(anchor="w", pady=(3, 0))
        ttk.Label(summary, textvariable=self.last_output_printer).pack(anchor="w", pady=(3, 0))
        ttk.Label(summary, textvariable=self.last_output_path, wraplength=820, justify="left").pack(anchor="w", pady=(3, 8))
        ttk.Button(summary, text="Open Output Folder", command=self.open_latest_output_folder).pack(anchor="w")
        self.sample_label = ttk.Label(tab, text=self.sample_artwork_status(), padding=(0, 12, 0, 0))
        self.sample_label.pack(anchor="w")

    def _build_catalog_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text="Catalog")
        search = ttk.LabelFrame(tab, text="Search Catalog", padding=10)
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
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill="both", expand=True, pady=10)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        self.catalog_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=9)
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
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.catalog_tree.yview)
        self.catalog_tree.configure(yscrollcommand=tree_scroll.set)
        self.catalog_tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll.grid(row=0, column=1, sticky="ns")
        ttk.Button(tab, text="Refresh Catalog", command=self.refresh_catalog).pack(anchor="w")
        self.refresh_catalog()

    def _build_printing_tab(self, notebook):
        tab = self._add_scrollable_tab(notebook, "Printing", padding=10)
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=0)
        tab.rowconfigure(1, weight=1)

        intro = self._card(tab, padding=(12, 10))
        intro.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        ttk.Label(intro, text="Printing Command Center", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            intro,
            text="Create print-ready HTML files for production records, artist paperwork, packaging inserts, and release handoff.",
            style="CardMuted.TLabel",
            wraplength=820,
            justify="left",
        ).pack(anchor="w", pady=(5, 0))

        actions = ttk.Frame(tab)
        actions.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
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
            card.grid(row=row, column=column, sticky="nsew", padx=(0 if column == 0 else 8, 0), pady=(0, 8))
            actions.rowconfigure(row, weight=1)

        sidebar = ttk.Frame(tab)
        sidebar.grid(row=1, column=1, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)

        self._build_info_panel(
            sidebar,
            "Output Location",
            f"Generated files are saved in:\n{EXPORTS_DIR}",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self._build_info_panel(
            sidebar,
            "Before You Print",
            "Confirm approval status, copyright owner, source artwork, and export files before packaging.",
        ).grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self._build_info_panel(
            sidebar,
            "License Status",
            self.license_status.display,
        ).grid(row=2, column=0, sticky="ew", pady=(0, 8))

        package = self._card(sidebar, padding=10)
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
        tab = self._add_scrollable_tab(notebook, "Support", padding=10)
        self.support_info = build_support_info(self.license_status)
        ttk.Label(tab, text=format_support_info(self.support_info), justify="left").pack(anchor="w")
        buttons = ttk.Frame(tab)
        buttons.pack(anchor="w", pady=16)
        ttk.Button(buttons, text="Open Logs Folder", command=lambda: open_folder(LOGS_DIR)).pack(side="left")
        ttk.Button(buttons, text="Open Project Folder", command=lambda: open_folder(JOBS_DIR)).pack(side="left", padx=8)
        ttk.Button(buttons, text="Copy Support Info", command=self.copy_support_info).pack(side="left")

    def _build_about_tab(self, notebook):
        tab = self._add_scrollable_tab(notebook, "About", padding=12)
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
        if hasattr(self, "last_output_path"):
            self.last_output_path.set("Saved file path: Not exported yet")
            self.last_output_file = None
            self.update_export_summary()
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

    def send_project_to_catalog(self):
        project = self.save_project()
        self.status_text.set(f"Project sent to catalog: {project.get('catalog_number', '')}")
        messagebox.showinfo(
            "Catalog Updated",
            "Project added to catalog:\n"
            f"{project.get('catalog_number', '')}\n\n"
            f"Catalog file:\n{self.catalog.catalog_file}",
        )
        self.notebook.select(2)
        self.refresh_catalog()

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

    def update_export_summary(self, *_args):
        if not hasattr(self, "last_output_preset"):
            return
        preset = self.export_type.get()
        self.last_output_preset.set(f"Selected output preset: {preset}")
        self.last_output_format.set(f"Output format: {self.export_format.get()}")
        self.last_output_printer.set(f"Suggested printer: {PRINTER_GUIDANCE.get(preset, 'Review output preset')}")

    def open_latest_output_folder(self):
        if self.last_output_file:
            open_folder(Path(self.last_output_file).parent)
            return
        open_folder(EXPORTS_DIR)

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
        preset = self.export_type.get()
        output_format = self.export_format.get()
        suggested_printer = PRINTER_GUIDANCE.get(preset, "Review output preset")
        self.last_output_file = output_path
        self.last_output_path.set(f"Saved file path: {output_path}")
        self.update_export_summary()
        self.save_project()
        self.status_text.set(f"Export created: {output_path}")
        messagebox.showinfo(
            "Export Created",
            "Export created:\n"
            f"{preset}\n"
            f"Format: {output_format}\n"
            f"Saved to: {output_path}\n"
            f"Suggested printer: {suggested_printer}",
        )

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
        open_file(path)

    def generate_production_package(self):
        project = self.save_project()
        paths = self.printing.create_production_package(project)
        self.status_text.set(f"Production package created with {len(paths)} files.")
        messagebox.showinfo("Printing", f"Created {len(paths)} print-ready files in:\n{EXPORTS_DIR}")
        open_folder(EXPORTS_DIR)

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
    ensure_app_dirs()
    log_file = configure_logging()
    if tk is None:
        LOGGER.error("Tkinter is not available.")
        print(
            "PuzzleProof Studio requires Tkinter. On Fedora, install it with: sudo dnf install python3-tkinter",
            file=sys.stderr,
        )
        sys.exit(1)
    root = tk.Tk()

    def report_callback_exception(exc_type, exc_value, exc_traceback):
        LOGGER.exception("Unhandled Tkinter exception", exc_info=(exc_type, exc_value, exc_traceback))
        messagebox.showerror(
            "PuzzleProof Studio Error",
            f"An unexpected error occurred. Details were saved to:\n{log_file}",
        )

    root.report_callback_exception = report_callback_exception
    PuzzleProofApp(root)
    try:
        root.mainloop()
    except Exception:
        LOGGER.exception("Unhandled application exception")
        raise
    finally:
        LOGGER.info("PuzzleProof Studio closed.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.getLogger(__name__).exception("Fatal startup error")
        raise

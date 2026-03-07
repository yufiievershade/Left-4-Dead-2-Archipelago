"""Tkinter GUI for L4D2 Archipelago Companion.

Provides a graphical interface for connecting to Archipelago servers.
"""

import tkinter as tk
from collections.abc import Callable
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

from l4d2_companion.config import CAMPAIGN_NAMES
from pydantic import BaseModel, Field


class ThemeConfiguration(BaseModel):
    """Configuration for GUI themes (light/dark)."""

    name: str
    background_color: str
    foreground_color: str
    text_background: str = "#ffffff"
    text_foreground: str = "#000000"
    button_bg: str = "#e0e0e0"
    accent_color: str = "#007acc"

    class Config:
        frozen = True


class WindowConfiguration(BaseModel):
    """Window settings configuration."""

    title: str = "L4D2 AP Companion Client"
    width: int = 800
    height: int = 700
    min_width: int = 600
    min_height: int = 500
    resizable_x: bool = True
    resizable_y: bool = True


class ConnectionInfo(BaseModel):
    """Connection information from GUI inputs."""

    host: str
    slot: str
    password: str = Field(default="", description="Optional server password")

    def is_valid(self) -> tuple[bool, str]:
        """Validate connection info.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.host.strip():
            return False, "Host is required"
        if not self.slot.strip():
            return False, "Slot name is required"
        return True, ""


class L4D2CompanionGUI(tk.Tk):
    """Main GUI window for the L4D2 Archipelago Companion."""

    def __init__(self, l4d2_paths: list[Path]):
        super().__init__()

        self.l4d2_paths = l4d2_paths
        self.is_dark = False
        self.connected = False
        self.on_connect: Callable[[str, str, str], None] | None = None
        self.on_disconnect: Callable[[], None] | None = None

        self._setup_window()
        self._setup_styles()
        self._create_widgets()

    def _setup_window(self) -> None:
        """Configure main window properties using Pydantic model."""
        config = WindowConfiguration()
        self.title(config.title)
        self.geometry(f"{config.width}x{config.height}")
        self.minsize(config.min_width, config.min_height)
        if not config.resizable_x:
            self.resizable(False, config.resizable_y)
        elif not config.resizable_y:
            self.resizable(config.resizable_x, False)
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def _setup_styles(self) -> None:
        """Configure ttk styles."""
        # Light theme (default)
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0")
        self.style.configure("TButton", padding=5)

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_input_section(main_frame)
        self._create_button_section(main_frame)
        self._create_notebook(main_frame)
        self._create_status_section(main_frame)

    def _create_input_section(self, parent: ttk.Frame) -> None:
        """Create connection input fields."""
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Host
        ttk.Label(input_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.host_entry = ttk.Entry(input_frame, width=40)
        self.host_entry.grid(row=0, column=1, sticky=tk.EW)
        self.host_entry.insert(0, "archipelago.gg:38281")

        # Slot Name
        ttk.Label(input_frame, text="Slot Name:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0)
        )
        self.slot_entry = ttk.Entry(input_frame, width=40)
        self.slot_entry.grid(row=1, column=1, sticky=tk.EW, pady=(5, 0))

        # Password
        ttk.Label(input_frame, text="Password:").grid(
            row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0)
        )
        self.password_entry = ttk.Entry(input_frame, width=40, show="*")
        self.password_entry.grid(row=2, column=1, sticky=tk.EW, pady=(5, 0))

        input_frame.columnconfigure(1, weight=1)

    def _create_button_section(self, parent: ttk.Frame) -> None:
        """Create action buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        self.connect_button = ttk.Button(
            button_frame, text="Connect", command=self._on_connect_clicked
        )
        self.connect_button.pack(side=tk.LEFT, padx=(0, 5))

        self.disconnect_button = ttk.Button(
            button_frame, text="Disconnect", command=self._on_disconnect_clicked, state=tk.DISABLED
        )
        self.disconnect_button.pack(side=tk.LEFT)

        self.theme_button = ttk.Button(
            button_frame, text="Toggle Theme", command=self._toggle_theme
        )
        self.theme_button.pack(side=tk.LEFT, padx=(5, 0))

    def _create_notebook(self, parent: ttk.Frame) -> None:
        """Create tabbed notebook."""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self._create_log_tab()
        self._create_campaigns_tab()

    def _create_log_tab(self) -> None:
        """Create log output tab."""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Log")

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=20, width=70, state=tk.DISABLED, wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure tags for colored text
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("info", foreground="blue")
        self.log_text.tag_config("item", foreground="purple")

    def _create_campaigns_tab(self) -> None:
        """Create campaigns display tab."""
        campaigns_frame = ttk.Frame(self.notebook)
        self.notebook.add(campaigns_frame, text="Campaigns")

        campaigns_inner = ttk.Frame(campaigns_frame, padding="10")
        campaigns_inner.pack(fill=tk.BOTH, expand=True)

        # Create campaign status labels
        self.campaign_labels: dict[str, ttk.Label] = {}

        for i, campaign in enumerate(CAMPAIGN_NAMES):
            label = ttk.Label(campaigns_inner, text=f"❌ {campaign}", font=("TkDefaultFont", 10))
            label.grid(row=i % 7, column=i // 7, sticky=tk.W, padx=10, pady=2)
            self.campaign_labels[campaign] = label

    def _create_status_section(self, parent: ttk.Frame) -> None:
        """Create status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X)

        self.status_label = ttk.Label(
            status_frame, text=f"L4D2 paths: {len(self.l4d2_paths)} found", relief=tk.SUNKEN
        )
        self.status_label.pack(fill=tk.X)

    def _on_connect_clicked(self) -> None:
        """Handle connect button click with Pydantic validation."""
        conn_info = ConnectionInfo(
            host=self.host_entry.get().strip(),
            slot=self.slot_entry.get().strip(),
            password=self.password_entry.get().strip(),
        )

        is_valid, error_msg = conn_info.is_valid()
        if not is_valid:
            messagebox.showerror("Error", error_msg)
            return

        self.connected = True
        self.connect_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.NORMAL)

        if self.on_connect:
            self.on_connect(conn_info.host, conn_info.slot, conn_info.password)

    def _on_disconnect_clicked(self) -> None:
        """Handle disconnect button click."""
        self.connected = False
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)

        if self.on_disconnect:
            self.on_disconnect()

    # Theme configurations as class variables
    THEME_LIGHT = ThemeConfiguration(
        name="light",
        background_color="#f0f0f0",
        foreground_color="#000000",
    )
    THEME_DARK = ThemeConfiguration(
        name="dark",
        background_color="#2d2d2d",
        foreground_color="#ffffff",
    )

    def _toggle_theme(self) -> None:
        """Toggle between light and dark themes using Pydantic models."""
        self.is_dark = not self.is_dark
        theme = self.THEME_DARK if self.is_dark else self.THEME_LIGHT

        self.configure(bg=theme.background_color)
        self.style.configure("TFrame", background=theme.background_color)
        self.style.configure(
            "TLabel", background=theme.background_color, foreground=theme.foreground_color
        )

    def log_message(self, message: str, tag: str = "info") -> None:
        """Add a message to the log.

        Args:
            message: Message text to log
            tag: Tag for styling (error, success, info, item)
        """
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_campaign_status(self, campaign: str, unlocked: bool) -> None:
        """Update the display status of a campaign.

        Args:
            campaign: Campaign name
            unlocked: Whether the campaign is unlocked
        """
        if campaign in self.campaign_labels:
            label = self.campaign_labels[campaign]
            if unlocked:
                label.config(text=f"✅ {campaign}", foreground="green")
            else:
                label.config(text=f"❌ {campaign}", foreground="red")

    def set_connect_callback(self, callback: Callable[[str, str, str], None]) -> None:
        """Set the callback for when connect is clicked.

        Args:
            callback: Function(host, slot, password) to call
        """
        self.on_connect = callback

    def set_disconnect_callback(self, callback: Callable[[], None]) -> None:
        """Set the callback for when disconnect is clicked.

        Args:
            callback: Function() to call
        """
        self.on_disconnect = callback

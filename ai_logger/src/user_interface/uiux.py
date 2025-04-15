import json
from rich.console import Console, ConsoleOptions, RenderResult
from rich.live import Live
from rich.markdown import CodeBlock, Markdown
from rich.syntax import Syntax
from rich.text import Text
from rich.theme import Theme
from rich.panel import Panel
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.status import Status
from contextlib import contextmanager

class CyberpunkUI:
    def __init__(self):
        self.theme, self.colors = self._create_cyberpunk_theme()
        self._setup_prettier_code_blocks()
        self.console = Console(theme=self.theme, emoji=True, emoji_variant="emoji")
        self.live = Live(console=self.console, auto_refresh=False)
        self.live_active = False
        self.last_content = None  # Store the last displayed content
    
    def _create_cyberpunk_theme(self):
        # Cyberpunk color palette
        cyberpunk_colors = {
            "neon_pink": "#FF00FF",
            "electric_blue": "#00FFFF",
            "acid_green": "#39FF14",
            "cyber_yellow": "#FFD300",
            "digital_purple": "#9A00FF",
            "terminal_green": "#00FF41",
            "hacker_red": "#FF3131"
        }

        # Create cyberpunk theme
        cyberpunk_theme = Theme({
            "info": f"bold {cyberpunk_colors['terminal_green']}",
            "warning": f"bold {cyberpunk_colors['cyber_yellow']}",
            "danger": f"bold {cyberpunk_colors['hacker_red']}",
            "prompt": f"bold {cyberpunk_colors['neon_pink']}",
            "header": f"bold {cyberpunk_colors['electric_blue']}",
            "success": f"bold {cyberpunk_colors['acid_green']}",
            "highlight": f"bold {cyberpunk_colors['digital_purple']}",
            "default": "white",
        })
        return cyberpunk_theme, cyberpunk_colors
    
    def _setup_prettier_code_blocks(self):
        """Make rich code blocks prettier and easier to copy."""
        class SimpleCodeBlock(CodeBlock):
            def __rich_console__(
                self, console: Console, options: ConsoleOptions
            ) -> RenderResult:
                code = str(self.text).rstrip()
                yield Text(self.lexer_name, style='dim')
                yield Syntax(
                    code,
                    self.lexer_name,
                    theme=self.theme,
                    background_color='default',
                    word_wrap=True,
                )
                yield Text(f'/{self.lexer_name}', style='dim')

        Markdown.elements['fence'] = SimpleCodeBlock
    
    def start_live(self):
        """Start the live display if not already active"""
        if not self.live_active:
            self.live.start()
            self.live_active = True
            # Restore previous content if available
            if self.last_content:
                self.live.update(self.last_content)
                self.live.refresh()
    
    def stop_live(self):
        """Stop the live display if active"""
        if self.live_active:
            self.live.stop()
            self.live_active = False
    
    def print(self, message, style="info"):
        """Print with cyberpunk styling"""
        formatted_message = f"[{style}]{message}[/{style}]"
        self.last_content = formatted_message  # Store content for restoration
        
        if self.live_active:
            self.live.update(formatted_message)
            self.live.refresh()
        else:
            self.console.print(formatted_message)
    
    def display_json(self, data, title=None):
        """Safely display JSON data in cyberpunk style"""
        json_theme = "dracula"
        
        # Process title if provided
        if title:
            title_panel = Panel(f"[header]>>> {title.upper()} <<<[/header]")
            self.last_content = title_panel  # Store content for restoration
            
            if self.live_active:
                self.live.update(title_panel)
                self.live.refresh()
            else:
                self.console.print(title_panel)
        
        # Check if data is already a string
        panel = None  # Initialize panel variable
        
        if isinstance(data, str):
            try:
                # Try to parse to ensure it's valid JSON
                panel = Panel(Syntax(data, "json", theme=json_theme, background_color="default"))
            except json.JSONDecodeError:
                try:
                    # Try to parse and then format as JSON
                    parsed_data = json.loads(data)
                    json_str = json.dumps(parsed_data, indent=4)
                    panel = Panel(Syntax(json_str, "json", theme=json_theme, background_color="default"))
                except json.JSONDecodeError:
                    # If not valid JSON, display as text
                    panel = Panel(Text(data))
        else:
            # Convert Python object to JSON string
            json_str = json.dumps(data, indent=4)
            panel = Panel(Syntax(json_str, "json", theme=json_theme, background_color="default"))
        
        # Store and display the panel if created
        if panel:
            self.last_content = panel  # Store content for restoration
            if self.live_active:
                self.live.update(panel)
                self.live.refresh()
            else:
                self.console.print(panel)
    
    def display_header(self, title, subtitle=None):
        """Display a cyberpunk-styled header"""
        header_text = f"[header]>>> {title.upper()} <<<[/header]"
        panel = None  # Initialize panel variable
        
        if subtitle:
            if isinstance(subtitle, (dict, list)):
                # Display header and then JSON separately
                panel = Panel(header_text, border_style=self.colors["neon_pink"])
                self.last_content = panel  # Store content for restoration
                
                if self.live_active:
                    self.live.update(panel)
                    self.live.refresh()
                else:
                    self.console.print(panel)
                self.display_json(subtitle)
                return
            elif isinstance(subtitle, str) and (subtitle.startswith("{") or subtitle.startswith("[")):
                # Handle JSON strings
                panel = Panel(header_text, border_style=self.colors["neon_pink"])
                self.last_content = panel  # Store content for restoration
                
                if self.live_active:
                    self.live.update(panel)
                    self.live.refresh()
                else:
                    self.console.print(panel)
                try:
                    # Try to parse and display as JSON
                    self.display_json(subtitle)
                    return
                except json.JSONDecodeError:
                    # If not valid JSON, display as escaped text
                    json_panel = Panel(Text(subtitle), border_style=self.colors["highlight"])
                    self.last_content = json_panel  # Store content for restoration
                    
                    if self.live_active:
                        self.live.update(json_panel)
                        self.live.refresh()
                    else:
                        self.console.print(json_panel)
                    return
            else:
                header_text += f"\n[highlight]{escape(str(subtitle))}[/highlight]"
        
        panel = Panel(header_text, border_style=self.colors["neon_pink"])
        self.last_content = panel  # Store content for restoration
        
        if self.live_active:
            self.live.update(panel)
            self.live.refresh()
        else:
            self.console.print(panel)
    
    @contextmanager
    def spinner(self, message: str, spinner_type: str = None):
        """
        Display a spinner with a message during a long-running operation.
        
        Args:
            message: The message to display alongside the spinner
            spinner_type: The type of spinner to display (dots, dots2, dots3, etc.)
        """
        # Import here to avoid circular import
        from config import CONFIG, get_spinner_type
        
        # Use provided spinner type or get from config
        if spinner_type is None:
            spinner_type = get_spinner_type()
        
        # Check if loading animations are enabled in config
        if not CONFIG.ui.loading_animation:
            # Simple non-animation fallback with no output
            try:
                yield None
            finally:
                pass
            return
        
        spinner_style = self.colors["electric_blue"]
        message_style = self.colors["terminal_green"]
        
        # Save the current content before stopping live
        saved_content = self.last_content
        
        # Use progress bar style for AI agent operations
        if "AI agent" in message or "agent" in message.lower():
            # Make sure any Live display is stopped before starting Progress
            was_live_active = self.live_active
            if was_live_active:
                self.stop_live()
                
            with Progress(
                TextColumn(f"[{message_style}]{message}[/{message_style}]"),
                BarColumn(complete_style=self.colors["acid_green"]),
                console=self.console
            ) as progress:
                task = progress.add_task("", total=None)
                try:
                    yield progress
                finally:
                    progress.stop()
                    # Add a blank line after the progress bar is done
                    self.console.print()
                    
                    # Restore the saved content and restart Live if it was active before
                    if saved_content:
                        self.last_content = saved_content
                        
                    if was_live_active:
                        self.start_live()
        else:
            # Use spinner for other operations
            # Make sure any Live display is stopped before starting Status
            was_live_active = self.live_active
            if was_live_active:
                self.stop_live()
                
            with Status(f"[{spinner_style}][[/{spinner_style}][{message_style}]{message}[/{message_style}][{spinner_style}]][/{spinner_style}]", 
                    spinner=spinner_type, spinner_style=spinner_style, console=self.console) as status:
                try:
                    yield status
                finally:
                    status.stop()
                    # Add a blank line after the spinner is done
                    self.console.print()
                    
                    # Restore the saved content and restart Live if it was active before
                    if saved_content:
                        self.last_content = saved_content
                        
                    if was_live_active:
                        self.start_live()
    
    @contextmanager
    def progress(self, total: int, description: str = "Processing"):
        """
        Display a progress bar for a task with known total steps.
        
        Args:
            total: The total number of steps to complete
            description: Description of the task being performed
        """
        # Import here to avoid circular import
        from config import CONFIG, get_spinner_type
        
        # Save the current content before potentially stopping live
        saved_content = self.last_content
        
        # Check if loading animations are enabled in config
        if not CONFIG.ui.loading_animation:
            # Simple non-animation fallback
            progress_message = f"[info]{description} (0/{total})[/info]"
            self.last_content = progress_message  # Store content for restoration
            
            if self.live_active:
                self.live.update(progress_message)
                self.live.refresh()
            else:
                self.console.print(progress_message)
            
            count = 0
            
            def update(n=1):
                nonlocal count
                count += n
                if count % max(1, total // 10) == 0 or count >= total:  # Print status at 10% intervals
                    current_message = f"[info]{description} ({count}/{total})[/info]"
                    self.last_content = current_message  # Store content for restoration
                    
                    if self.live_active:
                        self.live.update(current_message)
                        self.live.refresh()
                    else:
                        self.console.print(current_message)
            
            try:
                yield update
            finally:
                final_message = f"[info]{description} completed ({total}/{total})[/info]"
                self.last_content = final_message  # Store content for restoration
                
                if self.live_active:
                    self.live.update(final_message)
                    self.live.refresh()
                else:
                    self.console.print(final_message)
            return
        
        progress_style = self.colors["acid_green"]
        desc_style = self.colors["terminal_green"]
        time_style = self.colors["cyber_yellow"]
        spinner_type = get_spinner_type()
        
        # Make sure any Live display is stopped before starting Progress
        was_live_active = self.live_active
        if was_live_active:
            self.stop_live()
            
        with Progress(
            SpinnerColumn(spinner_name=spinner_type, style=self.colors["electric_blue"]),
            TextColumn(f"[{desc_style}]{description}[/{desc_style}]"),
            BarColumn(complete_style=progress_style),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task(description, total=total)
            try:
                yield lambda n=1: progress.update(task, advance=n)
            finally:
                # Restore the saved content and restart Live if it was active before
                if saved_content:
                    self.last_content = saved_content
                    
                if was_live_active:
                    self.start_live()
    
    def indeterminate_progress(self, description: str = "Processing..."):
        """Create an indeterminate progress bar for tasks with unknown duration."""
        # Import here to avoid circular import
        from config import CONFIG, get_spinner_type
        
        # Check if loading animations are enabled
        if not CONFIG.ui.loading_animation:
            progress_message = f"[info]{description}[/info]"
            self.last_content = progress_message  # Store content for restoration
            
            if self.live_active:
                self.live.update(progress_message)
                self.live.refresh()
            else:
                self.console.print(progress_message)
            return None
        
        spinner_type = get_spinner_type()
        
        return Progress(
            SpinnerColumn(spinner_name=spinner_type, style=self.colors["electric_blue"]),
            TextColumn(f"[{self.colors['terminal_green']}]{description}[/]"),
            console=self.console
        )


# Initialize the UI
ui = CyberpunkUI()

__all__ = ["ui"]
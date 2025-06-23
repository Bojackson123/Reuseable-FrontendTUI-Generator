from typing import TypedDict, Callable, Optional, List, Any, Dict
import os
import sys

class Option(TypedDict, total=False):
    """Class that controls the formatting of each option in the options list"""
    label: str                               # Display label for the TUI
    function: Callable                       # The function to call
    args: Optional[List[Any]]                # Static positional arguments (optional)
    kwargs: Optional[Dict[str, Any]]         # Static keyword arguments (optional)
    prompt_args: Optional[List[str]]         # Prompts for runtime positional args (optional)

class FrontendTUI:
    """Reuseable frontend TUI class"""
    def __init__(self, options: List[Option] = [], app_name:str = "My TUI App"):
        self.title = app_name
        self.options = options
        self.running = True
        
        # add an exit option to the end of options list
        self.options.append(Option({
            "label": "Exit",
            "function": self.exit_program
        }))
    
    def exit_program(self):
        print("Exiting Program!")
        self.running = False
            
    def init_ui(self) -> None:
        self.print_header()
        self.print_footer()
    
    def clear_screen(self) -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, subtitle: str = "") -> None:
        """Print a formatted header."""
        self.clear_screen()
        width = 50
        print("=" * width)
        print(self.title.center(width))
        if subtitle:
            print(subtitle)
        print("=" * width)
        print()

        
    def print_footer(self) -> None:
        """Print a formatted footer."""
        print()
        print("-" * 50)
        print("Press Enter to continue...")
        input()
        
    def run(self):
        """Main loop for the TUI"""
        subtitle = "Main Menu"
        while self.running:
            self.print_header(subtitle)
            for idx, opt in enumerate(self.options, start=1):
                print(f"{idx}. {opt["label"]}")
            print()
            
            choice = input("Select an option by number:").strip()
            
            if not choice.isdigit() or not (1 <= int(choice) <= len(self.options)):
                print("\n⚠️   Invalid selection - please try again.")
                self.print_footer()
                continue
            
            option = self.options[int(choice) - 1]
            
            static_pos = option.get("args", [])
            static_kw = option.get("kwargs", {})
            runtime_pos = []
            cancelled  = False
            
            self.print_header(option["label"])
            print("Press ESC to cancel and go back . . .")
            print()
            
            for prompt in option.get("prompt_args", []):
                val = input_with_esc(f"{prompt}: ")
                
                if val is None:  # ESC pressed -> cancel input gathering
                    cancelled = True
                    break
                runtime_pos.append(val)

            if cancelled:
                continue
            
            self.print_header(option["label"])
            try:
                option["function"](*static_pos, *runtime_pos, **static_kw)
            except Exception as e:
                print(f"\n 💥 Error while executing '{option['label']}': {e}")
            
            if self.running:
                self.print_footer()        
            
            
            
    
# --- Helper Functions ---

if os.name == 'nt':
    import msvcrt

    def input_with_esc(prompt: str) -> str | None:
        """Custom input function that cancels on ESC key (Windows)."""
        print(prompt, end='', flush=True)
        result = ''
        while True:
            key = msvcrt.getwch()  # getwch() returns a Unicode char directly
            if key == '\r':  # Enter key
                print()
                return result
            elif key == '\x1b':  # ESC key
                print("\nInput cancelled.")
                return None
            elif key == '\b':  # Backspace
                if len(result) > 0:
                    result = result[:-1]
                    # Move cursor back, overwrite last char with space, move back again
                    print('\b \b', end='', flush=True)
            else:
                result += key
                print(key, end='', flush=True)

else:
    import tty
    import termios

    def input_with_esc(prompt: str) -> str | None:
        """Custom input function that cancels on ESC key (Unix)."""
        print(prompt, end='', flush=True)
        result = ''
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch == '\r' or ch == '\n':  # Enter key
                    print()
                    return result
                elif ch == '\x1b':  # ESC key
                    print("\nInput cancelled.")
                    return None
                elif ch == '\x7f':  # Backspace on Unix
                    if len(result) > 0:
                        result = result[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    result += ch
                    print(ch, end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
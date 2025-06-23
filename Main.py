from FrontendTUI import FrontendTUI
""" THIS Main.py SCRIPT IS JUST FOR TESTING AND SHOWING FUNCTIONALITY"""

# --- Test Functions ---
def greet(name: str) -> None:
    print(f"\nHello, {name}! Welcome to the TUI.")

def add_numbers(a: str, b: str) -> None:
    try:
        result = float(a) + float(b)
        print(f"\nResult: {a} + {b} = {result}")
    except ValueError:
        print("\n⚠️   Please enter valid numbers.")

def show_info() -> None:
    print("\nThis is a reusable TUI demo. Have fun!")
    

# follow this template for your functions
# prompt args will ask for input from the users
# be sure to put this in the same order as the args 
# your function.
# you can hard code your positional args with the "args" key
# same thing for kargws with "kargws"

# class Option(TypedDict, total=False):
#     label: str                               # Display label for the TUI
#     function: Callable                       # The function to call
#     args: Optional[List[Any]]                # Static positional arguments (optional)
#     kwargs: Optional[Dict[str, Any]]         # Static keyword arguments (optional)
#     prompt_args: Optional[List[str]]         # Prompts for runtime positional args (optional)

options = [
    {
        "label": "Greet User",
        "function": greet,
        "prompt_args": ["Enter your name"]
    },
    {
        "label": "Add Two Numbers",
        "function": add_numbers,
        "prompt_args": ["First number", "Second number"]
    },
    {
        "label": "Show Info",
        "function": show_info,
        # No args or prompt_args needed here
    },
]

# pass in options list and optional name:str arg 
frontend = FrontendTUI(options)
frontend.run()

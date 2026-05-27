import sys


def calculate(a: float, op: str, b: float) -> float | str:
    """Perform a single arithmetic operation. Returns result or error string."""
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            return "Error: Division by zero"
        return a / b
    else:
        return f"Error: Unknown operator '{op}'"


def format_result(value: float) -> str:
    """Display integers without a decimal point."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)




def run_cli():
    print("=" * 36)
    print("   Simple Calculator  (type 'q' to quit)")
    print("=" * 36)

    while True:
        expr = input("\nEnter expression (e.g. 12 + 7): ").strip()
        if expr.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            break

        parts = expr.split()
        if len(parts) != 3:
            print("  ✗  Please enter: <number> <operator> <number>")
            continue

        a_str, op, b_str = parts
        try:
            a, b = float(a_str), float(b_str)
        except ValueError:
            print("  ✗  Both operands must be numbers.")
            continue

        result = calculate(a, op, b)
        if isinstance(result, str):          # error message
            print(f"  ✗  {result}")
        else:
            print(f"  =  {format_result(result)}")


def run_gui():
    try:
        import tkinter as tk
        from tkinter import font as tkfont
    except ImportError:
        print("tkinter is not available. Run with --cli for the terminal version.")
        sys.exit(1)


    expression = ""          
    just_evaluated = False   


    def update_display(text: str):
        display_var.set(text)

    def button_click(value: str):
        nonlocal expression, just_evaluated

        if value == "C":
            expression = ""
            just_evaluated = False
            update_display("0")
            return

        if value == "⌫":
            expression = expression[:-1]
            just_evaluated = False
            update_display(expression if expression else "0")
            return

        if value == "=":
            try:

                result = eval(expression, {"__builtins__": {}})   # noqa: S307
                result_str = format_result(float(result))
                update_display(result_str)
                expression = result_str
                just_evaluated = True
            except ZeroDivisionError:
                update_display("Div by zero")
                expression = ""
            except Exception:
                update_display("Error")
                expression = ""
            return

        if just_evaluated and value in "0123456789.":
            expression = ""
        just_evaluated = False

        expression += value
        update_display(expression)
    root = tk.Tk()
    root.title("Calculator")
    root.resizable(False, False)
    root.configure(bg="#1e1e2e")

    display_var = tk.StringVar(value="0")
    display_font = tkfont.Font(family="Courier", size=28, weight="bold")
    display = tk.Label(
        root,
        textvariable=display_var,
        font=display_font,
        bg="#181825",
        fg="#cdd6f4",
        anchor="e",
        padx=16,
        pady=14,
        relief="flat",
        width=14,
    )
    display.grid(row=0, column=0, columnspan=4, padx=12, pady=(12, 4), sticky="ew")


    btn_font = tkfont.Font(family="Courier", size=16, weight="bold")

    buttons = [
        ["C",  "⌫",  "%",  "/"],
        ["7",  "8",  "9",  "*"],
        ["4",  "5",  "6",  "-"],
        ["1",  "2",  "3",  "+"],
        ["0",  ".",  " ",  "="],  
    ]


    COLOR = {
        "digit":    ("#313244", "#cdd6f4"),   
        "op":       ("#45475a", "#fab387"),
        "special":  ("#585b70", "#a6e3a1"),
        "equals":   ("#89b4fa", "#1e1e2e"),
        "clear":    ("#f38ba8", "#1e1e2e"),
        "back":     ("#f38ba8", "#1e1e2e"),
    }

    def color_for(lbl):
        if lbl == "=":   return COLOR["equals"]
        if lbl == "C":   return COLOR["clear"]
        if lbl == "⌫":  return COLOR["back"]
        if lbl in "+-*/": return COLOR["op"]
        if lbl in "%.":  return COLOR["special"]
        return COLOR["digit"]

    for r, row in enumerate(buttons, start=1):
        for c, label in enumerate(row):
            if label == " ":
                continue           

            bg, fg = color_for(label)


            colspan = 2 if label == "0" else 1

            btn = tk.Button(
                root,
                text=label,
                font=btn_font,
                bg=bg,
                fg=fg,
                activebackground=fg,
                activeforeground=bg,
                relief="flat",
                bd=0,
                padx=0,
                pady=12,
                cursor="hand2",
                command=lambda v=label: button_click(v),
            )
            btn.grid(
                row=r, column=c,
                columnspan=colspan,
                padx=4, pady=4,
                sticky="nsew",
                ipadx=10,
            )


    for i in range(4):
        root.grid_columnconfigure(i, weight=1)
    for i in range(6):
        root.grid_rowconfigure(i, weight=1)


    def key_press(event):
        key = event.char
        if key in "0123456789.+-*/":
            button_click(key)
        elif key in ("\r", "="):
            button_click("=")
        elif key in ("\x08",):          
            button_click("⌫")
        elif key.lower() == "c":
            button_click("C")

    root.bind("<Key>", key_press)

    root.mainloop()


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        run_gui()
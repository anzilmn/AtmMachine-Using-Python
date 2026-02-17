import tkinter as tk
from tkinter import messagebox, simpledialog

class PremierATM:
    def __init__(self, root):
        self.root = root
        self.root.title("PREMIER DIGITAL BANKING")
        self.root.geometry("450x700")
        self.root.configure(bg="#0a0a0a")  # Deep Obsidian Black

        # Premium UI Colors
        self.primary = "#00d4ff"   # Neon Cyan
        self.secondary = "#1a1a1a" # Dark Grey Frame
        self.accent = "#39ff14"    # Success Green
        self.danger = "#ff4b2b"    # Error Red
        self.text_col = "#ffffff"  # Pure White

        # Mock Database
        self.users = {
            "101": {"pin": "1234", "balance": 5000.0, "history": ["Initial Balance: $5000.00"]}
        }
        self.current_user = None

        self.show_auth_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def verify_action(self):
        """Asks for PIN before any transaction with a styled dialog"""
        verify_pin = simpledialog.askstring("SECURE VERIFICATION", "Please confirm your 4-Digit PIN:", show='*', parent=self.root)
        if verify_pin == self.users[self.current_user]['pin']:
            return True
        else:
            messagebox.showerror("SECURITY BREACH", "Authorization Failed: Incorrect PIN.")
            return False

    # --- AUTHENTICATION SCREENS ---
    def show_auth_screen(self):
        self.clear_window()
        
        # Header Logo Area
        header = tk.Frame(self.root, bg="#0a0a0a", pady=40)
        header.pack(fill="x")
        tk.Label(header, text="💎", font=("Arial", 40), bg="#0a0a0a").pack()
        
        # Fixed: Removed 'letterspacing' which caused the crash
        tk.Label(header, text="P R E M I E R", fg=self.primary, bg="#0a0a0a", font=("Helvetica", 24, "bold")).pack()
        tk.Label(header, text="DIGITAL BANKING", fg="#555", bg="#0a0a0a", font=("Helvetica", 10, "bold")).pack()

        # Input Frame
        frame = tk.Frame(self.root, bg=self.secondary, padx=30, pady=30, highlightbackground=self.primary, highlightthickness=1)
        frame.pack(pady=10, padx=40)

        tk.Label(frame, text="CARD NUMBER", fg="#888", bg=self.secondary, font=("Arial", 8, "bold")).pack(anchor="w")
        self.card_entry = tk.Entry(frame, font=("Arial", 16), justify='center', bg="#252525", fg="white", bd=0, insertbackground="white")
        self.card_entry.pack(pady=(5, 15), ipady=5)

        tk.Label(frame, text="SECRET PIN", fg="#888", bg=self.secondary, font=("Arial", 8, "bold")).pack(anchor="w")
        self.pin_entry = tk.Entry(frame, show="*", font=("Arial", 16), justify='center', bg="#252525", fg="white", bd=0, insertbackground="white")
        self.pin_entry.pack(pady=(5, 5), ipady=5)

        # Buttons
        tk.Button(self.root, text="SECURE LOGIN", command=self.handle_login, bg=self.primary, fg="black", 
                  font=("Arial", 11, "bold"), width=25, height=2, bd=0, cursor="hand2").pack(pady=25)
        
        tk.Button(self.root, text="CREATE ACCOUNT", command=self.show_register_screen, bg="#0a0a0a", 
                  fg="#777", bd=0, font=("Arial", 9, "underline"), cursor="hand2").pack()

    def show_register_screen(self):
        self.clear_window()
        tk.Label(self.root, text="NEW ENROLLMENT", fg=self.accent, bg="#0a0a0a", font=("Arial", 20, "bold"), pady=40).pack()
        
        frame = tk.Frame(self.root, bg=self.secondary, padx=30, pady=30)
        frame.pack(pady=10)

        tk.Label(frame, text="ASSIGN CARD NUMBER", fg="white", bg=self.secondary).pack()
        new_card = tk.Entry(frame, font=("Arial", 14), bg="#252525", fg="white", bd=0)
        new_card.pack(pady=10, ipady=5)

        tk.Label(frame, text="SET 4-DIGIT PIN", fg="white", bg=self.secondary).pack()
        new_pin = tk.Entry(frame, show="*", font=("Arial", 14), bg="#252525", fg="white", bd=0)
        new_pin.pack(pady=10, ipady=5)

        def save_user():
            c, p = new_card.get(), new_pin.get()
            if c and len(p) == 4 and p.isdigit():
                self.users[c] = {"pin": p, "balance": 0.0, "history": ["Account Created"]}
                messagebox.showinfo("SUCCESS", "Registration Complete. Please Login.")
                self.show_auth_screen()
            else:
                messagebox.showerror("ERROR", "PIN must be 4 digits.")

        tk.Button(self.root, text="REGISTER NOW", command=save_user, bg=self.accent, fg="black", 
                  font=("Arial", 11, "bold"), width=20, height=2, bd=0).pack(pady=20)
        tk.Button(self.root, text="← RETURN", command=self.show_auth_screen, bg="#0a0a0a", fg="white", bd=0).pack()

    def handle_login(self):
        card, pin = self.card_entry.get(), self.pin_entry.get()
        if card in self.users and self.users[card]['pin'] == pin:
            self.current_user = card
            self.main_menu()
        else:
            messagebox.showerror("ACCESS DENIED", "Invalid Credentials Provided.")

    # --- MAIN DASHBOARD ---
    def main_menu(self):
        self.clear_window()
        user_data = self.users[self.current_user]

        # Top Bar
        top_bar = tk.Frame(self.root, bg=self.secondary, height=50)
        top_bar.pack(fill="x")
        tk.Label(top_bar, text=f"👤 ID: {self.current_user}", fg="#aaa", bg=self.secondary, font=("Arial", 9)).pack(side="left", padx=20)
        
        # Balance Card
        disp = tk.Frame(self.root, bg="#111", pady=30, highlightbackground="#333", highlightthickness=1)
        disp.pack(fill="x", padx=30, pady=30)
        
        tk.Label(disp, text="TOTAL ASSETS", fg="#888", bg="#111", font=("Arial", 10, "bold")).pack()
        self.bal_label = tk.Label(disp, text=f"${user_data['balance']:,.2f}", fg=self.accent, bg="#111", font=("Courier", 35, "bold"))
        self.bal_label.pack()

        # Action Grid
        menu_frame = tk.Frame(self.root, bg="#0a0a0a")
        menu_frame.pack(pady=10)

        btns = [
            ("📥 DEPOSIT", self.deposit, "#222"), 
            ("📤 WITHDRAW", self.withdraw, "#222"),
            ("⚡ FAST CASH", self.show_fast_cash_menu, self.primary), 
            ("📜 MINI STMT", self.mini_statement, "#222"),
            ("🔐 SECURITY", self.change_pin, "#222"), 
            ("🚪 LOGOUT", self.show_auth_screen, self.danger)
        ]

        for i, (text, cmd, color) in enumerate(btns):
            fg_col = "black" if color in [self.primary, self.accent] else "white"
            b = tk.Button(menu_frame, text=text, command=cmd, bg=color, fg=fg_col, 
                          font=("Arial", 10, "bold"), width=18, height=3, bd=0, cursor="hand2")
            b.grid(row=i//2, column=i%2, padx=8, pady=8)

    # --- FAST CASH MENU ---
    def show_fast_cash_menu(self):
        self.clear_window()
        tk.Label(self.root, text="⚡ SELECT AMOUNT", fg=self.primary, bg="#0a0a0a", font=("Arial", 20, "bold"), pady=40).pack()
        
        grid_frame = tk.Frame(self.root, bg="#0a0a0a")
        grid_frame.pack()

        amounts = [100, 500, 1000, 2000, 5000, 10000]
        for i, amt in enumerate(amounts):
            b = tk.Button(grid_frame, text=f"${amt}", command=lambda a=amt: self.process_fast_cash(a),
                          bg=self.secondary, fg="white", font=("Arial", 12, "bold"), width=12, height=2, bd=0)
            b.grid(row=i//2, column=i%2, padx=10, pady=10)

        tk.Button(self.root, text="CANCEL", command=self.main_menu, bg=self.danger, fg="white", 
                  font=("Arial", 10, "bold"), width=20, height=2, bd=0).pack(pady=40)

    # --- CORE LOGIC ---
    def process_fast_cash(self, amount):
        if self.verify_action():
            if self.users[self.current_user]['balance'] >= amount:
                self.users[self.current_user]['balance'] -= amount
                self.users[self.current_user]['history'].append(f"Fast Cash: -${amount:,.2f}")
                self.main_menu()
                messagebox.showinfo("DISPENSED", f"Please collect your cash: ${amount}")
            else:
                messagebox.showerror("FUNDS ERROR", "Transaction Declined: Insufficient Balance.")

    def deposit(self):
        amt = simpledialog.askfloat("DEPOSIT FUNDS", "Enter Deposit Amount ($):", parent=self.root)
        if amt and amt > 0:
            if self.verify_action():
                self.users[self.current_user]['balance'] += amt
                self.users[self.current_user]['history'].append(f"Deposit: +${amt:,.2f}")
                self.update_ui_balance()
                messagebox.showinfo("COMPLETED", "Your account has been credited.")

    def withdraw(self):
        amt = simpledialog.askfloat("WITHDRAW CASH", "Enter Withdrawal Amount ($):", parent=self.root)
        if amt and amt > 0:
            if self.verify_action():
                if amt <= self.users[self.current_user]['balance']:
                    self.users[self.current_user]['balance'] -= amt
                    self.users[self.current_user]['history'].append(f"Withdrawal: -${amt:,.2f}")
                    self.update_ui_balance()
                    messagebox.showinfo("COMPLETED", "Please remove your card and cash.")
                else:
                    messagebox.showerror("DECLINED", "Insufficient funds for this request.")

    def mini_statement(self):
        if self.verify_action():
            history = "\n".join(self.users[self.current_user]['history'][-8:])
            messagebox.showinfo("TRANSACTION LEDGER", f"Last 8 Activities:\n\n{history}")

    def change_pin(self):
        if self.verify_action():
            new_p = simpledialog.askstring("SECURITY UPDATE", "Enter New Secret PIN (4 Digits):", show='*', parent=self.root)
            if new_p and len(new_p) == 4 and new_p.isdigit():
                self.users[self.current_user]['pin'] = new_p
                messagebox.showinfo("SUCCESS", "PIN updated. Keep it confidential.")
            else:
                messagebox.showerror("INVALID", "PIN must be exactly 4 digits.")

    def update_ui_balance(self):
        self.bal_label.config(text=f"${self.users[self.current_user]['balance']:,.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PremierATM(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk
from auth import authenticate, register_user
from inventory import *

# ----------------------------- Common Styling -----------------------------
BG_COLOR = "#f0f4f7"
FRAME_BG = "white"
BTN_GREEN = "#4CAF50"
BTN_BLUE = "#2196F3"
BTN_RED = "#f44336"
FONT_HEADER = ("Helvetica", 16, "bold")
FONT_LABEL = ("Helvetica", 11)
PADDING = 10

# ----------------------------- Login Window -----------------------------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Inventory System")
        self.root.geometry("400x300")
        self.root.configure(bg=BG_COLOR)

        self.frame = tk.Frame(root, bg=FRAME_BG, bd=3, relief=tk.RIDGE)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=350, height=250)

        tk.Label(self.frame, text="Login", font=FONT_HEADER, bg=FRAME_BG).pack(pady=15)

        tk.Label(self.frame, text="Username:", bg=FRAME_BG, font=FONT_LABEL).pack()
        self.username = tk.Entry(self.frame)
        self.username.pack(pady=5)

        tk.Label(self.frame, text="Password:", bg=FRAME_BG, font=FONT_LABEL).pack()
        self.password = tk.Entry(self.frame, show="*")
        self.password.pack(pady=5)

        tk.Button(self.frame, text="Login", bg=BTN_GREEN, fg="white", width=12, command=self.login).pack(pady=(10, 5))
        tk.Button(self.frame, text="Register", bg=BTN_BLUE, fg="white", width=12, command=self.open_register).pack()

    def login(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        if authenticate(user, pwd):
            self.root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_register(self):
        self.root.destroy()
        open_register()

# ----------------------------- Register Window -----------------------------
class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Register - Inventory System")
        self.root.geometry("450x550")
        self.root.configure(bg=BG_COLOR)

        self.frame = tk.Frame(root, bg=FRAME_BG, bd=3, relief=tk.RIDGE)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=500)

        tk.Label(self.frame, text="Create Account", font=FONT_HEADER, bg=FRAME_BG).pack(pady=15)

        self.entries = {}
        fields = ["Name", "Phone", "Age", "Workplace", "Branch", "Username", "Password"]
        for field in fields:
            tk.Label(self.frame, text=f"{field}:", bg=FRAME_BG, font=FONT_LABEL).pack()
            entry = tk.Entry(self.frame, show="*" if field == "Password" else "")
            entry.pack(pady=5)
            self.entries[field.lower()] = entry

        tk.Button(self.frame, text="Register", bg=BTN_GREEN, fg="white", width=15, command=self.register_user).pack(pady=(20, 10))
        tk.Button(self.frame, text="Back to Login", bg=BTN_BLUE, fg="white", width=15, command=self.back_to_login).pack()

    def register_user(self):
        try:
            name = self.entries["name"].get().strip()
            phone = self.entries["phone"].get().strip()
            age_text = self.entries["age"].get().strip()
            workplace = self.entries["workplace"].get().strip()
            branch = self.entries["branch"].get().strip()
            username = self.entries["username"].get().strip()
            password = self.entries["password"].get().strip()

            if not all([name, phone, age_text, workplace, branch, username, password]):
                raise ValueError("All fields must be filled")

            age = int(age_text)

            register_user(name, phone, age, workplace, branch, username, password)
            messagebox.showinfo("Success", "Account created successfully!")
            self.root.destroy()
            open_login()

        except Exception as e:
            print("Registration error:", e)
            messagebox.showerror("Error", f"Registration failed: {e}")

    def back_to_login(self):
        self.root.destroy()
        open_login()

# ----------------------------- Dashboard Window -----------------------------
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Dashboard")
        self.root.geometry("750x550")
        self.root.configure(bg=BG_COLOR)

        self.frame = tk.Frame(root, bg=FRAME_BG, bd=3, relief=tk.RIDGE)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=700, height=500)

        tk.Label(self.frame, text="Inventory Management", font=FONT_HEADER, bg=FRAME_BG).pack(pady=15)

        form_frame = tk.Frame(self.frame, bg=FRAME_BG)
        form_frame.pack(pady=10)

        labels = ["Product ID", "Name", "Quantity", "Price"]
        self.entries = []
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg=FRAME_BG, font=FONT_LABEL, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        self.id_entry, self.name_entry, self.qty_entry, self.price_entry = self.entries

        btn_frame = tk.Frame(self.frame, bg=FRAME_BG)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add", width=12, bg=BTN_GREEN, fg="white", command=self.add_product).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", width=12, bg=BTN_BLUE, fg="white", command=self.update_product).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", width=12, bg=BTN_RED, fg="white", command=self.delete_product).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Low Stock", width=12, bg="#9C27B0", fg="white", command=self.show_low_stock).grid(row=0, column=3, padx=5)

        self.tree = ttk.Treeview(self.frame, columns=("id", "name", "qty", "price"), show="headings", height=10)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)
        self.tree.pack(pady=10)
        self.tree.bind("<Double-1>", self.load_product)

        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in read_inventory():
            self.tree.insert("", "end", values=(item["id"], item["name"], item["quantity"], item["price"]))

    def add_product(self):
     try:
        add_product_to_db(self.id_entry.get(), self.name_entry.get(),
                          int(self.qty_entry.get()), float(self.price_entry.get()))
        self.refresh_table()
     except:
        messagebox.showerror("Error", "Invalid input for adding product")

    def delete_product(self):
        pid = self.id_entry.get()
        delete_product(pid)
        self.refresh_table()

    def update_product(self):
        try:
            update_product(self.id_entry.get(), self.name_entry.get(),
                           int(self.qty_entry.get()), float(self.price_entry.get()))
            self.refresh_table()
        except:
            messagebox.showerror("Error", "Invalid input for updating product")

    def load_product(self, event):
        selected = self.tree.item(self.tree.focus())['values']
        if selected:
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.qty_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.id_entry.insert(0, selected[0])
            self.name_entry.insert(0, selected[1])
            self.qty_entry.insert(0, selected[2])
            self.price_entry.insert(0, selected[3])

    def show_low_stock(self):
        stocks = low_stock()
        msg = "\n".join([f"{item['name']} (Qty: {item['quantity']})" for item in stocks])
        messagebox.showinfo("Low Stock", msg if msg else "All stock levels are sufficient.")

# ----------------------------- Page Loaders -----------------------------
def open_login():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

def open_register():
    root = tk.Tk()
    RegisterWindow(root)
    root.mainloop()

def open_dashboard():
    root = tk.Tk()
    Dashboard(root)
    root.mainloop()

# ----------------------------- Run -----------------------------
if __name__ == "__main__":
    open_login()
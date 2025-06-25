import tkinter as tk
import tkinter.font as tkfont
import os
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

API_URL = "http://127.0.0.1:5000/api"

class ShoeShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XMove Shoe Shop Desktop")
        self.geometry("1050x670")
        self.resizable(False, False)
        self.selected_gender = "Men"
        self.selected_brand = "All"
        self.section = "shop"
        self.bg_label = None  # Track the background image label

        font_path = os.path.join(os.path.dirname(__file__), "fonts", "PressStart2P-Regular.ttf")
        if os.path.exists(font_path):
            try:
                self.tk.call('font', 'create', 'PixelFont', '-family', 'Press Start 2P', '-size', 9)
                self.pixel_font = tkfont.Font(name='PixelFont', exists=True)
                self.option_add("*Font", self.pixel_font)
            except Exception as e:
                print("Failed to load pixel font, using default. Reason:", e)
                self.pixel_font = ("Arial", 10)
                self.option_add("*Font", self.pixel_font)
        else:
            print("Font file not found. Using default font.")
            self.pixel_font = ("Arial", 10)
            self.option_add("*Font", self.pixel_font)
        
        self.init_ui()
        self.show_login()

    # ========== AUTH UI ==========

    def show_login(self):
        for widget in self.winfo_children():
            widget.pack_forget()
            widget.place_forget()

        # Set background image (track bg_label so we can hide it later)
        bg_path = os.path.join(os.path.dirname(__file__), "background.jpg")
        if os.path.exists(bg_path):
            bg_img = Image.open(bg_path).resize((1050, 670))
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            if hasattr(self, "bg_label") and self.bg_label:
                self.bg_label.configure(image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                self.bg_label = tk.Label(self, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.configure(bg="#242426")
            self.bg_label = None

        # Center login panel
        panel_width, panel_height = 520, 410
        x0, y0 = (1050 - panel_width) // 2, (670 - panel_height) // 2

        self.login_canvas = tk.Canvas(self, width=panel_width, height=panel_height, bg='#dedede', highlightthickness=0)
        self.login_canvas.place(x=x0, y=y0)
        radius = 40
        color = "#dedede"
        # Draw corners
        self.login_canvas.create_arc((0, 0, radius*2, radius*2), start=90, extent=90, fill=color, outline=color)
        self.login_canvas.create_arc((panel_width-radius*2, 0, panel_width, radius*2), start=0, extent=90, fill=color, outline=color)
        self.login_canvas.create_arc((0, panel_height-radius*2, radius*2, panel_height), start=180, extent=90, fill=color, outline=color)
        self.login_canvas.create_arc((panel_width-radius*2, panel_height-radius*2, panel_width, panel_height), start=270, extent=90, fill=color, outline=color)
        self.login_canvas.create_rectangle((radius, 0, panel_width-radius, panel_height), fill=color, outline=color)
        self.login_canvas.create_rectangle((0, radius, panel_width, panel_height-radius), fill=color, outline=color)

        frm = tk.Frame(self.login_canvas, bg=color)
        tk.Label(frm, text="LOGIN", font=(self.pixel_font, 28, "bold"), bg=color).pack(pady=(20, 18))

        # Email Entry
        email_var = tk.StringVar()
        self.email_entry = tk.Entry(frm, width=34, font=(self.pixel_font, 13), bg="#ececec", fg="#222", textvariable=email_var, borderwidth=0, relief=tk.FLAT)
        self.email_entry.insert(0, "EMAIL ADDRESS")
        self.email_entry.pack(pady=(0, 14), ipady=7)

        # Password Entry
        password_var = tk.StringVar()
        self.password_entry = tk.Entry(frm, width=34, font=(self.pixel_font, 13), bg="#ececec", fg="#222", textvariable=password_var, borderwidth=0, relief=tk.FLAT)
        self.password_entry.insert(0, "PASSWORD")
        self.password_entry.pack(pady=(0, 10), ipady=7)

        # Checkbox only
        cb_var = tk.IntVar()
        cb_frame = tk.Frame(frm, bg=color)
        cb_frame.pack(fill="x", padx=16)
        cb = tk.Checkbutton(cb_frame, text="KEEP ME LOGGED IN", variable=cb_var, bg=color, font=(self.pixel_font, 10), borderwidth=0, highlightthickness=0)
        cb.pack(side=tk.LEFT, anchor="w")

        # Divider
        tk.Frame(frm, bg=color).pack(pady=(6,0))

        # Login button
        login_btn = tk.Button(frm, text="LOGIN", font=(self.pixel_font, 14, "bold"), bg="black", fg="white", width=20, height=1,
                              command=lambda: self.do_login_with_entries(self.email_entry, self.password_entry))
        login_btn.pack(pady=(20, 8))

        # Sign Up button
        signup_btn = tk.Button(frm, text="Sign Up", font=(self.pixel_font, 12, "bold"), bg="#444", fg="white", width=20, height=1,
                               command=self.show_signup)
        signup_btn.pack(pady=(0, 10))

        # Policy text
        tk.Label(frm, text="By logging in, you agree to XMove's Privacy Policy and Terms of use",
                 bg=color, fg="#222", font=(self.pixel_font, 9), wraplength=420, justify="center").pack(pady=(12,2))

        self.login_status = tk.Label(frm, text="", fg="red", bg=color, font=(self.pixel_font, 10))
        self.login_status.pack(pady=2)

        self.login_canvas.create_window(panel_width // 2, panel_height // 2, window=frm)

        # Clear placeholder text on click
        def clear_email(e):
            if self.email_entry.get() == "EMAIL ADDRESS":
                self.email_entry.delete(0, tk.END)
        def clear_pw(e):
            if self.password_entry.get() == "PASSWORD":
                self.password_entry.delete(0, tk.END)
                self.password_entry.config(show="*")
        self.email_entry.bind("<FocusIn>", clear_email)
        self.password_entry.bind("<FocusIn>", clear_pw)

    def do_login_with_entries(self, email_entry, password_entry):
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        if not email or not password or email == "EMAIL ADDRESS" or password == "PASSWORD":
            self.login_status.config(text="Please enter email and password.", fg="red")
            return
        try:
            resp = requests.post(API_URL.replace('/api','') + "/api/login", json={"email": email, "password": password})
            if resp.status_code == 200:
                self.login_status.config(text="Login successful!", fg="green")
                self.login_canvas.place_forget()
                # Hide background image after login
                if hasattr(self, "bg_label") and self.bg_label:
                    self.bg_label.place_forget()
                self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
                self.topbar.pack(side=tk.TOP, fill=tk.X)
                self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                self.load_brands()
                self.show_section("shop")
            else:
                self.login_status.config(text=resp.json().get("error", "Login failed"), fg="red")
        except Exception as e:
            self.login_status.config(text="Server error: " + str(e), fg="red")

    def logout(self):
        self.sidebar.pack_forget()
        self.topbar.pack_forget()
        self.main_frame.pack_forget()
        self.show_login()

    # Sign Up Page
    def show_signup(self):
        self.login_canvas.place_forget()
        # Show background image if hidden
        if hasattr(self, "bg_label") and self.bg_label:
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Center sign up panel
        panel_width, panel_height = 520, 410
        x0, y0 = (1050 - panel_width) // 2, (670 - panel_height) // 2

        self.signup_canvas = tk.Canvas(self, width=panel_width, height=panel_height, bg='#dedede', highlightthickness=0)
        self.signup_canvas.place(x=x0, y=y0)
        radius = 40
        color = "#dedede"
        # Draw corners
        self.signup_canvas.create_arc((0, 0, radius*2, radius*2), start=90, extent=90, fill=color, outline=color)
        self.signup_canvas.create_arc((panel_width-radius*2, 0, panel_width, radius*2), start=0, extent=90, fill=color, outline=color)
        self.signup_canvas.create_arc((0, panel_height-radius*2, radius*2, panel_height), start=180, extent=90, fill=color, outline=color)
        self.signup_canvas.create_arc((panel_width-radius*2, panel_height-radius*2, panel_width, panel_height), start=270, extent=90, fill=color, outline=color)
        self.signup_canvas.create_rectangle((radius, 0, panel_width-radius, panel_height), fill=color, outline=color)
        self.signup_canvas.create_rectangle((0, radius, panel_width, panel_height-radius), fill=color, outline=color)

        frm = tk.Frame(self.signup_canvas, bg=color)
        tk.Label(frm, text="SIGN UP", font=(self.pixel_font, 28, "bold"), bg=color).pack(pady=(20, 18))

        # Email and password entries
        self.signup_email_entry = tk.Entry(frm, width=34, font=(self.pixel_font, 13), bg="#ececec", fg="#222", borderwidth=0, relief=tk.FLAT)
        self.signup_email_entry.insert(0, "EMAIL ADDRESS")
        self.signup_email_entry.pack(pady=(0, 14), ipady=7)
        self.signup_password_entry = tk.Entry(frm, width=34, font=(self.pixel_font, 13), bg="#ececec", fg="#222", borderwidth=0, relief=tk.FLAT)
        self.signup_password_entry.insert(0, "PASSWORD")
        self.signup_password_entry.pack(pady=(0, 10), ipady=7)

        # Sign Up button
        signup_btn = tk.Button(frm, text="Sign Up", font=(self.pixel_font, 14, "bold"), bg="black", fg="white", width=20, height=1,
                               command=self.do_signup)
        signup_btn.pack(pady=(20, 10))

        # Back to Login button
        login_btn = tk.Button(frm, text="Back to Login", font=(self.pixel_font, 12, "bold"), bg="#444", fg="white", width=20, height=1,
                              command=self.back_to_login)
        login_btn.pack(pady=(0, 10))

        self.signup_status = tk.Label(frm, text="", fg="red", bg=color, font=(self.pixel_font, 10))
        self.signup_status.pack(pady=2)

        self.signup_canvas.create_window(panel_width // 2, panel_height // 2, window=frm)

        # Clear placeholder text on click
        def clear_signup_email(e):
            if self.signup_email_entry.get() == "EMAIL ADDRESS":
                self.signup_email_entry.delete(0, tk.END)
        def clear_signup_pw(e):
            if self.signup_password_entry.get() == "PASSWORD":
                self.signup_password_entry.delete(0, tk.END)
                self.signup_password_entry.config(show="*")
        self.signup_email_entry.bind("<FocusIn>", clear_signup_email)
        self.signup_password_entry.bind("<FocusIn>", clear_signup_pw)

    def back_to_login(self):
        self.signup_canvas.place_forget()
        self.show_login()

    def do_signup(self):
        email = self.signup_email_entry.get().strip()
        password = self.signup_password_entry.get().strip()
        if not email or not password or email == "EMAIL ADDRESS" or password == "PASSWORD":
            self.signup_status.config(text="Please enter email and password.", fg="red")
            return
        try:
            resp = requests.post(API_URL.replace('/api','') + "/api/signup", json={"email": email, "password": password})
            if resp.status_code == 200:
                self.signup_status.config(text="Sign up successful! Please login.", fg="green")
            else:
                self.signup_status.config(text=resp.json().get("error", "Sign up failed"), fg="red")
        except Exception as e:
            self.signup_status.config(text="Server error: " + str(e), fg="red")
            self.signup_status.after(3000, lambda: self.signup_status.config(text=""))

    # ========== MAIN UI ==========

    def init_ui(self):
        # Sidebar for brands 
        self.sidebar = tk.Frame(self, bg="black", width=160)
        self.brand_buttons = []
        self.brand_frame = tk.Frame(self.sidebar, bg="black")
        self.brand_frame.pack(pady=20)

        # Top menu 
        self.topbar = tk.Frame(self, bg="black", height=40)
        self.men_btn = tk.Button(self.topbar, text="Men", bg="white", fg="black", width=12,
                  command=lambda: self.switch_gender("Men"))
        self.men_btn.pack(side=tk.LEFT, padx=6, pady=5)
        self.women_btn = tk.Button(self.topbar, text="Women", bg="black", fg="white", width=12,
                  command=lambda: self.switch_gender("Women"))
        self.women_btn.pack(side=tk.LEFT, padx=6, pady=5)
        tk.Label(self.topbar, text="XMove", bg="black", fg="white", font=(self.pixel_font, 14, "bold")).pack(side=tk.LEFT, padx=14)
        tk.Button(self.topbar, text="Logout", bg="black", fg="white", width=10, command=self.logout).pack(side=tk.RIGHT, padx=6)
        tk.Button(self.topbar, text="Orders", bg="black", fg="white", width=10,
                  command=lambda: self.show_section("orders")).pack(side=tk.RIGHT, padx=6)
        tk.Button(self.topbar, text="Cart", bg="black", fg="white", width=10,
                  command=lambda: self.show_section("cart")).pack(side=tk.RIGHT, padx=6)

        # Main area with sections (shop, cart, orders)
        self.main_frame = tk.Frame(self, bg="white")

        # Shop Section 
        self.shop_canvas = tk.Canvas(self.main_frame, bg="white", highlightthickness=0)
        self.shop_scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.shop_canvas.yview)
        self.shop_canvas.configure(yscrollcommand=self.shop_scrollbar.set)
        self.shop_frame = tk.Frame(self.shop_canvas, bg="white")
        self.shop_frame_id = self.shop_canvas.create_window((0, 0), window=self.shop_frame, anchor="nw")
        self.shop_frame.bind("<Configure>", lambda event: self.shop_canvas.configure(scrollregion=self.shop_canvas.bbox("all")))
        self.shop_canvas.bind("<Configure>", lambda event: self.shop_canvas.itemconfig(self.shop_frame_id, width=event.width))

        # Cart Section
        self.cart_section = tk.Frame(self.main_frame, bg="white")
        self.cart_title = tk.Label(self.cart_section, text="Your Cart", font=(self.pixel_font, 14, "bold"), bg="white")
        self.cart_title.pack(pady=(22, 2))
        self.cart_list = tk.Frame(self.cart_section, bg="white")
        self.cart_list.pack(fill=tk.BOTH, expand=True)
        self.place_order_btn = tk.Button(self.cart_section, text="Place Order", bg="black", fg="white", font=(self.pixel_font, 12),
                                         command=self.place_order)
        self.place_order_btn.pack(pady=16)
        self.empty_cart_label = tk.Label(self.cart_section, text="Your cart is empty.", font=(self.pixel_font, 11), bg="white")

        # Orders Section
        self.orders_canvas = tk.Canvas(self.main_frame, bg="white", highlightthickness=0)
        self.orders_scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.orders_canvas.yview)
        self.orders_canvas.configure(yscrollcommand=self.orders_scrollbar.set)
        self.orders_frame = tk.Frame(self.orders_canvas, bg="white")
        self.orders_frame_id = self.orders_canvas.create_window((0, 0), window=self.orders_frame, anchor="nw")
        self.orders_frame.bind("<Configure>", lambda event: self.orders_canvas.configure(scrollregion=self.orders_canvas.bbox("all")))
        self.orders_canvas.bind("<Configure>", lambda event: self.orders_canvas.itemconfig(self.orders_frame_id, width=event.width))

    def show_section(self, section):
        self.section = section
        self.shop_canvas.pack_forget()
        self.shop_scrollbar.pack_forget()
        self.cart_section.pack_forget()
        self.orders_canvas.pack_forget()
        self.orders_scrollbar.pack_forget()
        
        if section == "shop":
            self.shop_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=20)
            self.shop_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.load_products()
            self.men_btn.config(relief=tk.SUNKEN if self.selected_gender=="Men" else tk.RAISED,
                               bg="white" if self.selected_gender=="Men" else "black",
                               fg="black" if self.selected_gender=="Men" else "white")
            self.women_btn.config(relief=tk.SUNKEN if self.selected_gender=="Women" else tk.RAISED,
                               bg="white" if self.selected_gender=="Women" else "black",
                               fg="black" if self.selected_gender=="Women" else "white")
        elif section == "cart":
            self.cart_section.pack(fill=tk.BOTH, expand=True, padx=120, pady=30)
            self.render_cart()
        elif section == "orders":
            self.orders_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=20)
            self.orders_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.render_orders()

    def load_brands(self):
        for btn in self.brand_buttons:
            btn.destroy()
        self.brand_buttons = []
        try:
            brands = requests.get(API_URL + "/brands").json()
        except:
            brands = ["All"]
        for brand in brands:
            btn = tk.Button(self.brand_frame, text=brand, width=14, bg="black" if self.selected_brand != brand else "white",
                            fg="white" if self.selected_brand != brand else "black", relief=tk.FLAT,
                            command=lambda b=brand: self.switch_brand(b))
            btn.pack(pady=2)
            self.brand_buttons.append(btn)

    def switch_brand(self, brand):
        self.selected_brand = brand
        self.load_brands()
        self.load_products()

    def switch_gender(self, gender):
        self.selected_gender = gender
        self.load_products()
        self.show_section("shop")

    def load_products(self):
        for widget in self.shop_frame.winfo_children():
            widget.destroy()
        params = {"gender": self.selected_gender}
        if self.selected_brand and self.selected_brand != "All":
            params["brand"] = self.selected_brand
        try:
            products = requests.get(API_URL + "/products", params=params).json()
        except:
            products = []
        for idx, prod in enumerate(products):
            frame = tk.Frame(self.shop_frame, bd=2, relief=tk.GROOVE, bg="white")
            frame.grid(row=idx // 3, column=idx % 3, padx=16, pady=12, sticky="nsew")
            # Product image
            try:
                imgdata = requests.get("http://127.0.0.1:5000" + prod["img"]).content
                image = Image.open(BytesIO(imgdata)).resize((110, 65))
                tkimg = ImageTk.PhotoImage(image)
                img_label = tk.Label(frame, image=tkimg, bg="white")
                img_label.image = tkimg
            except:
                img_label = tk.Label(frame, text="[Image]", bg="white")
            img_label.pack(pady=8)
            tk.Label(frame, text=prod["name"], bg="white", font=(self.pixel_font, 11, "bold")).pack()
            tk.Label(frame, text=f"RM {prod['price']:.2f}", bg="white").pack()
            # Buttons
            bframe = tk.Frame(frame, bg="white")
            bframe.pack(pady=6)
            tk.Button(bframe, text="Add to Cart", bg="black", fg="white", width=11,
                      command=lambda pid=prod["id"]: self.add_to_cart(pid)).pack(side=tk.LEFT, padx=2)
            tk.Button(bframe, text="Order", bg="black", fg="white", width=8,
                      command=lambda pid=prod["id"]: self.order_now(pid)).pack(side=tk.LEFT, padx=2)

    def add_to_cart(self, product_id):
        try:
            products = requests.get(API_URL + "/products").json()
        except:
            messagebox.showerror("Error", "Failed to fetch products from server.")
            return
        prod = next((p for p in products if p["id"] == product_id), None)
        if prod:
            payload = {"id": prod["id"], "name": prod["name"], "price": prod["price"]}
            requests.post(API_URL + "/cart", json=payload)
            messagebox.showinfo("Cart", f"{prod['name']} added to cart.")

    def order_now(self, product_id):
        try:
            products = requests.get(API_URL + "/products").json()
        except:
            messagebox.showerror("Error", "Failed to fetch products from server.")
            return
        prod = next((p for p in products if p["id"] == product_id), None)
        if prod:
            payload = {"id": prod["id"], "name": prod["name"], "price": prod["price"]}
            requests.post(API_URL + "/cart", json=payload)
            resp = requests.post(API_URL + "/order")
            if resp.status_code == 200:
                messagebox.showinfo("Order", f"Order placed for {prod['name']}!")
                self.show_section("orders")
            else:
                messagebox.showerror("Error", "Order failed: " + resp.json().get("error", "Unknown error"))

    def render_cart(self):
        for widget in self.cart_list.winfo_children():
            widget.destroy()
        try:
            cart = requests.get(API_URL + "/cart").json()
        except:
            cart = []
        if not cart:
            self.empty_cart_label.pack()
            self.place_order_btn.pack_forget()
            return
        self.empty_cart_label.pack_forget()
        self.place_order_btn.pack()
        for item in cart:
            frame = tk.Frame(self.cart_list, bg="white", pady=6)
            frame.pack(fill=tk.X)
            tk.Label(frame, text=item["name"], width=28, anchor="w", bg="white", font=(self.pixel_font, 10)).pack(side=tk.LEFT)
            qty_var = tk.IntVar(value=item["qty"])
            qty_entry = tk.Entry(frame, textvariable=qty_var, width=3, justify="center")
            qty_entry.pack(side=tk.LEFT, padx=8)
            def update_qty(ev=None, iid=item["id"], var=qty_var):
                try:
                    qty = int(var.get())
                    if qty < 1: qty = 1
                except:
                    qty = 1
                requests.put(API_URL + "/cart", json={"id": iid, "qty": qty})
                self.render_cart()
            qty_entry.bind("<Return>", update_qty)
            qty_entry.bind("<FocusOut>", update_qty)
            tk.Button(frame, text="Remove", bg="#222", fg="white", command=lambda iid=item["id"]: self.remove_item(iid)).pack(side=tk.LEFT, padx=8)
            tk.Label(frame, text=f"RM {item['price']*item['qty']:.2f}", width=12, anchor="e", bg="white").pack(side=tk.LEFT)

    def remove_item(self, item_id):
        requests.delete(API_URL + "/cart", json={"id": item_id})
        self.render_cart()

    def place_order(self):
        resp = requests.post(API_URL + "/order")
        if resp.status_code == 200:
            messagebox.showinfo("Order", "Order placed successfully!")
            self.render_cart()
        else:
            messagebox.showerror("Error", "Order failed: " + resp.json().get("error", "Unknown error"))

    def render_orders(self):
        for widget in self.orders_frame.winfo_children():
            widget.destroy()
        try:
            orders = requests.get(API_URL + "/orders").json()
        except:
            orders = []
        if not orders:
            tk.Label(self.orders_frame, text="No orders yet.", font=(self.pixel_font, 12), bg="white").pack(pady=30)
            return
        for order in orders:
            frame = tk.Frame(self.orders_frame, bg="#f7f7f7", bd=1, relief=tk.RIDGE)
            frame.pack(fill=tk.X, pady=7, padx=18)
            tk.Label(frame, text=f"Order #{order['order_id']}", font=(self.pixel_font, 11, "bold"), bg="#f7f7f7").pack(anchor="w", pady=(7,1), padx=7)
            for item in order["items"]:
                tk.Label(frame, text=f"- {item['name']} x {item['qty']} (RM {item['price']*item['qty']:.2f})", bg="#f7f7f7", anchor="w").pack(anchor="w", padx=22)
            cancel_btn = tk.Button(frame, text="Cancel Order", bg="red", fg="white",
                                   command=lambda oid=order['order_id']: self.cancel_order(oid))
            cancel_btn.pack(pady=(0,7), padx=7, anchor="e")
            tk.Label(frame, text="", bg="#f7f7f7").pack()

    def cancel_order(self, order_id):
        resp = requests.delete(API_URL + "/order", json={"order_id": order_id})
        if resp.status_code == 200:
            messagebox.showinfo("Canceled", "Order canceled successfully!")
        else:
            messagebox.showerror("Error", "Failed to cancel order.")
        self.render_orders()

if __name__ == "__main__":
    app = ShoeShopApp()
    app.mainloop()

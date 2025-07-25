import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel
from PIL import Image, ImageTk
import os
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from products import productsClass
from sales import salesClass
from login import Login_System
import sqlite3
import time

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')  # For Windows - maximizes the window
        self.root.title("Inventory Management System")
        self.root.configure(bg="white")

        #title
        # Open and resize the image to match heading size
        original_image = Image.open("Images/cart.jpg")

        resized_image = original_image.resize((47, 47), Image.Resampling.LANCZOS)
        self.icon_title = ImageTk.PhotoImage(resized_image)
        
        #=====title_label=====#
        if self.icon_title:
            title = tk.Label(self.root, text="Inventory Management System", image=self.icon_title, compound="left", font=("times new roman",35,"bold"), bg="#008080", fg="white", anchor="w", padx=10, pady=10, height=50)
        else:
            title = tk.Label(self.root, text="Inventory Management System", font=("times new roman",35,"bold"), bg="white", fg="black", anchor="w", padx=10, pady=10)

        #====button_logout=====#
        btn_logout=tk.Button(self.root, text="Logout", command=self.logout, font=("times new roman",15,"bold"), bg="#f56464", fg="white", cursor="hand2").place(x=1425, y=20)

        #====label_clock=====#
        self.lbl_clock=tk.Label(self.root, text="Welcome to Inventory Management System \t\t (Date: DD/MM/YYYY) \t\t (Time: HH:MM:SS)", font=("times new roman",15), bg="#b2d8d8", fg="#008080", anchor="w", padx=10, pady=10)
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        title.pack(fill=tk.X)

        #=====left_menu=====#
        original_image = Image.open("Images/leftmenu_image.jpg")
        scale_factor = 0.23 
        original_width, original_height = original_image.size
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        scaled_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(scaled_image)


        LeftMenu=tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="white")
        LeftMenu.place(x=0, y=105, width=300, height=750)

        # Create a container frame for centering
        menu_container = tk.Frame(LeftMenu, bg="white")
        menu_container.pack(expand=True, fill=tk.BOTH, padx=10, pady=20)

        lbl_menulogo=tk.Label(menu_container, image=self.MenuLogo)
        lbl_menulogo.pack(side=tk.TOP, fill=tk.X, pady=(0, 20))

        #menu label
        lbl_menu=tk.Label(menu_container, text="Menu", font=("times new roman",30), bg="#008080", fg="white").pack(side=tk.TOP, fill=tk.X, pady=(0, 20))

        #buttons
        arrow_icon = "⟶"  # Unicode right arrow

        btn_employee=tk.Button(menu_container, text=f"{arrow_icon} Employee", command=self.employee, font=("times new roman", 17), bg="#b2d8d8", fg="#008080", cursor="hand2", anchor="w", height=2).pack(side=tk.TOP, fill=tk.X, pady=5)
        btn_supplier=tk.Button(menu_container, text=f"{arrow_icon} Supplier", command=self.supplier, font=("times new roman", 17), bg="#b2d8d8", fg="#008080", cursor="hand2", anchor="w", height=2).pack(side=tk.TOP, fill=tk.X, pady=5)
        btn_category=tk.Button(menu_container, text=f"{arrow_icon} Category", command=self.category, font=("times new roman", 17), bg="#b2d8d8", fg="#008080", cursor="hand2", anchor="w", height=2).pack(side=tk.TOP, fill=tk.X, pady=5)
        btn_products=tk.Button(menu_container, text=f"{arrow_icon} Products", command=self.products, font=("times new roman", 17), bg="#b2d8d8", fg="#008080", cursor="hand2", anchor="w", height=2).pack(side=tk.TOP, fill=tk.X, pady=5)
        btn_sales=tk.Button(menu_container, text=f"{arrow_icon} Sales", command=self.sales, font=("times new roman", 17), bg="#b2d8d8", fg="#008080", cursor="hand2", anchor="w", height=2).pack(side=tk.TOP, fill=tk.X, pady=5)
        btn_exit=tk.Button(menu_container, text=f"{arrow_icon} Exit", font=("times new roman", 17), bg="#b2d8d8", fg="#008080", cursor="hand2", anchor="w", height=2).pack(side=tk.TOP, fill=tk.X, pady=5)

        #=====content=====#

        x=63
        # First row (3 boxes) - centered
        self.lbl_employee = tk.Label(self.root, text="Total Employee\n\n [ 0 ]", font=("times new roman", 20), bg="#b2d8d8", fg="#008080", bd=5, relief=tk.RIDGE, padx=10, pady=10)
        self.lbl_employee.place(x=400+x, y=150, width=275, height=200)

        self.lbl_supplier = tk.Label(self.root, text="Total Supplier\n\n [ 0 ]", font=("times new roman", 20), bg="#b2d8d8", fg="#008080", bd=5, relief=tk.RIDGE, padx=10, pady=10)
        self.lbl_supplier.place(x=725+x, y=150, width=275, height=200)

        self.lbl_category = tk.Label(self.root, text="Total Category\n\n [ 0 ]", font=("times new roman", 20), bg="#b2d8d8", fg="#008080", bd=5, relief=tk.RIDGE, padx=10, pady=10)
        self.lbl_category.place(x=1050+x, y=150, width=275, height=200)

        # Second row (2 boxes) - centered
        self.lbl_products = tk.Label(self.root, text="Total Products\n\n [ 0 ]", font=("times new roman", 20), bg="#b2d8d8", fg="#008080", bd=5, relief=tk.RIDGE, padx=10, pady=10)
        self.lbl_products.place(x=400+x, y=380, width=275, height=200)

        self.lbl_sales = tk.Label(self.root, text="Total Sales\n\n [ 0 ]", font=("times new roman", 20), bg="#b2d8d8", fg="#008080", bd=5, relief=tk.RIDGE, padx=10, pady=10)
        self.lbl_sales.place(x=725+x, y=380, width=275, height=200)

        #=====footer=====#
        footer_frame = tk.Frame(self.root, bg="#008080", height=30)
        footer_frame.place(x=0, y=860, relwidth=1)
        
        footer_text = tk.Label(footer_frame, text="© 2025 Inventory Management System. All rights reserved.", font=("times new roman", 10), bg="#008080", fg="white")
        footer_text.pack(side=tk.BOTTOM, pady=5)

        # Start the content and clock updates loop
        self.update_content()
#========================================================================================#

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def products(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productsClass(self.new_win) 
    
    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_products.config(text=f'Total Products\n[ {str(len(product))} ]')

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))} ]')

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f'Total Category\n[ {str(len(category))} ]')
            
            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f'Total Employees\n[ {str(len(employee))} ]')

            bill = len(os.listdir('bills'))
            self.lbl_sales.config(text=f'Total Sales\n[ {str(bill)} ]')

            # Update Time and Date
            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        
            self.lbl_clock.after(200, self.update_content) # Schedule this function to run again after 200ms

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



if __name__=="__main__":
    root = tk.Tk()
    obj = IMS(root)
    root.mainloop()    
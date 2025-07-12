from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile

# for print functionality
import platform
import win32api

class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+100+75")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        
        # === Create bills directory if not exists ===
        if not os.path.exists('bills'):
            os.makedirs('bills')
            
        # === Variables ===
        self.cart_list = []
        self.chk_print = 0

        # === Title ===
        try:
            original_image = Image.open("Images/cart.jpg")
            resized_image = original_image.resize((47, 47), Image.Resampling.LANCZOS)
            self.icon_title = ImageTk.PhotoImage(resized_image)   
            title_img = self.icon_title
        except FileNotFoundError:
            title_img = None

        title = Label(self.root, text="Inventory Management System", image=title_img, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#005858", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # === Logout Button ===
        btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, "bold"), command=self.logout, bg="#f56464", fg="white", cursor="hand2").place(x=1150, y=10, height=50, width=150)

        # === Clock ===
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 15), bg="#008080", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        
        #================Product Frame================
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)
        
        pTitle=Label(ProductFrame1, text="All Products", font=("times new roman", 20, "bold"), bg="#005858", fg="white").pack(side=TOP, fill=X)
        
        #==Product Search Frame==
        self.var_search=StringVar()
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)
        
        lbl_search=Label(ProductFrame2, text="Search Product | By Name", font=("times new roman", 15, "bold"), bg="white", fg="#005858").place(x=2, y=5)
        
        lbl_search=Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"), bg="white").place(x=2, y=45)
        txt_search=Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15), bg="#b2d8d8").place(x=128, y=47, width=150, height=22)
        btn_search=Button(ProductFrame2, text="Search", command=self.search, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all=Button(ProductFrame2, text="Show All", command=self.show, font=("times new roman", 15), bg="#008080", fg="white", cursor="hand2").place(x=285, y=10, width=100, height=25)
        
        #==Product Details Frame==
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=375)
        
        scrolly=Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3, orient=HORIZONTAL)
        
        self.product_Table=ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        
        self.product_Table.heading("pid", text="PID")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status", text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid", width=40)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)
        
        lbl_note=Label(ProductFrame1, text="Note: Enter 0 Quantity to remove product from the Cart", font=("times new roman", 12), anchor='w', bg="white", fg="red").pack(side=BOTTOM, fill=X)

        #==Customer Frame==
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)
        cTitle=Label(CustomerFrame, text="Customer Details", font=("times new roman", 15, "bold"), bg="#005858", fg="white").pack(side=TOP, fill=X)
        lbl_name=Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(x=5, y=35)
        txt_name=Entry(CustomerFrame, textvariable=self.var_cname, font=("times new roman", 13), bg="#b2d8d8").place(x=80, y=35, width=180)
        
        lbl_contact=Label(CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="white").place(x=270, y=35)
        txt_contact=Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman", 13), bg="#b2d8d8").place(x=380, y=35, width=140)

        #==Cal Cart Frame==
        Cal_Cart_Frame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place(x=420, y=190, width=530, height=360)

        #==Calculator Frame==
        self.var_cal_input=StringVar()
        Cal_Frame=Frame(Cal_Cart_Frame, bd=9, relief=RIDGE, bg="white")
        Cal_Frame.place(x=5, y=10, width=268, height=340)

        txt_cal_input=Entry(Cal_Frame, textvariable=self.var_cal_input, font=('arial', 15, 'bold'), width=21, bd=10, relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)
        
        btn_7=Button(Cal_Frame, text='7', font=('arial', 15, 'bold'), command=lambda:self.get_input(7), bd=5, width=4, pady=10, cursor="hand2").grid(row=1, column=0)
        btn_8=Button(Cal_Frame, text='8', font=('arial', 15, 'bold'), command=lambda:self.get_input(8), bd=5, width=4, pady=10, cursor="hand2").grid(row=1, column=1)
        btn_9=Button(Cal_Frame, text='9', font=('arial', 15, 'bold'), command=lambda:self.get_input(9), bd=5, width=4, pady=10, cursor="hand2").grid(row=1, column=2)
        btn_sum=Button(Cal_Frame, text='+', font=('arial', 15, 'bold'), command=lambda:self.get_input('+'), bd=5, width=4, pady=10, cursor="hand2").grid(row=1, column=3)
        
        btn_4=Button(Cal_Frame, text='4', font=('arial', 15, 'bold'), command=lambda:self.get_input(4), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=0)
        btn_5=Button(Cal_Frame, text='5', font=('arial', 15, 'bold'), command=lambda:self.get_input(5), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=1)
        btn_6=Button(Cal_Frame, text='6', font=('arial', 15, 'bold'), command=lambda:self.get_input(6), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=2)
        btn_sub=Button(Cal_Frame, text='-', font=('arial', 15, 'bold'), command=lambda:self.get_input('-'), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=3)
        
        btn_1=Button(Cal_Frame, text='1', font=('arial', 15, 'bold'), command=lambda:self.get_input(1), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=0)
        btn_2=Button(Cal_Frame, text='2', font=('arial', 15, 'bold'), command=lambda:self.get_input(2), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=1)
        btn_3=Button(Cal_Frame, text='3', font=('arial', 15, 'bold'), command=lambda:self.get_input(3), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=2)
        btn_mul=Button(Cal_Frame, text='*', font=('arial', 15, 'bold'), command=lambda:self.get_input('*'), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=3)
        
        btn_0=Button(Cal_Frame, text='0', font=('arial', 15, 'bold'), command=lambda:self.get_input(0), bd=5, width=4, pady=15, cursor="hand2").grid(row=4, column=0)
        btn_c=Button(Cal_Frame, text='c', font=('arial', 15, 'bold'), command=self.clear_cal, bd=5, width=4, pady=15, cursor="hand2").grid(row=4, column=1)
        btn_eq=Button(Cal_Frame, text='=', font=('arial', 15, 'bold'), command=self.perform_cal, bd=5, width=4, pady=15, cursor="hand2").grid(row=4, column=2)
        btn_div=Button(Cal_Frame, text='/', font=('arial', 15, 'bold'), command=lambda:self.get_input('/'), bd=5, width=4, pady=15, cursor="hand2").grid(row=4, column=3)

        #==Cart Frame==
        cart_Frame=Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=280, y=8, width=245, height=342)
        self.cartTitle=Label(cart_Frame, text="Cart \t Total Product: [0]", font=("times new roman", 15), bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)
        
        scrolly=Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame, orient=HORIZONTAL)
        
        self.CartTable=ttk.Treeview(cart_Frame, columns=("pid", "name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("pid", text="PID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        #==ADD Cart Widgets Frame==
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        
        Add_CartWidgetsFrame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)
        
        lbl_p_name=Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white").place(x=5, y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15), bg="#b2d8d8", state='readonly').place(x=5, y=35, width=190, height=22)
        
        lbl_p_price=Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman", 15), bg="white").place(x=230, y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15), bg="#b2d8d8", state='readonly').place(x=230, y=35, width=150, height=22)
        
        lbl_p_qty=Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(x=390, y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15), bg="#b2d8d8").place(x=390, y=35, width=120, height=22)

        self.lbl_inStock=Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)
        
        btn_clear_cart=Button(Add_CartWidgetsFrame, text="Clear", command=self.clear_cart, font=("times new roman", 15, "bold"), bg="#b2d8d8", fg="#005858", cursor="hand2").place(x=180, y=70, width=150, height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame, text="Add | Update Cart", command=self.add_update_cart, font=("times new roman", 15, "bold"), bg="#008080", fg="white", cursor="hand2").place(x=340, y=70, width=180, height=30)
        
        #==Billing Area==
        billFrame=Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=953, y=110, width=410, height=410)

        BTitle=Label(billFrame, text="Customer Bill Area", font=("times new roman", 20, "bold"), bg="#005858", fg="white").pack(side=TOP, fill=X)
        scrolly=Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_bill_area=Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #==Billing Buttons==
        billMenuFrame=Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=953, y=520, width=410, height=140)
        
        self.lbl_amnt=Label(billMenuFrame, text='Bill Amount\n[0]', font=('times new roman', 15, "bold"), bg="#b2d8d8", fg="#005858")
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)
        
        self.lbl_discount=Label(billMenuFrame, text='Discount\n[5%]', font=('times new roman', 15, "bold"), bg="#b2d8d8", fg="#005858")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)
        
        self.lbl_net_pay=Label(billMenuFrame, text='Net Pay\n[0]', font=('times new roman', 15, "bold"), bg="#b2d8d8", fg="#005858")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)
        
        # FIX: Added command to print button
        btn_print=Button(billMenuFrame, text='Print', command=self.print_bill, font=('times new roman', 15, "bold"), bg="#008080", fg="white", cursor="hand2")
        btn_print.place(x=2, y=80, width=120, height=50)
        
        btn_clear_all=Button(billMenuFrame, text='Clear All', command=self.clear_all, font=('times new roman', 15, "bold"), bg="#008080", fg="white", cursor="hand2")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate=Button(billMenuFrame, text='Generate/Save Bill', command=self.generate_bill, font=('times new roman', 12, "bold"), bg="#008080", fg="white", cursor="hand2")
        btn_generate.place(x=246, y=80, width=160, height=50)

        #==Footer==
        footer=Label(self.root, text="IMS-Inventory Management System | Developed By Me\nFor any Technical Issue contact: 987xxxxx01", font=("times new roman", 12), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)
        
        self.show()
        self.update_date_time()
        
    #================All Functions====================

    def get_input(self, num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        if result:
            try:
                self.var_cal_input.set(eval(result))
            except Exception:
                self.var_cal_input.set("Error")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE ? and status='Active'", ('%'+self.var_search.get()+'%',))
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()
            
    def get_data(self, ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
            self.var_stock.set(row[3])
            self.var_qty.set('1')

    def get_data_cart(self, ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])
            # FIX: Find stock from original cart_list to prevent IndexError
            for item in self.cart_list:
                if item[0] == row[0]: # Match by PID
                    self.var_stock.set(item[4])
                    self.lbl_inStock.config(text=f"In Stock [{str(item[4])}]")
                    break

    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error', "Please select product from the list", parent=self.root)
        elif self.var_qty.get()=='' or not self.var_qty.get().isdigit():
            messagebox.showerror('Error', "Quantity is Required and must be a number", parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error', "Invalid Quantity", parent=self.root)
        else:
            price_cal = float(self.var_price.get())
            cart_data=[self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
            
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            
            if present=='yes':
                op=messagebox.askyesno('Confirm', "Product already present\nDo you want to Update or Remove from the Cart List?", parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        # Only update quantity
                        self.cart_list[index_][3]=self.var_qty.get()
            elif int(self.var_qty.get()) > 0:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt + (float(row[2]) * int(row[3]))
        
        self.discount = (self.bill_amnt * 5) / 100
        self.net_pay = self.bill_amnt - self.discount
        self.lbl_amnt.config(text=f'Bill Amnt\n{str(round(self.bill_amnt,2))}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(round(self.net_pay,2))}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")
        
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            # FIX: Insert only the first 4 elements, as the table has 4 columns
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row[:4])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", f"Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", f"Please Add product to the Cart!!!", parent=self.root)
        else:
            # Bill Top
            self.bill_top()
            # Bill Middle (Updates product quantities)
            self.bill_middle()
            # Bill Bottom
            self.bill_bottom()

            # === Save Bill to File and Database ===
            bill_text = self.txt_bill_area.get('1.0', END)
            # Save file
            with open(f'bills/{str(self.invoice)}.txt', 'w') as fp:
                fp.write(bill_text)
            
            # MODIFICATION: Save to database
            self.save_to_db(bill_text)

            messagebox.showinfo("Saved", "Bill has been generated and saved successfully!", parent=self.root)
            self.chk_print = 1

    def save_to_db(self, bill_text):
        con = None
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            # Using the new sales table
            cur.execute("INSERT INTO sales (invoice, cname, contact, amount, net_pay, date, bill_data) VALUES (?,?,?,?,?,?,?)",
                        (self.invoice,
                         self.var_cname.get(),
                         self.var_contact.get(),
                         self.bill_amnt,
                         self.net_pay,
                         time.strftime("%d-%m-%Y"),
                         bill_text
                        ))
            con.commit()
        except Exception as ex:
            messagebox.showerror("DB Error", f"Error saving to database: {ex}", parent=self.root)
        finally:
            if con:
                con.close()

    def print_bill(self):
        if self.chk_print == 0:
            messagebox.showerror('Print Error', 'Please generate the bill first to print the receipt.', parent=self.root)
            return

        # Check if the operating system is Windows
        if platform.system() == "Windows":
            try:
                # Create a temporary file to hold the bill content
                file_path = tempfile.mktemp('.txt')
                with open(file_path, 'w') as f:
                    f.write(self.txt_bill_area.get('1.0', END))

                messagebox.showinfo('Print', 'Your bill is being sent to your default printer.', parent=self.root)
                
                # Use the reliable win32api to send the file to the printer
                win32api.ShellExecute(
                    0,          # Handle to the parent window
                    "print",    # Action to perform
                    file_path,  # Path to the file
                    None,       # Parameters
                    ".",        # Default directory
                    0           # Show command
                )
            except Exception as e:
                # Catch any error, such as no default printer configured
                messagebox.showerror('Print Error', f'Failed to print. Please ensure you have a default printer set up in Windows.\nError: {str(e)}', parent=self.root)
        else:
            # Fallback for other operating systems like macOS or Linux
            messagebox.showerror('Unsupported System', 'Automatic printing is only supported on Windows.', parent=self.root)
    
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tInventory
\t Phone No. 98725*****, Rajkot-360005
{str("="*47)}
Customer Name: {self.var_cname.get()}
Ph no. :{self.var_contact.get()}
Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Bill Amount\t\t\t\tRs.{round(self.bill_amnt, 2)}
Discount\t\t\t\tRs.{round(self.discount, 2)}
Net Pay\t\t\t\tRs.{round(self.net_pay, 2)}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)
    
    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty = int(row[3])
                stock = int(row[4])
                
                new_qty = stock - qty
                status = 'Inactive' if new_qty == 0 else 'Active'

                price = float(row[2]) * qty
                self.txt_bill_area.insert(END, f"\n {name}\t\t\t{qty}\tRs.{price:.2f}")
                
                # Update the product quantity and status in the database
                cur.execute('UPDATE product SET qty=?, status=? WHERE pid=?', (
                    new_qty,
                    status,
                    pid
                ))
            con.commit()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error in bill_middle: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text="In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.lbl_amnt.config(text='Bill Amount\n[0]')
        self.lbl_net_pay.config(text='Net Pay\n[0]')
        self.chk_print = 0
        
    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200, self.update_date_time)

    def logout(self):
        self.root.destroy()
        # The following command is not recommended for cross-platform apps
        # Consider a different approach for window management if this is an issue
        # os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
# sales.py

from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list = []
        self.var_invoice = StringVar()

        # === Title ===
        lbl_title = Label(self.root, text="View Customer Bills", font=("times new roman", 30), bg="#008080", fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_invoice = Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="white").place(x=50, y=100)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15), bg="#b2d8d8").place(x=160, y=100, width=180, height=28)

        btn_search = Button(self.root, text="Search", command=self.search, font=("times new roman", 15, "bold"), bg="#008080", fg="white", cursor="hand2").place(x=360, y=100, width=120, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15, "bold"), bg="lightgray", cursor="hand2").place(x=490, y=100, width=120, height=28)

        # === Bill List Frame ===
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List = Listbox(sales_Frame, font=("times new roman", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # === Bill Area Frame ===
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)

        lbl_title2 = Label(bill_Frame, text="Customer Bill Area", font=("times new roman", 20), fg="white", bg="#008080").pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, bg="#b2d8d8", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        self.show()

    # MODIFICATION: Fetch data from database instead of files
    def show(self):
        self.bill_area.delete('1.0', END)
        self.Sales_List.delete(0, END)
        del self.bill_list[:]
        
        con = None
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            # Fetch all invoice numbers, newest first
            cur.execute("SELECT invoice FROM sales ORDER BY invoice DESC")
            invoices = cur.fetchall()
            if invoices:
                for i in invoices:
                    self.bill_list.append(i[0])
                    self.Sales_List.insert(END, i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching bills: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    # MODIFICATION: Fetch bill text from database
    def get_data(self, ev):
        index_ = self.Sales_List.curselection()
        if index_:
            invoice_no = self.Sales_List.get(index_)
            self.bill_area.delete('1.0', END)
            
            con = None
            try:
                con = sqlite3.connect(database=r'ims.db')
                cur = con.cursor()
                cur.execute("SELECT bill_data FROM sales WHERE invoice=?", (invoice_no,))
                bill_text = cur.fetchone()
                if bill_text:
                    self.bill_area.insert(END, bill_text[0])
            except Exception as ex:
                messagebox.showerror("Error", f"Error retrieving bill: {str(ex)}", parent=self.root)
            finally:
                if con:
                    con.close()

    # MODIFICATION: Search database for the invoice
    def search(self):
        query = self.var_invoice.get().strip()
        if query == "":
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
            return

        con = None
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT bill_data FROM sales WHERE invoice=?", (query,))
            bill_text = cur.fetchone()
            if bill_text:
                self.bill_area.delete('1.0', END)
                self.bill_area.insert(END, bill_text[0])
                
                # Highlight the found invoice in the listbox
                self.Sales_List.delete(0, END)
                self.Sales_List.insert(END, query)

            else:
                messagebox.showerror("Error", "No invoice found with that number.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error searching: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.close()

    def clear(self):
        self.var_invoice.set("")
        self.show() # Reload all bills

if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
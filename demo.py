# Import modules
from tkinter import *
from tkinter import ttk
import datetime as dt
import csv
from mydb1 import Database
from tkinter import messagebox
from tkinter.simpledialog import askstring

# Initialize database object
db = Database(db='test.db')

# Global variables
selected_row_id = None


# Functions
def save_record():
    """Save a new record to the database."""
    try:
        db.insertRecord(
            item_name=item_name_var.get(),
            item_price=item_price_var.get(),
            purchase_date=purchase_date_var.get()
        )
        clear_entries()
        refresh_data()
    except Exception as e:
        messagebox.showerror('Error', str(e))


def set_current_date():
    """Set the current date in the date entry."""
    current_date = dt.datetime.now()
    purchase_date_var.set(f'{current_date:%d %B %Y}')


def clear_entries():
    """Clear all entry fields."""
    item_name_var.set('')
    item_price_var.set('')
    purchase_date_var.set('')


def fetch_records(query="SELECT rowid, * FROM expense_record"):
    """Fetch and display records from the database."""
    global selected_row_id
    records = db.fetchRecord(query)
    for idx, record in enumerate(records):
        tv.insert(parent='', index='end', iid=idx, values=record)
    tv.after(400, refresh_data)


def select_record(event):
    """Select a record from the Treeview and populate the entry fields."""
    global selected_row_id
    selected_item = tv.focus()
    values = tv.item(selected_item, 'values')

    try:
        selected_row_id = values[0]
        item_name_var.set(values[1])
        item_price_var.set(values[2])
        purchase_date_var.set(values[3])
    except Exception as e:
        messagebox.showerror('Error', str(e))


def update_record():
    """Update the selected record."""
    global selected_row_id
    try:
        db.updateRecord(
            item_name=item_name_var.get(),
            item_price=item_price_var.get(),
            purchase_date=purchase_date_var.get(),
            row_id=selected_row_id
        )
        selected_item = tv.focus()
        tv.item(selected_item,
                values=(selected_row_id, item_name_var.get(), item_price_var.get(), purchase_date_var.get()))
        clear_entries()
        refresh_data()
    except Exception as e:
        messagebox.showerror('Error', str(e))


def show_total_balance():
    """Show the total balance and remaining balance."""
    try:
        records = db.fetchRecord("SELECT SUM(item_price) FROM expense_record")
        total_expense = records[0][0] or 0
        balance_remaining = 5000 - total_expense
        messagebox.showinfo('Balance', f"Total Expense: {total_expense}\nBalance Remaining: {balance_remaining}")
    except Exception as e:
        messagebox.showerror('Error', str(e))


def delete_record():
    """Delete the selected record."""
    global selected_row_id
    try:
        if selected_row_id is not None:
            db.removeRecord(selected_row_id)
            refresh_data()
            clear_entries()
        else:
            messagebox.showwarning('Select Record', 'No record selected to delete.')
    except Exception as e:
        messagebox.showerror('Error', str(e))


def refresh_data():
    """Refresh the data in the Treeview."""
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()


def search_records():
    """Search records by item name or date."""
    search_term = askstring('Search', 'Enter item name or date (dd MMMM yyyy):')
    if search_term:
        query = f"SELECT rowid, * FROM expense_record WHERE item_name LIKE '%{search_term}%' OR purchase_date LIKE '%{search_term}%'"
        refresh_data_with_query(query)


def export_to_csv():
    """Export records to a CSV file."""
    try:
        with open('expense_records.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Serial No", "Item Name", "Item Price", "Purchase Date"])
            for record in db.fetchRecord("SELECT * FROM expense_record"):
                writer.writerow(record)
        messagebox.showinfo('Export Success', 'Records have been exported to expense_records.csv')
    except Exception as e:
        messagebox.showerror('Error', str(e))


def view_summary():
    """Show a summary report of records."""
    records = db.fetchRecord("SELECT COUNT(*), SUM(item_price) FROM expense_record")
    total_records, total_expense = records[0]
    summary = f"Total Records: {total_records}\nTotal Expense: {total_expense}"
    messagebox.showinfo('Summary Report', summary)


def refresh_data_with_query(query):
    """Refresh data with a specific query."""
    for item in tv.get_children():
        tv.delete(item)
    fetch_records(query)


def filter_by_date_range():
    """Filter records based on a date range."""
    start_date = askstring('Start Date', 'Enter start date (dd MMMM yyyy):')
    end_date = askstring('End Date', 'Enter end date (dd MMMM yyyy):')
    if start_date and end_date:
        query = f"SELECT rowid, * FROM expense_record WHERE purchase_date BETWEEN '{start_date}' AND '{end_date}'"
        refresh_data_with_query(query)


# Create tkinter object
app = Tk()
app.title('Daily Expense Tracker')

# Variables
font = ('Times New Roman', 14)
item_name_var = StringVar()
item_price_var = IntVar()
purchase_date_var = StringVar()

# Frames
input_frame = Frame(app, padx=10, pady=10)
input_frame.pack(expand=True, fill=BOTH)

tree_frame = Frame(app)
tree_frame.pack()

# Labels
Label(input_frame, text='Item Name', font=font).grid(row=0, column=0, sticky=W)
Label(input_frame, text='Item Price', font=font).grid(row=1, column=0, sticky=W)
Label(input_frame, text='Purchase Date', font=font).grid(row=2, column=0, sticky=W)

# Entries
Entry(input_frame, font=font, textvariable=item_name_var).grid(row=0, column=1, sticky=EW, padx=10)
Entry(input_frame, font=font, textvariable=item_price_var).grid(row=1, column=1, sticky=EW, padx=10)
Entry(input_frame, font=font, textvariable=purchase_date_var).grid(row=2, column=1, sticky=EW, padx=10)

# Buttons
Button(input_frame, text='Current Date', font=font, bg='#04C4D9', command=set_current_date).grid(row=3, column=1,
                                                                                                 sticky=EW, padx=10)
Button(input_frame, text='Save Record', font=font, bg='#42602D', fg='white', command=save_record).grid(row=0, column=2,
                                                                                                       sticky=EW,
                                                                                                       padx=10)
Button(input_frame, text='Clear Entry', font=font, bg='#D9B036', fg='white', command=clear_entries).grid(row=1,
                                                                                                         column=2,
                                                                                                         sticky=EW,
                                                                                                         padx=10)
Button(input_frame, text='Exit', font=font, bg='#D33532', fg='white', command=app.quit).grid(row=2, column=2, sticky=EW,
                                                                                             padx=10)
Button(input_frame, text='Total Balance', font=font, bg='#486966', command=show_total_balance).grid(row=0, column=3,
                                                                                                    sticky=EW, padx=10)
Button(input_frame, text='Update', font=font, bg='#C2BB00', command=update_record).grid(row=1, column=3, sticky=EW,
                                                                                        padx=10)
Button(input_frame, text='Delete', font=font, bg='#BD2A2E', command=delete_record).grid(row=2, column=3, sticky=EW,
                                                                                        padx=10)
Button(input_frame, text='Search', font=font, command=search_records).grid(row=3, column=2, sticky=EW, padx=10)
Button(input_frame, text='Export to CSV', font=font, command=export_to_csv).grid(row=4, column=2, sticky=EW, padx=10)
Button(input_frame, text='View Summary', font=font, command=view_summary).grid(row=4, column=3, sticky=EW, padx=10)
Button(input_frame, text='Filter by Date Range', font=font, command=filter_by_date_range).grid(row=5, column=2,
                                                                                               sticky=EW, padx=10)

# Treeview
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

# Define columns
tv.column(1, anchor=CENTER, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial No")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# Binding
tv.bind("<ButtonRelease-1>", select_record)

# Style
style = ttk.Style()
style.theme_use("default")

# Vertical scrollbar
scrollbar = Scrollbar(tree_frame, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# Fetch records on start
fetch_records()

# Run the app
app.mainloop()

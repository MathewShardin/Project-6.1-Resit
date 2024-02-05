import time
import tkinter as tk
from tkinter import ttk
import requests
from src.base_application.admin.adminLogin import login_admin_page
from src.base_application import api_server_ip
from xml.etree import ElementTree as ET



def create_window():
    selected_row = None
    protocol_retrieve = "JSON"
    """Create a Tkinter window with two equal sections."""
    # Create the main window
    root = tk.Tk()
    root.title("Sports Accounting - Register a user")
    root.geometry("1200x900")

    # Get balance from db
    balance = "No data"
    response = requests.get(api_server_ip + "/api/getFile")
    if len(response.json()) != 0:
        balance = response.json()[0][4]

    def admin_login_button_click():
        root.destroy()
        login_admin_page()

    # Define a function to be called when a row of the table is clicked
    def on_click_table_row(event):
        global selected_row
        # Get the selected item
        item = table.selection()[0]
        # Get the values of the selected item
        values = table.item(item, "values")
        selected_row = values[0]

    def edit_button_click():
        global selected_row
        if selected_row is None:
            return
        root.destroy()
        from editTransaction import edit_transaction_page
        edit_transaction_page(selected_row)

    def details_button_click():
        global selected_row
        if selected_row is None:
            return
        from src.base_application.app_pages.transactionDetails import transaction_details
        transaction_details(selected_row)

    root.resizable(False, False)  # Prevent the window from being resized

    # Create a frame to hold the left section
    left_frame = tk.Frame(root, width=600, height=900, bg="#D9D9D9")  # Set the background color to grey
    left_frame.pack(side="left")

    # Create a label and text area for the User Panel
    label = tk.Label(left_frame, text="User Panel", font=("Inter", 24, "normal"), bg="#D9D9D9", fg="#000000",
                     justify="left")
    label.place(x=20, y=20, width=190, height=50)

    # Create a label and text area for the Welcome message
    label = tk.Label(left_frame, text="Welcome", font=("Inter", 18, "bold"), bg="#D9D9D9", fg="#000000", justify="left",
                     underline=len("Welcome"))
    label.place(x=30, y=200, width=190, height=50)

    # Create a label and text area for the keyword
    entry = tk.Entry(left_frame, font=("Inter", 14))
    entry.place(x=70, y=300, width=280, height=24)

    style = ttk.Style()
    style.configure("RoundedButton.TButton", padding=6, relief="flat",
                    background="#000000", foreground="#FFFFFF",
                    font=("Inter", 14), borderwidth=0, bordercolor="#000000")
    style.map("RoundedButton.TButton", background=[("active", "#333333")])


    style = ttk.Style()
    style.configure("RoundedButton.TButton", padding=6, relief="flat",
                    background="#000000", foreground="#FFFFFF",
                    font=("Inter", 14), borderwidth=0, bordercolor="#000000")
    style.map("RoundedButton.TButton", background=[("active", "#333333")])

    button2 = ttk.Button(left_frame, text="Admin Login",
                         command=admin_login_button_click)

    button2.place(x=250, y=400, width=150, height=24)

    balance_label = tk.Label(left_frame, text="Available Balance:", font=("Inter", 15), bg="#D9D9D9", fg="#000000", justify="left")
    balance_label.place(x=70, y=500, width=160, height=24)

    balance_number = tk.Label(left_frame, text=balance, font=("Inter", 15), bg="#D9D9D9", fg="#000000", justify="left")
    balance_number.place(x=250, y=500, width=160, height=24)

    search_balance_label = tk.Label(left_frame, text="Sum of found transactions:", font=("Inter", 15), bg="#D9D9D9", fg="#000000", justify="left")
    search_balance_label.place(x=70, y=600, width=240, height=24)

    search_summary_num = tk.Label(left_frame, text="", font=("Inter", 15), bg="#D9D9D9", fg="#000000", justify="left")
    search_summary_num.pack_forget()

    # Create a frame to hold the right section
    right_frame = tk.Frame(root, width=600, height=900, bg="#F0AFAF")
    # Set the background color to pink
    right_frame.pack(side="right")  # Add padding to prevent overlap

    # Create a Treeview widget to display the table
    table = ttk.Treeview(right_frame, columns=("ID", "Date", "Details", "Description", "Ref", "Amount"),
                         show="headings", style="Custom.Treeview")
    table.heading("ID", text="ID")
    table.heading("Date", text="Date")
    table.heading("Details", text="Company Name")
    table.heading("Description", text="Description")
    table.heading("Ref", text="Ref")
    table.heading("Amount", text="Amount")


    # Looping through the columns and get the heading
    for column in table["columns"]:
        # Assigning the heading as text of the column
        table.heading(column, text=column, command=lambda: None)

    # Apply the background color to the entire table
    style = ttk.Style()
    style.configure("Custom.Treeview", background="#F0AFAF", rowheight=30)

    table.column("ID", width=20)  # Set width of column zero
    table.column("Date", width=100)  # Set the width of the first column
    table.column("Details", width=200)  # Set the width of the second column
    table.column("Description", width=100)  # Set the width of the third column
    table.column("Ref", width=50)  # Set the width of the forth column
    table.column("Amount", width=100)  # Set the width of the fifth
    table.config(height=20)  # Set the height of the table to 10 rows

    # Get data from DB using XML or JSON based on user choice
    rows = retrieveDB(protocol_retrieve)

    # # Clear existing rows in the table
    table.delete(*table.get_children())

    # Insert retrieved data into the table
    if rows is not None:
        for row in rows:
            table.insert("", "end", values=row)

    # Pack the table into the frame and center it horizontally
    table.pack(fill="both", expand=False)  # Fill the frame with the table
    table.place(x=15, y=100)  # Place the table 15 pixels from the left and 100 pixels from the top
    table.bind("<ButtonRelease-1>", on_click_table_row, "+") # Bind row selection
    right_frame.pack_propagate(False)  # Prevent the frame from resizing to fit the table

    edit_button = ttk.Button(right_frame, text="Edit", command=lambda: edit_button_click())
    edit_button.place(x=15, y=35, width=100, height=30)

    details_button = ttk.Button(right_frame, text="Details", command=lambda: details_button_click())
    details_button.place(x=485, y=35, width=100, height=30)

    button1 = ttk.Button(left_frame, text="Keyboard Search", command=lambda: keyword_search_button(entry.get(), table, search_summary_num))
    button1.place(x=70, y=400, width=150, height=24)

    # Creating JSON and XML buttons
    # Create a style for the radio buttons
    style = ttk.Style()
    style.configure("TRadiobutton", font=("Inter", 18), background="#F0AFAF", borderwidth=0)

    # Create a frame to hold the radio buttons
    radio_frame = tk.Frame(right_frame, bg="#F0AFAF")
    radio_frame.place(x=0, y=700, width=600, height=100)

    # Set "JSON" as the default selection
    format_var = tk.StringVar(value=protocol_retrieve)

    # Create the radio buttons
    json_radio = ttk.Radiobutton(radio_frame, text="JSON", value="JSON", variable=format_var,
                                 command=lambda: radio_button_update("JSON"))
    xml_radio = ttk.Radiobutton(radio_frame, text="XML", value="XML", variable=format_var,
                                command=lambda: radio_button_update("XML"))

    # Pack the radio buttons (left and right)
    json_radio.pack(side="left", padx=100)
    xml_radio.pack(side="right", padx=100)

    def radio_button_update(protocol):
        global protocol_retrieve
        if protocol == "JSON":
            protocol_retrieve = "JSON"
        else:
            protocol_retrieve = "XML"
        clear_table(table)
        update_table(table)

    def on_closing():
        root.destroy()

    def keyword_search_button(keyword, table, widget):
        # Clear existing rows in the table
        table.delete(*table.get_children())
        # Show all transactions if keyword entry field is empty
        if len(keyword) == 0:
            # Get data from DB using XML or JSON based on user choice
            keyword_table = retrieveDB(protocol_retrieve)
            widget.config(text="")
        else:
            keyword_table = retrieveDB_keyword_search(keyword)
            sum_output = 0
            # Calculate total sum of money per keyword
            for tuple_entry in keyword_table:
                sum_output = sum_output + float(tuple_entry[5])
            widget.config(text=str(sum_output))
            widget.place(x=310, y=600, width=350, height=24)

        # Insert retrieved data into the table
        for result in keyword_table:
            table.insert("", "end", values=result)

    def update_table(table_inp):
        global protocol_retrieve
        rows = retrieveDB(protocol_retrieve)
        if len(rows) == 0:
            return
        # Insert retrieved data into the table
        for result in rows:
            table_inp.insert("", "end", values=result)

    def clear_table(table_inp):
        # Clear input
        entry.delete(first=0, last=255)
        # Remove the sum per search label if table is updated
        search_summary_num.config(text="")
        # Clear existing rows in the table
        table_inp.delete(*table_inp.get_children())



    # Bind the on_closing function to the window close event
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the main event loop
    root.mainloop()


def retrieveDB_JSON():
    response = requests.get(api_server_ip + "/api/getTransactionsSQL")
    if len(response.json()) == 0:
        return

    # Convert JSON object into an array of tuples
    rows_out = []
    for entry in response.json():
        temp_tuple = (entry[0], entry[6], entry[2], entry[3], entry[1], entry[4])
        rows_out.append(tuple(temp_tuple))

    print('Using JSON')
    return rows_out


def retrieveDB_XML():
    response = requests.get(api_server_ip + "/api/getTransactionsSQLXML")
    # Check if the request was not successful
    if response.status_code != 200:
        return

    # Parse XML response
    xml_str = response.content.decode('utf-8')  # Decode the bytes received
    root = ET.fromstring(xml_str)

    # Check if the XML file is not empty
    if len(root) == 0:
        return

    # Convert XML object into an array of tuples to display in table
    rows_out = []
    for entry in root.findall('transaction'):
        trans_id = int(entry.findtext('transactionid'))
        date = entry.findtext('transaction_date')
        details = entry.findtext('transactiondetail')
        desc = entry.findtext('description')
        ref = entry.findtext('refrencenumber')
        amount = entry.findtext('amount')
        temp_tuple = (trans_id, date, details, desc, ref, amount)
        rows_out.append(tuple(temp_tuple))
    print('Using XML')
    return rows_out


def retrieveDB_keyword_search(keyword):
    response = requests.get(api_server_ip + "/api/searchKeyword/" + str(keyword))
    if len(response.json()) == 0:
        return

    # Convert JSON object into an array of tuples
    rows_out = []
    for entry in response.json():
        temp_tuple = (entry[0], entry[6], entry[2], entry[3], entry[1], entry[4])
        rows_out.append(tuple(temp_tuple))

    return rows_out


def retrieveDB(protocol):
    if protocol == "JSON":
        output = retrieveDB_JSON()
    else:
        output = retrieveDB_XML()
    return output
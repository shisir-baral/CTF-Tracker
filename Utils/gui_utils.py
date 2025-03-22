import tkinter as tk
from tkinter import ttk, messagebox
from Utils import db_utils

class CTFTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CTF Contribution Tracker")
        self.root.geometry("900x650")
        self.conn = db_utils.init_db()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create frames for each tab
        self.add_contribution_frame = ttk.Frame(self.notebook)
        self.add_user_frame = ttk.Frame(self.notebook)
        self.add_ctf_frame = ttk.Frame(self.notebook)
        self.view_contributions_frame = ttk.Frame(self.notebook)
        self.view_users_frame = ttk.Frame(self.notebook)
        self.view_ctfs_frame = ttk.Frame(self.notebook)
        self.delete_entries_frame = ttk.Frame(self.notebook)
        
        # Add frames to notebook
        self.notebook.add(self.add_contribution_frame, text="Add Contribution")
        self.notebook.add(self.add_user_frame, text="Add User")
        self.notebook.add(self.add_ctf_frame, text="Add CTF")
        self.notebook.add(self.view_contributions_frame, text="View Contributions")
        self.notebook.add(self.view_users_frame, text="View Users")
        self.notebook.add(self.view_ctfs_frame, text="View CTFs")
        self.notebook.add(self.delete_entries_frame, text="Delete Entries")
        
        # Set up each tab's content
        self.setup_add_contribution_tab()
        self.setup_add_user_tab()
        self.setup_add_ctf_tab()
        self.setup_view_contributions_tab()
        self.setup_view_users_tab()
        self.setup_view_ctfs_tab()
        self.setup_delete_entries_tab()
    
    def setup_add_contribution_tab(self):
        frame = self.add_contribution_frame
        
        # User dropdown
        ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_var = tk.StringVar()
        self.username_dropdown = ttk.Combobox(frame, textvariable=self.username_var)
        self.username_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.update_username_dropdown()
        
        # CTF dropdown
        ttk.Label(frame, text="CTF Name:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ctf_name_var = tk.StringVar()
        self.ctf_dropdown = ttk.Combobox(frame, textvariable=self.ctf_name_var)
        self.ctf_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.update_ctf_dropdown()
        
        # CTF Score
        ttk.Label(frame, text="CTF Score:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.ctf_score_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.ctf_score_var).grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Submit button
        ttk.Button(frame, text="Add Contribution", command=self.submit_contribution).grid(row=4, column=0, columnspan=2, pady=20)
        
        # Configure grid
        frame.columnconfigure(1, weight=1)
    
    def setup_add_user_tab(self):
        frame = self.add_user_frame
        
        # Username
        ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.new_username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.new_username_var).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # NetID
        ttk.Label(frame, text="NetID:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.netid_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.netid_var).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Submit button
        ttk.Button(frame, text="Add User", command=self.submit_user).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Configure grid
        frame.columnconfigure(1, weight=1)
    
    def setup_add_ctf_tab(self):
        frame = self.add_ctf_frame
        
        # CTF Name
        ttk.Label(frame, text="CTF Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.new_ctf_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.new_ctf_name_var).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # CTFtime Score
        ttk.Label(frame, text="CTFtime Score:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.new_ctftime_score_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.new_ctftime_score_var).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Submit button
        ttk.Button(frame, text="Add CTF Event", command=self.submit_ctf).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Configure grid
        frame.columnconfigure(1, weight=1)
    
    def setup_view_contributions_tab(self):
        frame = self.view_contributions_frame
        
        # Create treeview
        columns = ("ID", "Username", "NetID", "CTF Name", "CTF Score", "CTFtime Score", "Total Value")
        self.contributions_tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.contributions_tree.heading(col, text=col)
            self.contributions_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.contributions_tree.yview)
        self.contributions_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.contributions_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Refresh button
        ttk.Button(frame, text="Refresh", command=self.refresh_contributions).pack(side="bottom", pady=10)
        
        # Load data
        self.refresh_contributions()
    
    def setup_view_users_tab(self):
        frame = self.view_users_frame
        
        # Create treeview
        columns = ("NetID", "Username")
        self.users_tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.users_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Refresh button
        ttk.Button(frame, text="Refresh", command=self.refresh_users).pack(side="bottom", pady=10)
        
        # Load data
        self.refresh_users()
    
    def setup_view_ctfs_tab(self):
        frame = self.view_ctfs_frame
        
        # Create treeview
        columns = ("ID", "CTF Name", "CTFtime Score")
        self.ctfs_tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.ctfs_tree.heading(col, text=col)
            self.ctfs_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.ctfs_tree.yview)
        self.ctfs_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.ctfs_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Refresh button
        ttk.Button(frame, text="Refresh", command=self.refresh_ctfs).pack(side="bottom", pady=10)
        
        # Load data
        self.refresh_ctfs()
    
    def setup_delete_entries_tab(self):
        frame = self.delete_entries_frame
        
        # Search frame
        search_frame = ttk.LabelFrame(frame, text="Search Criteria")
        search_frame.pack(fill="x", padx=10, pady=10, expand=False)
        
        # Username search
        ttk.Label(search_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.search_username_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_username_var).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # NetID search
        ttk.Label(search_frame, text="NetID:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.search_netid_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_netid_var).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # CTF name search
        ttk.Label(search_frame, text="CTF Name:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.search_ctf_name_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_ctf_name_var).grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Search button
        ttk.Button(search_frame, text="Search", command=self.search_entries).grid(row=3, column=0, columnspan=2, pady=10)
        
        search_frame.columnconfigure(1, weight=1)
        
        # Results frame
        results_frame = ttk.LabelFrame(frame, text="Search Results")
        results_frame.pack(fill="both", padx=10, pady=10, expand=True)
        
        # Create treeview for results
        columns = ("ID", "Username", "NetID", "CTF Name", "CTF Score", "CTFtime Score", "Total Value")
        self.search_results_tree = ttk.Treeview(results_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.search_results_tree.heading(col, text=col)
            self.search_results_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.search_results_tree.yview)
        self.search_results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.search_results_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Delete button
        delete_frame = ttk.Frame(frame)
        delete_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(delete_frame, text="Delete Selected Entry", command=self.delete_selected_entry).pack(side="left", padx=5)
        ttk.Button(delete_frame, text="Clear Results", command=self.clear_search_results).pack(side="left", padx=5)
    
    def submit_contribution(self):
        username = self.username_var.get()
        ctf_name = self.ctf_name_var.get()
        
        try:
            ctf_score = float(self.ctf_score_var.get())
        except ValueError:
            messagebox.showerror("Error", "CTF Score must be a numeric value")
            return
        
        if not username or not ctf_name:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, message = db_utils.add_contribution(self.conn, username, ctf_name, ctf_score)
        
        if success:
            messagebox.showinfo("Success", message)
            # Clear fields
            self.ctf_score_var.set("")
            # Refresh data
            self.refresh_contributions()
        else:
            messagebox.showerror("Error", message)
    
    def submit_user(self):
        username = self.new_username_var.get()
        netid = self.netid_var.get()
        
        if not username or not netid:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        result = db_utils.add_user(self.conn, username, netid)
        
        if result:
            messagebox.showinfo("Success", "User added successfully")
            # Clear fields
            self.new_username_var.set("")
            self.netid_var.set("")
            # Refresh data
            self.refresh_users()
            self.update_username_dropdown()
        else:
            messagebox.showinfo("Information", f"User with NetID '{netid}' already exists")
    
    def submit_ctf(self):
        ctf_name = self.new_ctf_name_var.get()
        
        try:
            ctftime_score = float(self.new_ctftime_score_var.get())
        except ValueError:
            messagebox.showerror("Error", "CTFtime Score must be a numeric value")
            return
        
        if not ctf_name:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        result = db_utils.add_ctf_event(self.conn, ctf_name, ctftime_score)
        
        if result:
            messagebox.showinfo("Success", "CTF event added successfully")
            # Clear fields
            self.new_ctf_name_var.set("")
            self.new_ctftime_score_var.set("")
            # Refresh data
            self.refresh_ctfs()
            self.update_ctf_dropdown()
        else:
            messagebox.showinfo("Information", f"CTF event '{ctf_name}' already exists")
    
    def refresh_contributions(self):
        # Clear existing data
        for item in self.contributions_tree.get_children():
            self.contributions_tree.delete(item)
        
        # Get and insert new data
        contributions = db_utils.get_all_contributions(self.conn)
        for contrib in contributions:
            self.contributions_tree.insert("", "end", values=contrib)
    
    def refresh_users(self):
        # Clear existing data
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Get and insert new data
        users = db_utils.get_all_users(self.conn)
        for user in users:
            self.users_tree.insert("", "end", values=user)
    
    def refresh_ctfs(self):
        # Clear existing data
        for item in self.ctfs_tree.get_children():
            self.ctfs_tree.delete(item)
        
        # Get and insert new data
        ctfs = db_utils.get_all_ctf_events(self.conn)
        for ctf in ctfs:
            self.ctfs_tree.insert("", "end", values=ctf)
    
    def update_username_dropdown(self):
        users = db_utils.get_all_users(self.conn)
        usernames = [user[1] for user in users]  # Extract usernames
        self.username_dropdown['values'] = usernames

    def update_ctf_dropdown(self):
        ctfs = db_utils.get_all_ctf_events(self.conn)
        ctf_names = [ctf[1] for ctf in ctfs]  # Extract CTF names
        self.ctf_dropdown['values'] = ctf_names
    
    def search_entries(self):
        # Clear existing results
        for item in self.search_results_tree.get_children():
            self.search_results_tree.delete(item)
        
        # Get search criteria
        username = self.search_username_var.get()
        netid = self.search_netid_var.get()
        ctf_name = self.search_ctf_name_var.get()
        
        # Search for entries
        results = db_utils.search_contributions(self.conn, username, netid, ctf_name)
        
        # Display results
        for result in results:
            self.search_results_tree.insert("", "end", values=result)
        
        if not results:
            messagebox.showinfo("Search Results", "No entries found matching your criteria.")
    
    def delete_selected_entry(self):
        selected_item = self.search_results_tree.selection()
        if not selected_item:
            messagebox.showinfo("Delete", "Please select an entry to delete")
            return
        
        # Get the ID of the selected entry
        entry_id = self.search_results_tree.item(selected_item[0], "values")[0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", 
                                      "Are you sure you want to delete this entry? This action cannot be undone.")
        if not confirm:
            return
        
        # Delete the entry
        success = db_utils.delete_contribution(self.conn, entry_id)
        
        if success:
            messagebox.showinfo("Success", "Entry deleted successfully")
            # Remove from the treeview
            self.search_results_tree.delete(selected_item)
            # Refresh the main contributions view
            self.refresh_contributions()
        else:
            messagebox.showerror("Error", "Failed to delete entry")
    
    def clear_search_results(self):
        # Clear all search results
        for item in self.search_results_tree.get_children():
            self.search_results_tree.delete(item)
        
        # Clear search criteria fields
        self.search_username_var.set("")
        self.search_netid_var.set("")
        self.search_ctf_name_var.set("")

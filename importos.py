import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import json
import os

# File paths
PROFILES_FILE = "profiles.json"

# Function to load profiles from JSON file
def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save profiles to JSON file
def save_to_json(profiles, filename):
    with open(filename, "w") as file:
        json.dump(profiles, file, indent=4)

# Initialize profiles
profiles = load_profiles()

# Function to create a new profile
def create_profile_window():
    create_window = tk.Toplevel()
    create_window.title("Create New Profile")

    tk.Label(create_window, text="Profile Name:").pack(pady=10)
    name_entry = tk.Entry(create_window)
    name_entry.pack()

    def save_profile():
        profile_name = name_entry.get()
        if not profile_name:
            messagebox.showwarning("Input Error", "Profile name cannot be empty.")
            return

        if any(p['name'] == profile_name for p in profiles):
            messagebox.showwarning("Profile Exists", f"Profile '{profile_name}' already exists.")
            return

        new_profile = {
            'name': profile_name,
            'vehicles': [],
            'contacts': [],
        }
        profiles.append(new_profile)
        save_to_json(profiles, PROFILES_FILE)
        profiles_listbox.insert(tk.END, profile_name)
        create_window.destroy()

    tk.Button(create_window, text="Save Profile", command=save_profile).pack(pady=10)

# Function to delete a highlighted profile
def delete_profile():
    selected_index = profiles_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Selection Error", "No profile selected.")
        return

    selected_index = selected_index[0]
    selected_profile = profiles[selected_index]
    
    # Confirm profile deletion
    confirm = messagebox.askyesno("Delete Profile", f"Are you sure you want to delete '{selected_profile['name']}'?")
    if confirm:
        profiles.pop(selected_index)
        save_to_json(profiles, PROFILES_FILE)
        
        # Update the listbox
        profiles_listbox.delete(selected_index)
        update_selected_profile_labels()  # Clear the labels after deletion

def open_real_estate_window(profile_name):
    profile = next((p for p in profiles if isinstance(p, dict) and p['name'] == profile_name), None)
    if not profile:
        messagebox.showwarning("Profile Not Found", f"Profile '{profile_name}' not found.")
        return

    real_estate_window = tk.Toplevel()
    real_estate_window.title(f"real_estate for Profile: {profile_name}")

    real_estate_list = tk.Listbox(real_estate_window, width=50, height=20)
    real_estate_list.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar = tk.Scrollbar(real_estate_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    real_estate_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=real_estate_list.yview)

    def print_real_estate():
        real_estate_list.delete(0, tk.END)
        for real_estate in profile.get('real_estate', []):
            real_estate_info = f"Name: {real_estate['name']}, Email: {real_estate.get('email', '')}, Phone: {real_estate.get('phone', '')}"
            real_estate_list.insert(tk.END, real_estate_info)

    def add_real_estate():
        add_real_estate_window = tk.Toplevel()
        add_real_estate_window.title("Add real_estate")

        tk.Label(add_real_estate_window, text="Name:").pack(pady=10)
        name_entry = tk.Entry(add_real_estate_window)
        name_entry.pack()

        tk.Label(add_real_estate_window, text="Email Address:").pack(pady=10)
        email_entry = tk.Entry(add_real_estate_window)
        email_entry.pack()

        tk.Label(add_real_estate_window, text="Phone Number:").pack(pady=10)
        phone_entry = tk.Entry(add_real_estate_window)
        phone_entry.pack()

        def save_real_estate():
            if 'real_estate' not in profile:
                profile['real_estate'] = []  # Initialize 'real_estate' list if it doesn't exist
            real_estate = {
                'name': name_entry.get(),
                'email': email_entry.get(),
                'phone': phone_entry.get()
            }
            profile['real_estate'].append(real_estate)
            save_to_json(profiles, PROFILES_FILE)
            messagebox.showinfo("Success", "real_estate added successfully!")
            print_real_estate()  # Update the real_estate listbox after adding a new real_estate
            add_real_estate_window.destroy()

        tk.Button(add_real_estate_window, text="Save real_estate", command=save_real_estate).pack(pady=20)


    def edit_real_estate():
        selected_index = real_estate_list.curselection()
        if selected_index:
            selected_real_estate = profile['real_estate'][selected_index[0]]
            edit_real_estate_window = tk.Toplevel()
            edit_real_estate_window.title("Edit real_estate")

            tk.Label(edit_real_estate_window, text="Name:").pack(pady=10)
            name_entry_edit = tk.Entry(edit_real_estate_window)
            name_entry_edit.insert(0, selected_real_estate['name'])
            name_entry_edit.pack()

            tk.Label(edit_real_estate_window, text="Email Address:").pack(pady=10)
            email_entry_edit = tk.Entry(edit_real_estate_window)
            email_entry_edit.insert(0, selected_real_estate.get('email', ''))
            email_entry_edit.pack()

            tk.Label(edit_real_estate_window, text="Phone Number:").pack(pady=10)
            phone_entry_edit = tk.Entry(edit_real_estate_window)
            phone_entry_edit.insert(0, selected_real_estate.get('phone', ''))
            phone_entry_edit.pack()

            def save_changes():
                selected_real_estate['name'] = name_entry_edit.get()
                selected_real_estate['email'] = email_entry_edit.get()
                selected_real_estate['phone'] = phone_entry_edit.get()
                save_to_json(profiles, PROFILES_FILE)
                messagebox.showinfo("Success", "real_estate updated successfully!")
                print_real_estate()  # Update the real_estate listbox after editing a real_estate
                edit_real_estate_window.destroy()

            tk.Button(edit_real_estate_window, text="Save Changes", command=save_changes).pack(pady=20)
        else:
            messagebox.showwarning("No real_estate Selected", "Please select a real_estate to edit.")

    def generate_pdf():
        pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_filename:
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.drawString(100, 750, f"Profile Information for: {profile_name}")
            y_position = 720

            # Print profile details
            for key, value in profile.items():
                if key == 'real_estate':
                    continue  # Skip printing real_estate here
                if isinstance(value, list) or isinstance(value, dict):
                    value = json.dumps(value, indent=4)
                profile_info = f"{key}: {value}"
                c.drawString(100, y_position, profile_info)
                y_position -= 20

            # Print real_estate information
            c.drawString(100, y_position, "real_estate:")
            y_position -= 20
            for real_estate in profile.get('real_estate', []):
                real_estate_info = f"Name: {real_estate['name']}, Email: {real_estate.get('email', '')}, Phone: {real_estate.get('phone', '')}"
                c.drawString(100, y_position, real_estate_info)
                y_position -= 20

            c.save()
            messagebox.showinfo("PDF Generated", f"PDF generated successfully at {pdf_filename}")

    tk.Button(real_estate_window, text="Add real_estate", command=add_real_estate).pack(pady=5)
    tk.Button(real_estate_window, text="Edit real_estate", command=edit_real_estate).pack(pady=5)
    tk.Button(real_estate_window, text="Generate PDF", command=generate_pdf).pack(pady=5)
    
    print_real_estate()

# Function to open contacts window
def open_contacts_window(profile_name):
    profile = next((p for p in profiles if p['name'] == profile_name), None)
    if not profile:
        messagebox.showwarning("Profile Not Found", f"Profile '{profile_name}' not found.")
        return

    contacts_window = tk.Toplevel()
    contacts_window.title(f"Contacts for Profile: {profile_name}")

    contacts_list = tk.Listbox(contacts_window, width=50, height=20)
    contacts_list.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar = tk.Scrollbar(contacts_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    contacts_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=contacts_list.yview)

    def print_contacts():
        contacts_list.delete(0, tk.END)
        for contact in profile.get('contacts', []):
            contact_info = f"Name: {contact['name']}, Phone: {contact.get('phone', 'N/A')}, Email: {contact.get('email', 'N/A')}"
            contacts_list.insert(tk.END, contact_info)

    def add_contact():
        add_contact_window = tk.Toplevel()
        add_contact_window.title("Add Contact")

        tk.Label(add_contact_window, text="Name:").pack(pady=10)
        name_entry = tk.Entry(add_contact_window)
        name_entry.pack()

        tk.Label(add_contact_window, text="Phone:").pack(pady=10)
        phone_entry = tk.Entry(add_contact_window)
        phone_entry.pack()

        tk.Label(add_contact_window, text="Email:").pack(pady=10)
        email_entry = tk.Entry(add_contact_window)
        email_entry.pack()

        def save_contact():
            selected_index = profiles_listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]  # Get the first selected item

            if 'contacts' not in profile:
                profile['contacts'] = []
            new_contact = {
                'name': name_entry.get(),
                'phone': phone_entry.get(),
                'email': email_entry.get()
            }
            profile['contacts'].append(new_contact)
            save_to_json(profiles, PROFILES_FILE)
            print_contacts()
            add_contact_window.destroy()

            if selected_index is not None:
                profiles_listbox.selection_set(selected_index)  # Re-select the profile
                profiles_listbox.activate(selected_index)  # Ensure the selection is active
                update_selected_profile_labels()  # Update the labels for the re-selected profile

        tk.Button(add_contact_window, text="Save Contact", command=save_contact).pack(pady=10)

    tk.Button(contacts_window, text="Add Contact", command=add_contact).pack(pady=10)
    print_contacts()


def open_contact2s2_window(profile_name):
    profile = next((p for p in profiles if p['name'] == profile_name), None)
    if not profile:
        messagebox.showwarning("Profile Not Found", f"Profile '{profile_name}' not found.")
        return

    contact2s2_window = tk.Toplevel()
    contact2s2_window.title(f"contact2s2 for Profile: {profile_name}")

    contact2s2_list = tk.Listbox(contact2s2_window, width=50, height=20)
    contact2s2_list.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar = tk.Scrollbar(contact2s2_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    contact2s2_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=contact2s2_list.yview)

    def print_contact2s2():
        contact2s2_list.delete(0, tk.END)
        for contact2 in profile.get('contact2s2', []):
            contact2_info = f"Name: {contact2['name']}, Phone: {contact2.get('phone', 'N/A')}, Email: {contact2.get('email', 'N/A')}"
            contact2s2_list.insert(tk.END, contact2_info)

    def add_contact2():
        add_contact2_window = tk.Toplevel()
        add_contact2_window.title("Add contact2")

        tk.Label(add_contact2_window, text="Name:").pack(pady=10)
        name_entry = tk.Entry(add_contact2_window)
        name_entry.pack()

        tk.Label(add_contact2_window, text="Phone:").pack(pady=10)
        phone_entry = tk.Entry(add_contact2_window)
        phone_entry.pack()

        tk.Label(add_contact2_window, text="Email:").pack(pady=10)
        email_entry = tk.Entry(add_contact2_window)
        email_entry.pack()

        def save_contact2():
            selected_index = profiles_listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]  # Get the first selected item

            if 'contact2s2' not in profile:
                profile['contact2s2'] = []
            new_contact2 = {
                'name': name_entry.get(),
                'phone': phone_entry.get(),
                'email': email_entry.get()
            }
            profile['contact2s2'].append(new_contact2)
            save_to_json(profiles, PROFILES_FILE)
            print_contact2s2()
            add_contact2_window.destroy()

            if selected_index is not None:
                profiles_listbox.selection_set(selected_index)  # Re-select the profile
                profiles_listbox.activate(selected_index)  # Ensure the selection is active
                update_selected_profile_labels()  # Update the labels for the re-selected profile

        tk.Button(add_contact2_window, text="Save contact2", command=save_contact2).pack(pady=10)

    tk.Button(contact2s2_window, text="Add contact2", command=add_contact2).pack(pady=10)
    print_contact2s2()

def open_contact3s3_window(profile_name):
    profile = next((p for p in profiles if p['name'] == profile_name), None)
    if not profile:
        messagebox.showwarning("Profile Not Found", f"Profile '{profile_name}' not found.")
        return

    contact3s3_window = tk.Toplevel()
    contact3s3_window.title(f"contact3s3 for Profile: {profile_name}")

    contact3s3_list = tk.Listbox(contact3s3_window, width=50, height=20)
    contact3s3_list.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar = tk.Scrollbar(contact3s3_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    contact3s3_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=contact3s3_list.yview)

    def print_contact3s3():
        contact3s3_list.delete(0, tk.END)
        for contact3 in profile.get('contact3s3', []):
            contact3_info = f"Name: {contact3['name']}, Phone: {contact3.get('phone', 'N/A')}, Email: {contact3.get('email', 'N/A')}"
            contact3s3_list.insert(tk.END, contact3_info)

    def add_contact3():
        add_contact3_window = tk.Toplevel()
        add_contact3_window.title("Add contact3")

        tk.Label(add_contact3_window, text="Name:").pack(pady=10)
        name_entry = tk.Entry(add_contact3_window)
        name_entry.pack()

        tk.Label(add_contact3_window, text="Phone:").pack(pady=10)
        phone_entry = tk.Entry(add_contact3_window)
        phone_entry.pack()

        tk.Label(add_contact3_window, text="Email:").pack(pady=10)
        email_entry = tk.Entry(add_contact3_window)
        email_entry.pack()

        def save_contact3():
            selected_index = profiles_listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]  # Get the first selected item

            if 'contact3s3' not in profile:
                profile['contact3s3'] = []
            new_contact3 = {
                'name': name_entry.get(),
                'phone': phone_entry.get(),
                'email': email_entry.get()
            }
            profile['contact3s3'].append(new_contact3)
            save_to_json(profiles, PROFILES_FILE)
            print_contact3s3()
            add_contact3_window.destroy()

            if selected_index is not None:
                profiles_listbox.selection_set(selected_index)  # Re-select the profile
                profiles_listbox.activate(selected_index)  # Ensure the selection is active
                update_selected_profile_labels()  # Update the labels for the re-selected profile

        tk.Button(add_contact3_window, text="Save contact3", command=save_contact3).pack(pady=10)

    tk.Button(contact3s3_window, text="Add contact3", command=add_contact3).pack(pady=10)
    print_contact3s3()

# Function to update the labels based on the selected profile
def update_selected_profile_labels():
    selected_index = profiles_listbox.curselection()
    if selected_index:
        selected_profile = profiles[selected_index[0]]

        vehicles_complete = selected_profile.get('vehicles', False)
        housing_complete = selected_profile.get('housing', False)
        housing2_complete = selected_profile.get('housing2', False)
        contacts_complete = len(selected_profile.get('contacts', [])) > 0
        contacts_complete2 = len(selected_profile.get('contact2s2', [])) > 0
        contacts_complete3 = len(selected_profile.get('contact3s3', [])) > 0

        contacts_label.config(text="Complete" if contacts_complete else "Incomplete", fg="green" if contacts_complete else "red")
        contacts_label2.config(text="Complete" if contacts_complete2 else "Incomplete", fg="green" if contacts_complete2 else "red")
        contacts_label3.config(text="Complete" if contacts_complete3 else "Incomplete", fg="green" if contacts_complete3 else "red")

# Function to generate a PDF for the selected profile
from reportlab.lib.pagesizes import letter
from reportlab.lib import utils

from reportlab.lib.pagesizes import letter

def generate_pdf():
    selected_index = profiles_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Selection Error", "No profile selected.")
        return

    profile = profiles[selected_index[0]]
    pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=f"{profile['name']}_profile.pdf")
    
    if not pdf_file:
        return

    # Create a canvas for the PDF
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Define some margin and text wrapping configurations
    margin_x = 50  # Left and right margin
    margin_y = 50  # Top and bottom margin
    max_text_width = width - 2 * margin_x  # Width available for text

    # Start drawing the profile info
    y = height - margin_y  # Starting position at the top of the page

    # Utility function to wrap text to fit within the margins
    def draw_wrapped_text(text, y, c, max_width, line_height=15):
        lines = []
        while text:
            split_index = len(text)
            while c.stringWidth(text[:split_index]) > max_width and split_index > 0:
                split_index -= 1
            lines.append(text[:split_index])
            text = text[split_index:].lstrip()
        for line in lines:
            if y < margin_y:  # Check if we are running out of space on the page
                c.showPage()  # Create a new page
                y = height - margin_y  # Reset y position
            c.drawString(margin_x, y, line)
            y -= line_height
        return y

    # Draw profile name
    y = draw_wrapped_text(f"Profile Name: {profile['name']}", y, c, max_text_width)

    # Draw contacts
    if profile.get('contacts'):
        y = draw_wrapped_text("Contacts:", y - 20, c, max_text_width)
        for contact in profile['contacts']:
            # Separate name, phone, and email on different lines
            y = draw_wrapped_text(f"Name: {contact['name']}", y - 10, c, max_text_width)
            y = draw_wrapped_text(f"Phone: {contact.get('phone', 'N/A')}", y - 5, c, max_text_width)
            y = draw_wrapped_text(f"Email: {contact.get('email', 'N/A')}", y - 5, c, max_text_width)
            y -= 10  # Add extra spacing between different contacts
    else:
        y = draw_wrapped_text("Contacts: None", y - 20, c, max_text_width)

    if profile.get('contact2s2'):
        y = draw_wrapped_text("Contact2s2:", y - 20, c, max_text_width)
        for contact in profile['contact2s2']:
            # Separate name, phone, and email on different lines
            y = draw_wrapped_text(f"Name: {contact['name']}", y - 10, c, max_text_width)
            y = draw_wrapped_text(f"Phone: {contact.get('phone', 'N/A')}", y - 5, c, max_text_width)
            y = draw_wrapped_text(f"Email: {contact.get('email', 'N/A')}", y - 5, c, max_text_width)
            y -= 10  # Add extra spacing between different contacts
    else:
        y = draw_wrapped_text("Contacts: None", y - 20, c, max_text_width)
    
    if profile.get('contact3s3'):
        y = draw_wrapped_text("Contact3s3:", y - 20, c, max_text_width)
        for contact in profile['contact3s3']:
            # Separate name, phone, and email on different lines
            y = draw_wrapped_text(f"Name: {contact['name']}", y - 10, c, max_text_width)
            y = draw_wrapped_text(f"Phone: {contact.get('phone', 'N/A')}", y - 5, c, max_text_width)
            y = draw_wrapped_text(f"Email: {contact.get('email', 'N/A')}", y - 5, c, max_text_width)
            y -= 10  # Add extra spacing between different contacts
    else:
        y = draw_wrapped_text("Contacts: None", y - 20, c, max_text_width)

    # Draw vehicles section
    vehicles_text = "Vehicles: Yes" if profile.get('vehicles') else "Vehicles: No"
    y = draw_wrapped_text(vehicles_text, y - 20, c, max_text_width)

    # Draw housing section
    housing_text = "Housing: Yes" if profile.get('housing') else "Housing: No"
    y = draw_wrapped_text(housing_text, y - 20, c, max_text_width)

    # Draw housing2 section
    housing2_text = "Housing2: Yes" if profile.get('housing2') else "Housing2: No"
    y = draw_wrapped_text(housing2_text, y - 20, c, max_text_width)

    # Save and close the PDF
    c.save()
    messagebox.showinfo("PDF Generated", f"PDF file '{pdf_file}' has been generated.")


# Main window function
def open_main_window():
    global profiles_listbox, vehicles_label, housing_label, housing_label2, contacts_label, contacts_label2, contacts_label3

    root = tk.Tk()
    root.title("Profile Manager")

    # Create a canvas for scrolling
    canvas = tk.Canvas(root, borderwidth=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a scrollbar for the canvas
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the main content
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Function to update the canvas scroll region
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", update_scroll_region)

    # Create a frame for the profiles listbox and scrollbar
    profiles_frame = tk.Frame(content_frame)
    profiles_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a scrollbar for the profiles listbox
    profiles_scrollbar = tk.Scrollbar(profiles_frame, orient="vertical")
    profiles_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create the Listbox for profiles
    profiles_listbox = tk.Listbox(profiles_frame, height=20, width=50, yscrollcommand=profiles_scrollbar.set)
    profiles_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure the scrollbar for the listbox
    profiles_scrollbar.config(command=profiles_listbox.yview)

    # Bind profile selection to update labels
    profiles_listbox.bind("<<ListboxSelect>>", lambda event: update_selected_profile_labels())

  # Add buttons and labels to the content frame
    tk.Button(content_frame, text="Create Profile", command=create_profile_window).pack(pady=5)
    tk.Button(content_frame, text="Delete Profile", command=delete_profile).pack(pady=5)  # Delete Profile Button


    # Section: Contacts
    contacts_frame = tk.Frame(content_frame)
    contacts_frame.pack(pady=5)
    tk.Button(contacts_frame, text="Manage Contacts", command=lambda: open_contacts_window(profiles_listbox.get(tk.ACTIVE))).pack(side=tk.LEFT)
    contacts_label = tk.Label(contacts_frame, text="Incomplete", fg="red")
    contacts_label.pack(side=tk.LEFT, padx=10)


    contacts_frame2 = tk.Frame(content_frame)
    contacts_frame2.pack(pady=5)
    tk.Button(contacts_frame2, text="Manage Contacts", command=lambda: open_contact2s2_window(profiles_listbox.get(tk.ACTIVE))).pack(side=tk.LEFT)
    contacts_label2 = tk.Label(contacts_frame2, text="Incomplete", fg="red")
    contacts_label2.pack(side=tk.LEFT, padx=10)

    contacts_frame3 = tk.Frame(content_frame)
    contacts_frame3.pack(pady=5)
    tk.Button(contacts_frame3, text="Manage Contacts", command=lambda: open_contact3s3_window(profiles_listbox.get(tk.ACTIVE))).pack(side=tk.LEFT)
    contacts_label3 = tk.Label(contacts_frame3, text="Incomplete", fg="red")
    contacts_label3.pack(side=tk.LEFT, padx=10)
    # Button to generate PDF
    tk.Button(content_frame, text="Generate PDF", command=generate_pdf).pack(pady=10)

    # Populate profiles listbox
    for profile in profiles:
        profiles_listbox.insert(tk.END, profile['name'])

    root.mainloop()

open_main_window()
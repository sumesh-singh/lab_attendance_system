# # Create a virtual environment (optional)
# # python -m venv myenv
# # .\myenv\Scripts\activate.ps1

import customtkinter as ctk
import pandas as pd
from datetime import datetime
import os
from tkinter import messagebox, filedialog

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

roll_format = "1601248620"

class ModernLabAttendanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Lab Attendance System")
        self.geometry("900x700")
        
        # Store attendance data
        self.attendance_data = []
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.create_header()
        self.create_input_section()
        self.create_attendance_list()
        self.create_bottom_buttons()
        
        # Bind Enter key
        self.bind('<Return>', lambda event: self.mark_attendance())

    def create_header(self):
        # Header Frame
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        # Title Label with modern font and styling
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Lab Attendance System",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(10,5))
        
        # Date Label
        self.date_label = ctk.CTkLabel(
            self.header_frame,
            text=f"Date: {datetime.now().strftime('%B %d, %Y')}",
            font=ctk.CTkFont(size=16)
        )
        self.date_label.grid(row=1, column=0, padx=20, pady=(0,10))

    def create_input_section(self):
        # Input Frame
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Roll Number Entry
        self.roll_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter Roll Number",
            font=ctk.CTkFont(size=16),
            width=200,
            height=40
        )
        self.roll_entry.grid(row=0, column=0, padx=(20,10), pady=20)
        
        # Mark Present Button
        self.mark_button = ctk.CTkButton(
            self.input_frame,
            text="Mark Present",
            font=ctk.CTkFont(size=16),
            width=120,
            height=40,
            command=self.mark_attendance
        )
        self.mark_button.grid(row=0, column=1, padx=10, pady=20)
        
        self.roll_entry.focus()

    def create_attendance_list(self):
        # List Frame
        self.list_frame = ctk.CTkFrame(self, corner_radius=10)
        self.list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # Scrollable Frame for attendance records
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.list_frame,
            label_text="Attendance Records",
            label_font=ctk.CTkFont(size=20, weight="bold")
        )
        self.scrollable_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)
        
        # Headers
        headers = ["Roll Number", "Time", "Status", "Actions"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.scrollable_frame,
                text=header,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            label.grid(row=0, column=i, padx=10, pady=5)
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

    def create_bottom_buttons(self):
        # Button Frame
        self.button_frame = ctk.CTkFrame(self, corner_radius=10)
        self.button_frame.grid(row=3, column=0, padx=20, pady=(10,20), sticky="ew")
        
        # Save Button
        self.save_button = ctk.CTkButton(
            self.button_frame,
            text="Save Attendance",
            font=ctk.CTkFont(size=16),
            width=150,
            height=40,
            command=self.save_attendance
        )
        self.save_button.grid(row=0, column=0, padx=20, pady=20)
        
        # Clear Button
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear All",
            font=ctk.CTkFont(size=16),
            width=150,
            height=40,
            fg_color="transparent",
            border_width=2,
            command=self.clear_attendance
        )
        self.clear_button.grid(row=0, column=1, padx=20, pady=20)
        
        self.button_frame.grid_columnconfigure((0,1), weight=1)

    def add_attendance_record(self, roll_number, time_str, status):
        row = len(self.scrollable_frame.grid_slaves()) // 4  # 4 columns per row
        if row == 0:  # If it's the first row after headers
            row = 1
        
        # Record Labels
        roll_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=roll_number,
            font=ctk.CTkFont(size=14)
        )
        roll_label.grid(row=row, column=0, padx=10, pady=5)
        
        time_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=time_str,
            font=ctk.CTkFont(size=14)
        )
        time_label.grid(row=row, column=1, padx=10, pady=5)
        
        status_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=status,
            font=ctk.CTkFont(size=14)
        )
        status_label.grid(row=row, column=2, padx=10, pady=5)
        
        # Delete Button
        delete_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Remove",
            font=ctk.CTkFont(size=14),
            width=80,
            height=30,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=lambda: self.remove_entry(row, roll_number)
        )
        delete_button.grid(row=row, column=3, padx=10, pady=5)

    def mark_attendance(self):
        roll_number = self.roll_entry.get().strip()
        
        if not self.validate_roll_number(roll_number):
            self.roll_entry.delete(0, ctk.END)
            return
            
        formatted_roll = f"{roll_format}{roll_number.zfill(2)}"
        
        if any(entry['Roll Number'] == formatted_roll for entry in self.attendance_data):
            messagebox.showwarning("Warning", f"Roll number {roll_number} is already marked present")
            self.roll_entry.delete(0, ctk.END)
            return
            
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Add to attendance data
        attendance_entry = {
            'Roll Number': formatted_roll,
            'Time': current_time,
            'Status': 'Present'
        }
        self.attendance_data.append(attendance_entry)
        
        # Add to UI
        self.add_attendance_record(formatted_roll, current_time, 'Present')
        
        self.roll_entry.delete(0, ctk.END)
        self.roll_entry.focus()

    def remove_entry(self, row, roll_number):
        if messagebox.askyesno("Confirm Removal", "Are you sure you want to remove this entry?"):
            # Remove from data structure
            self.attendance_data = [entry for entry in self.attendance_data 
                                  if entry['Roll Number'] != roll_number]
            
            # Clear all existing entries from UI
            for widget in self.scrollable_frame.grid_slaves():
                if int(widget.grid_info()['row']) > 0:  # Don't remove headers
                    widget.destroy()
            
            # Redraw all entries
            self.redraw_attendance_list()

    def redraw_attendance_list(self):
        """Redraws the entire attendance list from the current data"""
        # Add all records back
        for idx, entry in enumerate(self.attendance_data, start=1):
            self.add_attendance_record(
                entry['Roll Number'],
                entry['Time'],
                entry['Status']
            )
        
        # Reposition remaining widgets
        current_row = deleted_row
        for widget in reversed(widgets):
            widget.grid(row=current_row, column=widget.grid_info()['column'])
            if widget.grid_info()['column'] == 3:  # After last widget in row
                current_row += 1

    def validate_roll_number(self, roll_number):
        if not roll_number:
            messagebox.showerror("Error", "Please enter a roll number")
            return False
            
        try:
            roll_int = int(roll_number)
            if not (1 <= roll_int <= 64):
                messagebox.showerror("Error", "Roll number must be between 1 and 64")
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric roll number")
            return False
            
        return True

    def save_attendance(self):
        if not self.attendance_data:
            messagebox.showerror("Error", "No attendance data to save")
            return
            
        try:
            df = pd.DataFrame(self.attendance_data)
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            default_filename = f"lab_attendance_{current_datetime}.xlsx"
            
            filename = filedialog.asksaveasfilename(
                initialdir=os.path.expanduser("~/Desktop"),
                initialfile=default_filename,
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if filename:
                if os.path.exists(filename):
                    if messagebox.askyesno("File Exists", "File already exists. Do you want to overwrite it?"):
                        df.to_excel(filename, index=False)
                        messagebox.showinfo("Success", f"Attendance saved successfully to {filename}")
                        self.clear_attendance()
                else:
                    df.to_excel(filename, index=False)
                    messagebox.showinfo("Success", f"Attendance saved successfully to {filename}")
                    self.clear_attendance()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")

    def clear_attendance(self):
        if not self.attendance_data:
            messagebox.showinfo("Info", "No attendance data to clear")
            return
            
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all attendance data?"):
            self.attendance_data.clear()
            
            # Clear all records from scrollable frame (except headers)
            for widget in self.scrollable_frame.grid_slaves():
                if int(widget.grid_info()['row']) > 0:  # Don't remove headers
                    widget.destroy()

if __name__ == "__main__":
    app = ModernLabAttendanceApp()
    app.mainloop()
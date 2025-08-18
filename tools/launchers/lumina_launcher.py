#!/usr/bin/env python3
"""
Lumina Memory System - Professional Launcher
============================================
Cross-platform launcher with GUI menu system that can be compiled to executable
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from pathlib import Path

class LuminaLauncher:
    def __init__(self):
        self.project_dir = Path(__file__).parent.absolute()
        self.venv_path = self.project_dir / "venv"
        self.gui_script = self.project_dir / "llm_consciousness_gui" / "main.py"
        self.version = "1.0.0"
        
        # Setup main window
        self.root = tk.Tk()
        self.root.title(f"Lumina Memory System Launcher v{self.version}")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Configure style
        self.setup_styles()
        self.create_widgets()
        
        # Center window
        self.center_window()
        
    def setup_styles(self):
        """Configure the visual style"""
        self.root.configure(bg='#2b2b2b')
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom styles
        style.configure('Title.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ffffff',
                       font=('Arial', 16, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background='#2b2b2b',
                       foreground='#cccccc', 
                       font=('Arial', 10))
        
        style.configure('Action.TButton',
                       font=('Arial', 11),
                       padding=(20, 10))
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
    def create_widgets(self):
        """Create the main interface"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2b2b2b', pady=20)
        header_frame.pack(fill='x')
        
        title_label = ttk.Label(header_frame, 
                               text="🧠 LUMINA MEMORY SYSTEM",
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame,
                                  text="Enhanced LLM Consciousness GUI with XPUnit Analysis",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        version_label = ttk.Label(header_frame,
                                 text=f"Version {self.version}",
                                 style='Subtitle.TLabel')
        version_label.pack(pady=(5, 0))
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#2b2b2b')
        content_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Launch options
        self.create_launch_buttons(content_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_frame = tk.Frame(self.root, bg='#404040', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        status_label = tk.Label(status_frame, 
                               textvariable=self.status_var,
                               bg='#404040', 
                               fg='#ffffff',
                               font=('Arial', 9))
        status_label.pack(side='left', padx=10, pady=5)
        
    def create_launch_buttons(self, parent):
        """Create the main launch buttons"""
        buttons = [
            ("🚀 Launch GUI (Standard)", "Start the Enhanced LLM Consciousness GUI", self.launch_standard),
            ("🔧 Launch GUI (Debug)", "Start with verbose logging and debug information", self.launch_debug),
            ("🧪 Launch Jupyter Notebooks", "Open Jupyter Lab for notebook development", self.launch_jupyter),
            ("📊 System Diagnostics", "Check environment, dependencies, and system health", self.run_diagnostics),
            ("⚙️ Environment Setup", "Install/update virtual environment and dependencies", self.setup_environment),
            ("🔗 Create Desktop Shortcut", "Add launcher shortcut to desktop", self.create_shortcut),
        ]
        
        for i, (text, description, command) in enumerate(buttons):
            # Button frame
            btn_frame = tk.Frame(parent, bg='#2b2b2b', pady=5)
            btn_frame.pack(fill='x')
            
            # Main button
            btn = ttk.Button(btn_frame, 
                           text=text,
                           style='Action.TButton',
                           command=command)
            btn.pack(fill='x')
            
            # Description
            desc_label = ttk.Label(btn_frame,
                                  text=f"   └─ {description}",
                                  style='Subtitle.TLabel')
            desc_label.pack(anchor='w', padx=20)
            
        # Exit button
        exit_frame = tk.Frame(parent, bg='#2b2b2b', pady=20)
        exit_frame.pack(fill='x')
        
        exit_btn = ttk.Button(exit_frame,
                             text="❌ Exit",
                             style='Action.TButton', 
                             command=self.root.quit)
        exit_btn.pack()
        
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update()
        
    def check_environment(self):
        """Check if environment is properly set up"""
        if not self.venv_path.exists():
            messagebox.showerror("Environment Error", 
                               "Virtual environment not found.\nPlease run Environment Setup first.")
            return False
            
        if not self.gui_script.exists():
            messagebox.showerror("File Error",
                               f"GUI script not found at:\n{self.gui_script}")
            return False
            
        return True
        
    def run_in_venv(self, command, debug=False):
        """Run a command in the virtual environment"""
        if os.name == 'nt':  # Windows
            activate_script = self.venv_path / "Scripts" / "activate.bat"
            if debug:
                full_command = f'call "{activate_script}" && set PYTHONPATH={self.project_dir}\\src;%PYTHONPATH% && {command}'
            else:
                full_command = f'call "{activate_script}" && {command}'
        else:  # Unix-like
            activate_script = self.venv_path / "bin" / "activate"
            if debug:
                full_command = f'source "{activate_script}" && export PYTHONPATH={self.project_dir}/src:$PYTHONPATH && {command}'
            else:
                full_command = f'source "{activate_script}" && {command}'
            
        return subprocess.run(full_command, shell=True, cwd=self.project_dir)
        
    def launch_standard(self):
        """Launch GUI in standard mode"""
        if not self.check_environment():
            return
            
        self.update_status("Launching GUI (Standard Mode)...")
        
        def run():
            try:
                result = self.run_in_venv(f'python "{self.gui_script}"')
                if result.returncode != 0:
                    messagebox.showerror("Launch Error", f"GUI exited with error code: {result.returncode}")
            except Exception as e:
                messagebox.showerror("Launch Error", f"Failed to launch GUI: {str(e)}")
            finally:
                self.update_status("Ready")
                
        threading.Thread(target=run, daemon=True).start()
        
    def launch_debug(self):
        """Launch GUI in debug mode"""
        if not self.check_environment():
            return
            
        self.update_status("Launching GUI (Debug Mode)...")
        
        def run():
            try:
                result = self.run_in_venv(f'python -u "{self.gui_script}" --debug', debug=True)
                if result.returncode != 0:
                    messagebox.showerror("Launch Error", f"GUI exited with error code: {result.returncode}")
            except Exception as e:
                messagebox.showerror("Launch Error", f"Failed to launch GUI: {str(e)}")
            finally:
                self.update_status("Ready")
                
        threading.Thread(target=run, daemon=True).start()
        
    def launch_jupyter(self):
        """Launch Jupyter Lab"""
        if not self.check_environment():
            return
            
        self.update_status("Launching Jupyter Lab...")
        
        def run():
            try:
                notebooks_dir = self.project_dir / "notebooks"
                result = self.run_in_venv(f'jupyter lab "{notebooks_dir}"')
                if result.returncode != 0:
                    messagebox.showerror("Launch Error", f"Jupyter Lab exited with error code: {result.returncode}")
            except Exception as e:
                messagebox.showerror("Launch Error", f"Failed to launch Jupyter Lab: {str(e)}")
            finally:
                self.update_status("Ready")
                
        threading.Thread(target=run, daemon=True).start()
        
    def run_diagnostics(self):
        """Run system diagnostics"""
        self.update_status("Running diagnostics...")
        
        # Create diagnostics window
        diag_window = tk.Toplevel(self.root)
        diag_window.title("System Diagnostics")
        diag_window.geometry("700x500")
        diag_window.configure(bg='#2b2b2b')
        
        # Text widget for output
        text_widget = tk.Text(diag_window, 
                             bg='#1e1e1e', 
                             fg='#ffffff',
                             font=('Consolas', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        def run_checks():
            def write_line(text):
                text_widget.insert(tk.END, text + "\n")
                text_widget.see(tk.END)
                diag_window.update()
                
            write_line("🔍 LUMINA MEMORY SYSTEM - DIAGNOSTICS REPORT")
            write_line("=" * 60)
            write_line("")
            
            # Project directory check
            write_line("📁 PROJECT DIRECTORY:")
            write_line(f"   Path: {self.project_dir}")
            write_line(f"   {'✅ Found' if self.project_dir.exists() else '❌ Not found'}")
            write_line("")
            
            # Python check
            write_line("🐍 PYTHON INSTALLATION:")
            try:
                result = subprocess.run([sys.executable, "--version"], 
                                      capture_output=True, text=True)
                write_line(f"   ✅ {result.stdout.strip()}")
                write_line(f"   Path: {sys.executable}")
            except Exception as e:
                write_line(f"   ❌ Python check failed: {e}")
            write_line("")
            
            # Virtual environment check
            write_line("🌐 VIRTUAL ENVIRONMENT:")
            if self.venv_path.exists():
                write_line("   ✅ Virtual environment found")
                write_line(f"   Path: {self.venv_path}")
            else:
                write_line("   ❌ Virtual environment not found")
            write_line("")
            
            # Package checks
            write_line("📦 KEY PACKAGES:")
            packages = ["PySide6", "numpy", "scipy"]
            for package in packages:
                try:
                    result = self.run_in_venv(f'python -c "import {package}; print({package}.__version__)"')
                    if result.returncode == 0:
                        write_line(f"   ✅ {package} installed")
                    else:
                        write_line(f"   ❌ {package} not found")
                except:
                    write_line(f"   ❌ {package} check failed")
            write_line("")
            
            # Project structure
            write_line("📋 PROJECT STRUCTURE:")
            dirs_to_check = ["src/lumina_memory", "llm_consciousness_gui", "notebooks", "tests"]
            for dir_name in dirs_to_check:
                dir_path = self.project_dir / dir_name
                write_line(f"   {'✅' if dir_path.exists() else '❌'} {dir_name}")
            
            write_line("")
            write_line("=" * 60)
            write_line("✅ Diagnostics complete")
            
        threading.Thread(target=run_checks, daemon=True).start()
        self.update_status("Ready")
        
    def setup_environment(self):
        """Setup the development environment"""
        self.update_status("Setting up environment...")
        
        def setup():
            try:
                # Create virtual environment if it doesn't exist
                if not self.venv_path.exists():
                    result = subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)],
                                          cwd=self.project_dir)
                    if result.returncode != 0:
                        messagebox.showerror("Setup Error", "Failed to create virtual environment")
                        return
                
                # Install requirements
                requirements_files = ["requirements.txt", "requirements-dev.txt"]
                for req_file in requirements_files:
                    req_path = self.project_dir / req_file
                    if req_path.exists():
                        self.run_in_venv(f'python -m pip install -r "{req_path}"')
                
                # Install package in development mode
                setup_py = self.project_dir / "setup.py"
                if setup_py.exists():
                    self.run_in_venv('python -m pip install -e .')
                
                messagebox.showinfo("Setup Complete", "Environment setup completed successfully!")
                
            except Exception as e:
                messagebox.showerror("Setup Error", f"Environment setup failed: {str(e)}")
            finally:
                self.update_status("Ready")
                
        threading.Thread(target=setup, daemon=True).start()
        
    def create_shortcut(self):
        """Create desktop shortcut"""
        try:
            desktop = Path.home() / "Desktop"
            shortcut_name = "Lumina Memory System.lnk"
            
            if os.name == 'nt':  # Windows
                import winshell
                from win32com.client import Dispatch
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(str(desktop / shortcut_name))
                shortcut.Targetpath = str(Path(__file__).absolute())
                shortcut.WorkingDirectory = str(self.project_dir)
                shortcut.Description = "Lumina Memory System - Enhanced LLM Consciousness GUI"
                shortcut.save()
                
                messagebox.showinfo("Shortcut Created", 
                                  f"Desktop shortcut created successfully!\nLocation: {desktop / shortcut_name}")
            else:
                messagebox.showinfo("Not Supported", "Desktop shortcut creation not supported on this platform")
                
        except ImportError:
            messagebox.showerror("Missing Dependencies", 
                               "Desktop shortcut creation requires 'winshell' and 'pywin32' packages")
        except Exception as e:
            messagebox.showerror("Shortcut Error", f"Failed to create shortcut: {str(e)}")
            
    def run(self):
        """Start the launcher"""
        self.root.mainloop()

def main():
    """Main entry point"""
    launcher = LuminaLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
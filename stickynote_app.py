import ctypes
import tkinter as tk
from tkinter import font as tkFont

class PostItApp:
    def __init__(self, root, window_title="StickyNote", window_color="#ffff99", window_width=200, window_height=200):
        # Initialize the tkinter root window
        self.root = root
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg=window_color)
        self.root.overrideredirect(1)  # Remove window decorations to make it look like a sticky note
        self.root.wm_attributes("-topmost", 1)  # Keep window on top
        self.root.title(window_title)

        # Create a custom font for the sticky note
        custom_font = tkFont.Font(family='Indie Flower', size=12)

        # Create buttons for creating new notes, closing the current note and toggling draw mode
        self.close_button = tk.Label(root, text="X", bg=window_color, font=custom_font)
        self.close_button.bind("<Button-1>", self.close_app)
        self.close_button.pack(side="left", anchor='nw')

        self.draw_mode_button = tk.Label(root, text="*", bg=window_color, font=custom_font)
        self.draw_mode_button.bind("<Button-1>", self.toggle_draw_mode)
        self.draw_mode_button.pack(side="right", anchor='ne')

        self.new_note_button = tk.Label(root, text="+", bg=window_color, font=custom_font)
        self.new_note_button.bind("<Button-1>", self.new_note)
        self.new_note_button.pack(side="right", anchor='ne')

        # Create the text widget where the user can write their note
        self.text_widget = tk.Text(root, bg=window_color, font=custom_font, borderwidth=0)
        self.text_widget.pack(fill="both", expand=True)

        # Create a canvas for drawing
        self.canvas_widget = tk.Canvas(root, bg=window_color, bd=0, highlightthickness=0)
        self.canvas_widget.pack(fill="both", expand=True)

        # Variables used to implement the drag functionality
        self._offsetx = 0
        self._offsety = 0

        # Bind the dragging functions to the appropriate mouse events
        self.root.bind('<Button-1>', self.clickwin)
        self.root.bind('<B1-Motion>', self.dragwin)
        
        # Hide the console window
        self.hide_console_window()

        # Drawing mode
        self.drawing = False
        self.lastx, self.lasty = 0, 0
        self.root.bind("<Button-3>", self.start_draw)
        self.root.bind("<B3-Motion>", self.draw)

    def clickwin(self, event):
        """Function to get the current mouse position when it is clicked"""
        self._offsetx = event.x
        self._offsety = event.y

    def dragwin(self, event):
        """Function to update the position of the window when the mouse is dragged"""
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        self.root.geometry(f'+{x}+{y}')

    def close_app(self, event):
        """Function to close the current note window"""
        self.root.destroy()

    def new_note(self, event):
        """Function to create a new note"""
        new_root = tk.Toplevel()
        new_app = PostItApp(new_root)
        
    def hide_console_window(self):
        """Function to hide the console window in windows environment"""
        console_window = ctypes.windll.kernel32.GetConsoleWindow()
        if console_window != 0:
            ctypes.windll.user32.ShowWindow(console_window, 0)
            ctypes.windll.kernel32.CloseHandle(console_window)

    def toggle_draw_mode(self, event):
        """Toggle draw mode on and off."""
        self.drawing = not self.drawing
        self.text_widget.pack_forget() if self.drawing else self.text_widget.pack(fill="both", expand=True)
        self.canvas_widget.pack_forget() if not self.drawing else self.canvas_widget.pack(fill="both", expand=True)

    def start_draw(self, event):
        """Function to start drawing on the sticky note"""
        if self.drawing:
            self.lastx, self.lasty = event.x, event.y

    def draw(self, event):
        """Function to draw on the sticky note"""
        if self.drawing:
            self.canvas_widget.create_line((self.lastx, self.lasty, event.x, event.y), fill="black")
            self.lastx, self.lasty = event.x, event.y

if __name__ == "__main__":
    root = tk.Tk()
    PostItApp(root)
    root.mainloop()

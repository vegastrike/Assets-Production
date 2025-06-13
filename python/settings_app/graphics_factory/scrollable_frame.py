from tkinter import ttk
import tkinter as tk


class ScrollableFrame(ttk.Frame):
    def __init__(self, parent_frame):
        
        # Add a scrollbar to the left frame
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Create a canvas to hold the content
        self.canvas = tk.Canvas(parent_frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=False)

        # Configure the scrollbar to scroll the canvas
        scrollbar.config(command=self.canvas.yview)

        # Create an inner frame inside the canvas - this is our self object
        super().__init__(self.canvas)
                         
        self.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Add the inner frame to the canvas
        self.canvas.create_window((0, 0), window=self, anchor="nw")
    
        self.bind('<Enter>', self._bound_to_mousewheel)
        self.bind('<Leave>', self._unbound_to_mousewheel)
 

    def _bound_to_mousewheel(self, event):
        print("Binding to mousewheel")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        print("Unbinding from mousewheel")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        print(event)
        self.canvas.yview_scroll(event.delta, "units")


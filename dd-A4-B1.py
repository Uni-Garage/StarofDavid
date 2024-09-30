import tkinter as tk
                                        # TEXT OUTPUT 
class StarOfDavidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Star of David Interaction")
        self.selected_edges = []
        self.temp_selection = []

        # Main panel (Star of David interaction)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Canvas to display the Star of David
        self.canvas = tk.Canvas(self.main_frame, width=400, height=500)
        self.canvas.pack()

        # Draw the Star of David with individual selectable edges
        self.edges = self.create_star_of_david(self.canvas)

        # Button panel
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack()

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_selection)
        self.clear_button.grid(row=0, column=0)

        self.select_next_button = tk.Button(self.button_frame, text="Select-Next", command=self.select_next)
        self.select_next_button.grid(row=0, column=1)

        self.form_button = tk.Button(self.button_frame, text="Form", command=self.form_selected_edges)
        self.form_button.grid(row=0, column=2)

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.go_back, state=tk.DISABLED)
        self.back_button.grid(row=0, column=3)

        # Label to display selected edges
        self.label = tk.Label(self.main_frame, text="Selected Edges: None")
        self.label.pack()

        # Output panel (to display the final result of formed Star of David symbols)
        self.output_frame = tk.Frame(self.root)
        self.output_text = tk.Text(self.output_frame, width=50, height=20)
        self.output_text.pack()

    def create_star_of_david(self, canvas):
        # Define points for the two equilateral triangles
        points_up = [200, 50, 300, 200, 100, 200]
        points_down = [200, 250, 300, 100, 100, 100]

        edges = []

        # Function to divide an edge into smaller segments
        def divide_edge(x1, y1, x2, y2, segments):
            points = [(x1, y1)]
            for i in range(1, segments):
                points.append(((x1 * (segments - i) + x2 * i) / segments, (y1 * (segments - i) + y2 * i) / segments))
            points.append((x2, y2))
            return points

        segments_per_edge = 3  # Dividing each edge into 3 segments to make 18 edges

        # Draw the upward triangle divided into segments
        for i in range(3):
            x1, y1 = points_up[i * 2], points_up[i * 2 + 1]
            x2, y2 = points_up[(i * 2 + 2) % 6], points_up[(i * 2 + 3) % 6]
            points = divide_edge(x1, y1, x2, y2, segments_per_edge)
            for j in range(len(points) - 1):
                edge = canvas.create_line(points[j][0], points[j][1], points[j + 1][0], points[j + 1][1], width=2, fill="blue")
                canvas.tag_bind(edge, "<Button-1>", lambda event, e=edge: self.select_edge(e))
                edges.append(edge)

        # Draw the downward triangle divided into segments
        for i in range(3):
            x1, y1 = points_down[i * 2], points_down[i * 2 + 1]
            x2, y2 = points_down[(i * 2 + 2) % 6], points_down[(i * 2 + 3) % 6]
            points = divide_edge(x1, y1, x2, y2, segments_per_edge)
            for j in range(len(points) - 1):
                edge = canvas.create_line(points[j][0], points[j][1], points[j + 1][0], points[j + 1][1], width=2, fill="blue")
                canvas.tag_bind(edge, "<Button-1>", lambda event, e=edge: self.select_edge(e))
                edges.append(edge)

        return edges

    def select_edge(self, edge):
        if edge not in self.temp_selection:
            self.temp_selection.append(edge)
            self.canvas.itemconfig(edge, fill="green")
        else:
            self.temp_selection.remove(edge)
            self.canvas.itemconfig(edge, fill="blue")

        self.label.config(text=f"Selected Edges: {len(self.temp_selection)}")

    def clear_selection(self):
        for edge in self.edges:
            self.canvas.itemconfig(edge, fill="blue")
        self.temp_selection = []
        self.selected_edges = []
        self.label.config(text="Selected Edges: None")
        self.output_text.delete(1.0, tk.END)  # Clear output text

    def select_next(self):
        # Store the selected edges
        self.selected_edges.extend(self.temp_selection)
        self.temp_selection = []

        # Reset the Star of David for a new selection
        for edge in self.edges:
            self.canvas.itemconfig(edge, fill="blue")
        self.label.config(text=f"Stored {len(self.selected_edges)} edges, ready for new selection")

    def form_selected_edges(self):
        # Display the selected edges as text in the output panel
        self.output_text.delete(1.0, tk.END)  # Clear previous output
        output_data = "\n".join([f"Edge {i + 1}: {edge}" for i, edge in enumerate(self.selected_edges)])
        self.output_text.insert(tk.END, output_data)

        self.back_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.DISABLED)
        self.select_next_button.config(state=tk.DISABLED)
        self.form_button.config(state=tk.DISABLED)
        self.label.config(text="Formed output")
        self.toggle_panels()

    def toggle_panels(self):
        # Toggle visibility of the main and output frames
        if self.main_frame.winfo_viewable():
            self.main_frame.pack_forget()  # Hide main frame
            self.output_frame.pack(side=tk.LEFT, padx=10, pady=10)  # Show output frame
        else:
            self.output_frame.pack_forget()  # Hide output frame
            self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)  # Show main frame

    def go_back(self):
        # Reset to the original state, enabling selection again
        self.clear_selection()
        self.back_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.NORMAL)
        self.select_next_button.config(state=tk.NORMAL)
        self.form_button.config(state=tk.NORMAL)
        self.toggle_panels()  # Show main panel again

if __name__ == "__main__":
    root = tk.Tk()
    app = StarOfDavidGUI(root)
    root.mainloop()

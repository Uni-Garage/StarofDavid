import tkinter as tk

class StarOfDavidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Star of David Interaction")
        self.selected_edges = []
        self.temp_selection = []
        self.selected_sets = []  # To store sets of selected edges

        # Main panel (Star of David interaction)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Canvas to display the Star of David
        self.canvas = tk.Canvas(self.main_frame, width=400, height=500)
        self.canvas.pack()

        # Draw the Star of David with individual selectable edges
        self.edges = self.create_star_of_david(self.canvas)

        # Display panel for small stars
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        self.display_canvas = tk.Canvas(self.display_frame, width=400, height=400, bg="black")
        self.display_canvas.pack()

        # Buttons for selection
        self.select_next_button = tk.Button(self.root, text="Select Next", command=self.select_next)
        self.select_next_button.pack(pady=5)

        self.display_button = tk.Button(self.root, text="Display", command=self.display_result)
        self.display_button.pack(pady=5)

        # Label to show selected edges count
        self.label = tk.Label(self.root, text="Selected Edges: 0")
        self.label.pack(pady=5)

    def create_star_of_david(self, canvas):
        # Define points for the two equilateral triangles
        points_up = [200, 50, 300, 200, 100, 200]
        points_down = [200, 250, 300, 100, 100, 100]

        edges = []

        # Function to divide an edge into smaller segments
        def divide_edge(x1, y1, x2, y2, segments):
            points = [(x1, y1)]
            for i in range(1, segments):
                points.append(((x1 * (segments - i) + x2 * i) / segments,
                                (y1 * (segments - i) + y2 * i) / segments))
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
        """Toggle edge selection and update its color."""
        if edge not in self.temp_selection:
            self.temp_selection.append(edge)
            self.canvas.itemconfig(edge, fill="green")
        else:
            self.temp_selection.remove(edge)
            self.canvas.itemconfig(edge, fill="blue")

        self.label.config(text=f"Selected Edges: {len(self.temp_selection)}")

    def select_next(self):
        """Store current selections and prepare for a new selection."""
        if self.temp_selection:
            self.selected_sets.append(self.temp_selection.copy())  # Store a copy of current selection
            self.temp_selection = []  # Clear current selection

        self.label.config(text=f"Selected Sets: {len(self.selected_sets)}")

    def draw_small_star_of_david(self, canvas, x_offset, y_offset, selected_edges):
        """Draw a small Star of David (80x80) and highlight the selected edges in white."""
        scale = 0.4  # Scale factor for 80x80 star
        points_up = [
            x_offset + 40 * scale, y_offset + 10 * scale,
            x_offset + 70 * scale, y_offset + 40 * scale,
            x_offset + 10 * scale, y_offset + 40 * scale
        ]
        points_down = [
            x_offset + 40 * scale, y_offset + 70 * scale,
            x_offset + 70 * scale, y_offset + 40 * scale,
            x_offset + 10 * scale, y_offset + 40 * scale
        ]

        segments_per_edge = 3  # Dividing each edge into 3 segments to make edges

        small_star_edges = []  # To store small star edges for highlighting

        # Draw the upward triangle
        for i in range(3):
            x1, y1 = points_up[i * 2], points_up[i * 2 + 1]
            x2, y2 = points_up[(i * 2 + 2) % 6], points_up[(i * 2 + 3) % 6]
            for j in range(segments_per_edge):
                edge = canvas.create_line(x1 + (x2 - x1) * j / segments_per_edge,
                                           y1 + (y2 - y1) * j / segments_per_edge,
                                           x1 + (x2 - x1) * (j + 1) / segments_per_edge,
                                           y1 + (y2 - y1) * (j + 1) / segments_per_edge,
                                           width=1, fill="blue")
                small_star_edges.append(edge)

        # Draw the downward triangle
        for i in range(3):
            x1, y1 = points_down[i * 2], points_down[i * 2 + 1]
            x2, y2 = points_down[(i * 2 + 2) % 6], points_down[(i * 2 + 3) % 6]
            for j in range(segments_per_edge):
                edge = canvas.create_line(x1 + (x2 - x1) * j / segments_per_edge,
                                           y1 + (y2 - y1) * j / segments_per_edge,
                                           x1 + (x2 - x1) * (j + 1) / segments_per_edge,
                                           y1 + (y2 - y1) * (j + 1) / segments_per_edge,
                                           width=1, fill="blue")
                small_star_edges.append(edge)

        # Highlight selected edges
        for edge in selected_edges:
            index = self.edges.index(edge)  # Find the index in the original star
            if index < len(small_star_edges):  # Make sure the index is valid
                canvas.itemconfig(small_star_edges[index], fill="white")  # Highlight in white

    def display_result(self):
        """Display all selected edge sets as small Stars of David in a row."""
        self.display_canvas.delete("all")  # Clear the display canvas

        # For each selection set, display a small Star of David
        for idx, edge_set in enumerate(self.selected_sets):
            x_offset = 50 + idx * 90  # Adjust horizontal spacing for each small Star of David
            y_offset = 50  # Vertical offset remains the same
            self.draw_small_star_of_david(self.display_canvas, x_offset, y_offset, edge_set)

if __name__ == "__main__":
    root = tk.Tk()
    app = StarOfDavidGUI(root)
    root.mainloop()

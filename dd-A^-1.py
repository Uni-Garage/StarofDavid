import tkinter as tk

class StarOfDavidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Star of David Interaction")
        self.selected_edges = []
        self.temp_selection = []
        self.selected_sets = []  # Store each set of selected edges

        # Main panel (Star of David interaction)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Canvas to display the Star of David
        self.canvas = tk.Canvas(self.main_frame, width=400, height=500)
        self.canvas.pack()

        # Display canvas for selected stars
        self.display_canvas = tk.Canvas(self.main_frame, width=400, height=200, bg="black")
        self.display_canvas.pack()

        # Draw the Star of David with individual selectable edges
        self.edges = self.create_star_of_david(self.canvas)

        # Buttons for functionality
        self.select_next_button = tk.Button(self.root, text="Select Next", command=self.select_next)
        self.select_next_button.pack(pady=5)

        self.display_button = tk.Button(self.root, text="Display", command=self.display_result)
        self.display_button.pack(pady=5)

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
            self.canvas.itemconfig(edge, fill="green")  # Highlight selected edges in green
        else:
            self.temp_selection.remove(edge)
            self.canvas.itemconfig(edge, fill="blue")  # Reset to original color

    def select_next(self):
        """Store current selections and prepare for a new selection."""
        if self.temp_selection:  # Only add if there are selections
            self.selected_sets.append(self.temp_selection.copy())
            self.selected_edges.extend(self.temp_selection)
            self.temp_selection = []

    def display_result(self):
        """Display all selected edge sets as highlighted edges in a row on the original canvas."""
        self.display_canvas.delete("all")  # Clear the display canvas

        # Define colors for different selections
        colors = ["red", "green", "blue", "orange", "purple"]  # Add more colors as needed

        # For each selection set, highlight edges in different colors
        for idx, edge_set in enumerate(self.selected_sets):
            color = colors[idx % len(colors)]  # Cycle through colors
            for edge in edge_set:
                index = self.edges.index(edge)  # Get the index of the selected edge from the main star
                # Highlight the edge in the corresponding color
                self.canvas.itemconfig(self.edges[index], fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = StarOfDavidGUI(root)
    root.mainloop()

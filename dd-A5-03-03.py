import tkinter as tk
                                                # fail to utput correctly   but ok
class StarOfDavidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Star of David Interaction")
        self.selected_sets = []  # Stores sets of selected edges
        self.temp_selection = []  # Stores currently selected edges

        # Main panel (Star of David interaction)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Canvas to display the Star of David
        self.canvas = tk.Canvas(self.main_frame, width=400, height=500)
        self.canvas.pack()

        # Label to show how many edges are selected
        self.label = tk.Label(self.main_frame, text="Selected Edges: 0")
        self.label.pack(pady=10)

        # Button to select the next set of edges
        self.select_next_button = tk.Button(self.main_frame, text="Select-Next", command=self.select_next)
        self.select_next_button.pack(pady=10)

        # Button to display the final result
        self.display_button = tk.Button(self.main_frame, text="Display", command=self.display_result)
        self.display_button.pack(pady=10)

        # Frame and Canvas for displaying the final output
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.display_canvas = tk.Canvas(self.display_frame, width=800, height=500, bg="black")
        self.display_canvas.pack()

        # Draw the Star of David with individual selectable edges
        self.edges = self.create_star_of_david(self.canvas)

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
        # Add temporary selections to the main selection list
        if self.temp_selection:
            self.selected_sets.append(self.temp_selection[:])  # Copy the selection

        # Clear the temporary selection list and update color to indicate stored edges
        for edge in self.temp_selection:
            self.canvas.itemconfig(edge, fill="red")  # Change color to indicate confirmed selection

        self.temp_selection = []  # Reset the temporary selection list

        # Update label to show the total number of selected edges
        self.label.config(text=f"Total Confirmed Edges: {len(self.selected_sets)} sets")

    def draw_small_star_of_david(self, canvas, x_offset, y_offset, selected_edges):
        """Draw a small Star of David (50x50) and highlight the selected edges in white."""
        # Define points for the two smaller triangles, scaled down for a 50x50 size
        scale = 0.25  # Scale down to 1/4th size to fit 50x50 area
        points_up = [
            x_offset + 100 * scale, y_offset + 50 * scale,
            x_offset + 150 * scale, y_offset + 100 * scale,
            x_offset + 50 * scale, y_offset + 100 * scale
        ]
        points_down = [
            x_offset + 100 * scale, y_offset + 150 * scale,
            x_offset + 150 * scale, y_offset + 100 * scale,
            x_offset + 50 * scale, y_offset + 100 * scale
        ]

        # Function to divide an edge into smaller segments for the small stars
        def divide_edge(x1, y1, x2, y2, segments):
            points = [(x1, y1)]
            for i in range(1, segments):
                points.append(((x1 * (segments - i) + x2 * i) / segments,
                               (y1 * (segments - i) + y2 * i) / segments))
            points.append((x2, y2))
            return points

        segments_per_edge = 3  # Dividing each edge into 3 segments to make 18 edges

        # Store edges of the small star to check against selected edges
        small_star_edges = []

        # Draw the upward triangle with divided segments
        for i in range(3):
            x1, y1 = points_up[i * 2], points_up[i * 2 + 1]
            x2, y2 = points_up[(i * 2 + 2) % 6], points_up[(i * 2 + 3) % 6]
            points = divide_edge(x1, y1, x2, y2, segments_per_edge)
            for j in range(len(points) - 1):
                edge = canvas.create_line(points[j][0], points[j][1], points[j + 1][0], points[j + 1][1], width=1, fill="blue")
                small_star_edges.append(edge)

        # Draw the downward triangle with divided segments
        for i in range(3):
            x1, y1 = points_down[i * 2], points_down[i * 2 + 1]
            x2, y2 = points_down[(i * 2 + 2) % 6], points_down[(i * 2 + 3) % 6]
            points = divide_edge(x1, y1, x2, y2, segments_per_edge)
            for j in range(len(points) - 1):
                edge = canvas.create_line(points[j][0], points[j][1], points[j + 1][0], points[j + 1][1], width=1, fill="blue")
                small_star_edges.append(edge)

        # Highlight the selected edges in white
        for edge in selected_edges:
            index = self.edges.index(edge)  # Get the index of the selected edge from the main star
            small_edge_to_highlight = small_star_edges[index]  # Use the same index to get the corresponding small star edge
            canvas.itemconfig(small_edge_to_highlight, fill="white")  # Highlight it in white

    def display_result(self):
        """Display all selected edge sets as small Stars of David in a row."""
        self.display_canvas.delete("all")  # Clear the display canvas

        # For each selection set, display a small Star of David
        for idx, edge_set in enumerate(self.selected_sets):
            x_offset = 50 + idx * 70  # Adjust horizontal spacing for each small Star of David
            y_offset = 50  # Vertical offset remains the same
            self.draw_small_star_of_david(self.display_canvas, x_offset, y_offset, edge_set)


if __name__ == "__main__":
    root = tk.Tk()
    app = StarOfDavidGUI(root)
    root.mainloop()

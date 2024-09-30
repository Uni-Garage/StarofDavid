import tkinter as tk
import random

class StarOfDavidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Star of David Interaction")
        self.selected_edges = []
        self.temp_selection = []
        self.selected_sets = []  # To keep track of selections
        self.colors = ['red', 'green', 'blue', 'orange', 'purple']  # Different colors for selections

        # Main panel (Star of David interaction)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Canvas to display the Star of David
        self.canvas = tk.Canvas(self.main_frame, width=400, height=500)
        self.canvas.pack()

        # Draw the Star of David with individual selectable edges
        self.edges = self.create_star_of_david(self.canvas)

        # Panel for displaying results
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.display_canvas = tk.Canvas(self.result_frame, width=400, height=500, bg="black")
        self.display_canvas.pack()

        # Buttons for selecting and displaying
        self.select_next_button = tk.Button(self.root, text="Select Next", command=self.select_next)
        self.select_next_button.pack(pady=5)

        self.display_button = tk.Button(self.root, text="Display", command=self.display_result)
        self.display_button.pack(pady=5)

    def create_star_of_david(self, canvas):
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

    def select_next(self):
        """Store current selections and prepare for a new selection."""
        if self.temp_selection:
            self.selected_sets.append(self.temp_selection.copy())
            self.selected_edges.extend(self.temp_selection)
            self.temp_selection = []

    def display_result(self):
        """Display selected edges as lines in a ruler panel."""
        self.display_canvas.delete("all")  # Clear the display canvas

        # For each selection set, draw lines based on selected edges
        for idx, edge_set in enumerate(self.selected_sets):
            color = self.colors[idx % len(self.colors)]  # Cycle through colors
            for edge in edge_set:
                index = self.edges.index(edge)  # Get the index of the selected edge from the main star
                self.draw_edge_in_ruler_panel(self.display_canvas, index, color)

    def draw_edge_in_ruler_panel(self, canvas, index, color):
        """Draw the respective edge in the ruler panel."""
        # Calculate the starting and ending points based on the index
        segments_per_edge = 3
        x1, y1, x2, y2 = self.get_edge_coordinates(index, segments_per_edge)

        # Draw the edge in the ruler panel
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    def get_edge_coordinates(self, index, segments_per_edge):
        """Get the coordinates of an edge based on its index."""
        # Define points for the Star of David
        points_up = [200, 50, 300, 200, 100, 200]
        points_down = [200, 250, 300, 100, 100, 100]

        # Determine the triangle and edge
        if index < 9:  # First triangle
            i = index // segments_per_edge
            x1, y1 = points_up[i * 2], points_up[i * 2 + 1]
            x2, y2 = points_up[(i * 2 + 2) % 6], points_up[(i * 2 + 3) % 6]
        else:  # Second triangle
            index -= 9
            i = index // segments_per_edge
            x1, y1 = points_down[i * 2], points_down[i * 2 + 1]
            x2, y2 = points_down[(i * 2 + 2) % 6], points_down[(i * 2 + 3) % 6]

        return x1, y1, x2, y2

if __name__ == "__main__":
    root = tk.Tk()
    app = StarOfDavidGUI(root)
    root.mainloop()

import tkinter as tk

class StarOfDavidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Star of David Interaction")
        self.selected_edges = []
        self.temp_selection = []

        # Canvas to display the Star of David
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        # Draw the Star of David with individual selectable edges
        self.edges = self.create_star_of_david(self.canvas)

        # Button panel
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_selection)
        self.clear_button.grid(row=0, column=0)

        self.select_next_button = tk.Button(self.button_frame, text="Select-Next", command=self.select_next)
        self.select_next_button.grid(row=0, column=1)

        self.form_button = tk.Button(self.button_frame, text="Form", command=self.form_selected_edges)
        self.form_button.grid(row=0, column=2)

        # Label to display selected edges
        self.label = tk.Label(self.root, text="Selected Edges: None")
        self.label.pack()

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

    def select_next(self):
        self.selected_edges.extend(self.temp_selection)
        self.temp_selection = []
        self.label.config(text=f"Selected Edges: {len(self.selected_edges)} stored")

    def form_selected_edges(self):
        # Set all edges to black first
        for edge in self.edges:
            self.canvas.itemconfig(edge, fill="black")

        # Set the selected edges to green
        for edge in self.selected_edges:
            self.canvas.itemconfig(edge, fill="green")

        self.label.config(text=f"Formed {len(self.selected_edges)} edges (Green), others (Black)")

if __name__ == "__main__":
    root = tk.Tk()
    app = StarOfDavidGUI(root)
    root.mainloop()

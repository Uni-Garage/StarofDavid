import tkinter as tk
import cv2
import numpy as np
from tensorflow.keras.models import load_model

class StarOfDavidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Star of David Interaction")
        self.selected_sets = []  # Stores sets of selected edges
        self.temp_selection = []  # Stores currently selected edges

        # Load the Hebrew letter recognition model
        self.model = load_model('hebrew_letter_model.h5')  # Ensure your model is trained and saved

        # Main panel (Star of David interaction)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Canvas to display the Star of David
        self.canvas = tk.Canvas(self.main_frame, width=400, height=500)
        self.canvas.pack()

        # Label to show how many edges are selected
        self.label = tk.Label(self.main_frame, text="Selected Edges: 0")
        self.label.pack(pady=10)

        # Button to start Hebrew letter detection
        self.detect_button = tk.Button(self.main_frame, text="Detect Hebrew Letter", command=self.detect_hebrew_letter)
        self.detect_button.pack(pady=10)

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

    def detect_hebrew_letter(self):
        """Detect Hebrew letters using the camera feed."""
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Pre-process the frame for letter recognition
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (28, 28))  # Resize to match model input
            gray = gray.astype('float32') / 255.0  # Normalize
            gray = np.expand_dims(gray, axis=[0, -1])  # Reshape for model input

            # Predict the letter
            prediction = self.model.predict(gray)
            letter = np.argmax(prediction)

            # Draw the recognized letter on the frame
            cv2.putText(frame, f'Detected Letter: {letter}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show the frame with detection
            cv2.imshow('Hebrew Letter Detection', frame)

            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Call a method to draw the recognized pattern on the display canvas
            self.draw_recognized_pattern(letter)

        cap.release()
        cv2.destroyAllWindows()

    def draw_recognized_pattern(self, letter):
        """Draw recognized letter's pattern on the display canvas."""
        # Example patterns for demonstration; replace with actual patterns
        patterns = {
            0: [(100, 100), (150, 150), (200, 100)],  # Pattern for letter 0
            1: [(200, 200), (250, 250), (300, 200)],  # Pattern for letter 1
            # Add more letter patterns as needed
        }

        if letter in patterns:
            points = patterns[letter]
            for i in range(len(points) - 1):
                self.display_canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill="yellow", width=2)

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
            self.selected_sets.append(self.temp_selection[:])  # Copy the selection

        # Clear the temporary selection list and update color to indicate stored edges
        for edge in self.temp_selection:
            self.canvas.itemconfig(edge, fill="red")  # Change color to indicate confirmed selection

        self.temp_selection = []  # Reset the temporary selection list

        # Update label to show the total number of selected edges
        self.label.config(text=f"Total Confirmed Edges: {len(self.selected_sets)} sets")

    def display_result(self):
        """Display the final result of selected edges."""
        # This can include more visual elements or messages based on the selection
        for i, selected in enumerate(self.selected_sets):
            for edge in selected:
                self.canvas.itemconfig(edge, fill="purple")  # Highlight confirmed edges differently

        self.label.config(text=f"Final Display: {len(self.selected_sets)} sets")

if __name__ == "__main__":
    root = tk.Tk()
    app = StarOfDavidGUI(root)
    root.mainloop()

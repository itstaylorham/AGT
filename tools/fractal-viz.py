import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import glob
import os
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm

class FractalDataVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.frames = 100
        self.max_depth = 6
        self.data = None
        self.normalized_values = None
        
    def load_all_files(self):
        base_dir = "files/read_files/"
        files = glob.glob(os.path.join(base_dir, '**', '*.json'), recursive=True)
        
        if not files:
            print("No JSON files found in the specified directories.")
            return None

        data_list = []
        print("Loading files for fractal animation:")
        for file in files:
            print(f" - {file}")
            temp_data = pd.read_json(file)
            data_list.append(temp_data)
        
        self.data = pd.concat(data_list, ignore_index=True)
        
        # Normalize numerical columns for fractal parameters
        numerical_columns = self.data.select_dtypes(include=[np.number]).columns
        self.normalized_values = self.data[numerical_columns].apply(
            lambda x: (x - x.min()) / (x.max() - x.min())
        )
        return True

    def draw_fractal(self, x, y, length, angle, depth, color_val):
        if depth == 0:
            return
        
        # Calculate new points
        x2 = x + length * np.cos(angle)
        y2 = y + length * np.sin(angle)
        
        # Draw the line segment
        line = plt.Line2D([x, x2], [y, y2], 
                         color=plt.cm.viridis(color_val),
                         alpha=0.6,
                         linewidth=depth)
        self.ax.add_line(line)
        
        # Calculate new length and angles for branches
        new_length = length * 0.7
        angle_diff = np.pi * self.normalized_values.iloc[int(color_val * len(self.normalized_values))].mean()
        
        # Recurse for branches
        self.draw_fractal(x2, y2, new_length, angle + angle_diff, depth - 1, color_val)
        self.draw_fractal(x2, y2, new_length, angle - angle_diff, depth - 1, color_val)

    def init_animation(self):
        self.ax.clear()
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        self.ax.axis('off')
        return []

    def animate(self, frame):
        self.ax.clear()
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        self.ax.axis('off')
        
        # Calculate animation parameters based on frame
        t = frame / self.frames
        color_val = t
        
        # Initial parameters for the main trunk
        start_x = 0
        start_y = -1.5
        start_length = 1
        start_angle = np.pi/2 + np.sin(t * 2 * np.pi) * 0.1
        
        # Draw the fractal tree
        self.draw_fractal(start_x, start_y, start_length, start_angle, self.max_depth, color_val)
        
        # Add title with current data values
        if len(self.normalized_values.columns) > 0:
            current_idx = int(t * (len(self.normalized_values) - 1))
            values_str = " | ".join([
                f"{col}: {self.data[col].iloc[current_idx]:.2f}"
                for col in self.normalized_values.columns[:3]  # Show first 3 columns
            ])
            plt.title(f"Data Fractal Animation\n{values_str}", pad=20)
        
        return []

    def create_animation(self, save_path=None):
        if self.data is None:
            print("No data loaded. Please load data first.")
            return
        
        print("\nGenerating fractal animation...")
        anim = FuncAnimation(
            self.fig, 
            self.animate,
            init_func=self.init_animation,
            frames=tqdm(range(self.frames)),
            interval=50,
            blit=True
        )
        
        if save_path:
            print(f"\nSaving animation to {save_path}")
            anim.save(save_path, writer='pillow', fps=20)
            print("Animation saved successfully!")
        else:
            plt.show()

def main():
    visualizer = FractalDataVisualizer()
    if visualizer.load_all_files():
        # Create and display the animation
        visualizer.create_animation()
        # Optionally save the animation
        # visualizer.create_animation('fractal_animation.gif')

if __name__ == "__main__":
    main()
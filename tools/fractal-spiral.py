import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from tqdm import tqdm

class MandelbrotVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.frames = 150
        self.max_iter = 100
        self.data = None
        
    def load_data(self):
        try:
            self.data = pd.read_json('sesh.json')
            print("Successfully loaded sesh.json")
            return True
        except FileNotFoundError:
            print("Error: sesh.json not found!")
            return False
            
    def mandelbrot(self, h, w, max_iter, zoom, center):
        y, x = np.ogrid[-1.4:1.4:h*1j, -2:0.8:w*1j]
        c = x + y*1j
        c = c/zoom + center
        z = c
        divtime = max_iter + np.zeros(z.shape, dtype=int)

        for i in range(max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2

        return divtime
    
    def init_animation(self):
        self.ax.clear()
        return []

    def animate(self, frame):
        self.ax.clear()
        
        # Calculate zoom based on frame
        t = frame / self.frames
        zoom = np.exp(t * 10)  # Faster exponential zoom
        
        # Use sensor data to influence the center point if available
        if self.data is not None:
            idx = int(t * (len(self.data) - 1))
            temp = self.data['Temperature'].iloc[idx]
            moisture = self.data['Moisture'].iloc[idx]
            center = complex(-0.7 + temp/100, moisture/200)
        else:
            center = complex(-0.7, 0)

        # Generate Mandelbrot set
        h, w = 1000, 1500
        mandel = self.mandelbrot(h, w, self.max_iter, zoom, center)
        
        # Create the blue glow effect
        plt.imshow(mandel, cmap='Blues_r', extent=[-2, 0.8, -1.4, 1.4])
        
        # Style the plot
        self.ax.set_facecolor('black')
        self.fig.patch.set_facecolor('black')
        self.ax.axis('off')
        
        # Add title with current sensor values if available
        if self.data is not None:
            values_str = f"Temp: {temp:.1f}°C | Moisture: {moisture}%"
            plt.title(values_str, color='white', pad=20)
    
        return[]

    def create_animation(self, save_path=None):
        plt.style.use('dark_background')
        
        print("\nGenerating Mandelbrot zoom animation...")
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
            anim.save(save_path, writer='pillow', fps=30)
            print("Animation saved successfully!")
        else:
            plt.show()

def main():
    visualizer = MandelbrotVisualizer()
    visualizer.load_data()
    visualizer.create_animation()
    # Optionally save: visualizer.create_animation('mandelbrot.gif')

if __name__ == "__main__":
    main()
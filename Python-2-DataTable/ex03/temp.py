import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import threading
import time

class AutoSliderPlot:
    def __init__(self):
        # Set up the figure and axis
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        
        # Create some data to plot
        self.x = np.linspace(0, 2 * np.pi, 100)
        self.y = np.sin(self.x)
        self.line, = self.ax.plot(self.x, self.y, label="Sine Wave")
        
        # Set up the slider axis and slider widget
        self.slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
        self.slider = Slider(self.slider_ax, 'Phase', 0, 2 * np.pi, valinit=0)
        
        # Connect the slider to the update function
        self.slider.on_changed(self.update)
        
        # Initialize threading variables
        self.running = False
        self.thread = None

        # Add start and stop buttons
        self.start_ax = plt.axes([0.7, 0.02, 0.1, 0.05])
        self.stop_ax = plt.axes([0.8, 0.02, 0.1, 0.05])
        
        # btn_play = Button(ax_play, '\u25B6')  # Triangle pour Play
        # btn_pause = Button(ax_pause, '\u23F8')  # Deux barres pour Pause

        self.start_button = plt.Button(self.start_ax, '\u25B6')
        self.stop_button = plt.Button(self.stop_ax, r'$\mathbf{| |}$')

        self.start_button.on_clicked(self.start)
        self.stop_button.on_clicked(self.stop)

    def update(self, val):
        """Update the plot based on the slider value."""
        phase = self.slider.val
        self.line.set_ydata(np.sin(self.x + phase))
        self.fig.canvas.draw_idle()

    def auto_update(self):
        """Automatically move the slider."""
        while self.running:
            current_value = self.slider.val
            next_value = current_value + 0.1
            if next_value > 2 * np.pi:
                next_value = 0  # Reset to the start
            self.slider.set_val(next_value)
            time.sleep(0.1)  # Adjust speed of slider movement

    def start(self, event):
        """Start the automatic slider movement."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.auto_update)
            self.thread.start()

    def stop(self, event):
        """Stop the automatic slider movement."""
        self.running = False
        if self.thread:
            self.thread.join()

    def show(self):
        """Display the plot."""
        plt.show()

if __name__ == "__main__":
    app = AutoSliderPlot()
    app.show()

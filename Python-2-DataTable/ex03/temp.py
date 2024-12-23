import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class ResponsivePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)

        # Initialize data and plot
        self.x = np.linspace(0, 2 * np.pi, 100)
        self.y = np.sin(self.x)
        self.line, = self.ax.plot(self.x, self.y, label="Sine Wave")

        # Slider
        self.slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
        self.slider = Slider(self.slider_ax, 'Phase', 0, 2 * np.pi, valinit=0)
        self.slider.on_changed(self.update_slider)

        # Buttons
        self.play_ax = plt.axes([0.7, 0.02, 0.1, 0.05])
        self.pause_ax = plt.axes([0.8, 0.02, 0.1, 0.05])
        self.play_button = Button(self.play_ax, '▶')
        self.pause_button = Button(self.pause_ax, r'$\mathbf{| |}$')
        self.play_button.on_clicked(self.start_animation)
        self.pause_button.on_clicked(self.stop_animation)

        # Animation state
        self.running = False
        self.current_frame = 0
        self.anim = None

        # Font sizes
        self.title_fontsize = 15
        self.label_fontsize = 10
        self.legend_fontsize = 8
        self.annotation_fontsize = 10

        # Connect resize event
        self.fig.canvas.mpl_connect('resize_event', self.on_resize)

    def adjust_font_sizes(self):
        """Adjust font sizes dynamically based on figure size."""
        fig_width, fig_height = self.fig.get_size_inches()
        scale = min(fig_width, fig_height) / 10
        self.title_fontsize = 15 * scale
        self.label_fontsize = 10 * scale
        self.legend_fontsize = 8 * scale
        self.annotation_fontsize = 10 * scale

    def on_resize(self, event):
        """Handle resize events to adjust layout and font sizes."""
        fig_width, fig_height = self.fig.get_size_inches()
        scale = min(fig_width / 10, fig_height / 6)

        self.fig.subplots_adjust(
            top=0.97,
            bottom=0.1,
            left=0.05,
            right=0.99,
            hspace=0.13 * scale,
            wspace=0.2 * scale
        )

        self.adjust_font_sizes()

        # Adjust axes fonts
        self.ax.title.set_fontsize(self.title_fontsize)
        self.ax.xaxis.label.set_fontsize(self.label_fontsize)
        self.ax.yaxis.label.set_fontsize(self.label_fontsize)
        for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            label.set_fontsize(self.label_fontsize)

        plt.draw()

    def update_slider(self, val):
        """Update plot based on slider value."""
        phase = self.slider.val
        self.line.set_ydata(np.sin(self.x + phase))
        self.fig.canvas.draw_idle()

    def start_animation(self, event):
        """Start animation."""
        if self.running:
            return

        self.running = True
        self.anim = self.fig.canvas.new_timer(interval=100)
        self.anim.add_callback(self.animate)
        self.anim.start()

    def stop_animation(self, event):
        """Stop animation."""
        self.running = False
        if self.anim:
            self.anim.stop()

    def animate(self):
        """Update the slider for animation."""
        next_value = self.slider.val + 0.1
        if next_value > 2 * np.pi:
            next_value = 0
        self.slider.set_val(next_value)

    def show(self):
        """Display the plot."""
        plt.show()

if __name__ == "__main__":
    app = ResponsivePlot()
    app.show()

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox


# fig, axes = plt.subplot_mosaic(
#     [
#         ["log", "log", "lin", "lin"],
#         ["corr_log", "corr_log", "corr_", "E"]
#     ],
#     figsize=(10, 6)
# )

fig, axes = plt.subplot_mosaic(
    [
        ["A", "A", "B", "B"],
        ["C", "C", "D", "E"]
    ],
    figsize=(10, 6)
)


fig.subplots_adjust(top=0.9, bottom=0.15, left=0.1, right=0.95, hspace=0.4, wspace=0.4)

axes["A"].plot([1, 2, 3], [1, 4, 9], label="Quadratic")
axes["A"].legend()
axes["B"].scatter([1, 2, 3], [9, 4, 1], label="Scatter", color="orange")
axes["B"].legend()
axes["C"].bar([1, 2, 3], [1, 2, 3], label="Bar", color="green")
axes["C"].legend()
axes["D"].hist([1, 2, 2, 3, 3, 3], bins=3, label="Histogram", color="purple")
axes["D"].legend()
axes["E"].scatter([1, 2, 3], [9, 4, 1], label="Scatter", color="orange")
axes["E"].legend()

ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
slider = Slider(ax_slider, 'Value', 0, 10, valinit=5)

def update(val):
    current_val = slider.val
    axes["A"].lines[0].set_ydata([x**2 + current_val for x in [1, 2, 3]])
    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()

import plotext as plt
l, n = 1000, 2
x = range(1, l + 1)
y = plt.sin(l, n)
plt.plot(x, y, label = "periodic signal", color = "violet", marker = "small")
plt.plotsize(100, 30)
plt.grid(True)
plt.title("Plot Style Example")
plt.xlabel("x axis label")
plt.ylabel("y axis label")
plt.canvas_color("white")
plt.axes_color("cloud")
plt.ticks_color("iron")
plt.xaxes(1, 0)
plt.yaxes(1, 0)
plt.ticks(10)
plt.show()

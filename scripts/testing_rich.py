import time
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn

# Create layout
layout = Layout()
layout.split_column(
    Layout(name="top", size=3),
    Layout(name="bottom")
)

layout["top"].update(Panel("Press Enter simulation running...", title="Status"))

# Create Progress (DO NOT call progress.start())
progress = Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.0f}%",
    TimeRemainingColumn(),
    expand=True
)

task_id = progress.add_task("Collecting RSSI...", total=100)

with Live(layout, refresh_per_second=10):

    # Put progress into layout
    layout["bottom"].update(Panel(progress, title="RSSI Scan Progress"))

    for i in range(100):
        time.sleep(0.05)
        progress.update(task_id, advance=1)

    # After completion, replace progress with something else
    layout["bottom"].update(
        Panel("Scan Complete.\nAverage RSSI: -63 dBm", title="Results")
    )

    time.sleep(3)
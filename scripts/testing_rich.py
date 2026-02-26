from rich.live import Live
from rich.panel import Panel
from rich.text import Text
import keyboard

options = ["lo", "wlp0s20f3", "enp0s31f6"]
selected = 0

def render():
    text = Text()
    for i, opt in enumerate(options):
        if i == selected:
            text.append(f"> {opt}\n", style="bold green")
        else:
            text.append(f"  {opt}\n")
    return Panel(text, title="Select WLAN Interface")

with Live(render(), refresh_per_second=10, screen=True) as live:
    while True:
        event = keyboard.read_event()
        if event.event_type != "down":
            continue

        if event.name == "up":
            selected = (selected - 1) % len(options)
        elif event.name == "down":
            selected = (selected + 1) % len(options)
        elif event.name == "enter":
            break

        live.update(render())

print("Selected:", options[selected])
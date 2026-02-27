import random
import time
from math import sqrt

from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text


# ----------------------------
# Fake Data Generators
# ----------------------------

def fake_coordinates(x, y):
    x += random.choice([-1, 0, 1])
    y += random.choice([-1, 0, 1])
    return x, y


def fake_rssi_data():
    base_macs = [
        "7C:F1:7E:CC:D2:52",
        "AA:BB:CC:DD:EE:01",
        "12:34:56:78:90:AB",
        "DE:AD:BE:EF:CA:FE",
    ]

    data = {}
    for mac in base_macs:
        data[mac] = random.randint(-90, -30)

    return data


# ----------------------------
# Layout Builder
# ----------------------------

def make_layout():
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )

    layout["body"].split_row(
        Layout(name="coords", ratio=1),
        Layout(name="rssi", ratio=2)
    )

    return layout


# ----------------------------
# Panel Builders
# ----------------------------

def build_header():
    header_text = Text()
    header_text.append("WLAN: wlp0s20f3", style="bold cyan")
    header_text.append(" | ")
    header_text.append("Mode: Monitor", style="bold green")
    header_text.append(" | ")
    header_text.append("Sniff: Active", style="bold yellow")

    return Panel(Align.center(header_text), title="System Status")


def build_coords_panel(x, y):
    distance = round(sqrt(x**2 + y**2), 2)

    text = Text()
    text.append(f"X: {x}\n", style="bold cyan")
    text.append(f"Y: {y}\n\n", style="bold magenta")
    text.append(f"Distance from origin: {distance}")

    return Panel(text, title="Coordinates")


def build_rssi_table(rssi_dict):
    table = Table(title="RSSI Signals", expand=True)

    table.add_column("MAC Address", style="cyan")
    table.add_column("RSSI (dBm)", justify="right")
    table.add_column("Strength", justify="left")

    sorted_items = sorted(rssi_dict.items(), key=lambda x: x[1], reverse=True)

    for mac, rssi in sorted_items:
        bars = "█" * max(1, int((100 + rssi) / 5))
        table.add_row(mac, str(rssi), bars)

    return table


def build_footer():
    footer_text = Text(
        "Arrows: Move | M: Change Mode | S: Scan | Q: Quit",
        style="bold white"
    )

    return Panel(Align.center(footer_text))


# ----------------------------
# Main Live Loop
# ----------------------------

def main():
    layout = make_layout()

    x, y = 0, 0

    with Live(layout, refresh_per_second=4, screen=True):

        while True:
            # Update fake data
            x, y = fake_coordinates(x, y)
            rssi_data = fake_rssi_data()

            # Update layout sections
            layout["header"].update(build_header())
            layout["coords"].update(build_coords_panel(x, y))
            layout["rssi"].update(build_rssi_table(rssi_data))
            layout["footer"].update(build_footer())

            time.sleep(0.5)


if __name__ == "__main__":
    main()
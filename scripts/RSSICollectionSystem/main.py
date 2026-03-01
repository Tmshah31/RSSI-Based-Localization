from RSSIsystem import *




def list_all_net_interfaces():
    # Get all network interfaces
    interfaces = psutil.net_if_addrs()
    cards = []

    for interface_name in interfaces:
        cards.append(interface_name)

    return cards




def create_menu(options, selected, menu_title):
    

    def render(options,selected, menu_title):
        text = Text()
        for i, opt in enumerate(options):
            if i == selected:
                text.append(f">{opt}\n", style="bold green")
            else:
                text.append(f" {opt}\n")

        text.append("\nESC to exit Enter to Proceed", style= "bold magenta")

        return Panel(text, title=menu_title)
    
    with Live(render(options, selected, menu_title), refresh_per_second=10, screen=True) as live:
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type != "down":
                continue

            if event.name == "up":
                selected = (selected - 1) % len(options)
            elif event.name == "down":
                selected = (selected + 1) % len(options)
            elif event.name == "enter":
                break
            elif event.name == "esc":
                exit()

            live.update(render(options, selected, menu_title))

        rprint(f"{menu_title}: {options[selected]}")  

        console.clear()

        return selected  
    



def create_layout():

    layout = Layout()

    layout.split_column(
        Layout(name="header"),
        Layout(name="body"),
        Layout(name="footer")
    )

    layout["body"].split_row(
        Layout(name="coords"),
        Layout(name="RSSI")
    )

    return layout


def create_header(options):

    text = Text()
    text.append(f"WLAN Card: {options[0]}", style="italic bold green")
    text.append(" | ")
    text.append(f"Mode: {options[1]}", style="italic bold magenta")

    return Align.center(Panel.fit(Align.center(text), title="Systems Settings"))


def create_footer():

    text = Text()
    text.append(f"Move: Arrows")
    text.append(" | ")
    text.append(f"Sniff: Enter")
    text.append(" | ")
    text.append(f"Quit: Esc")

    return Panel(Align.center(text), title="Function Keys")

def create_coords(x,y):
    distance = round(np.sqrt(x**2 + y**2))


    text = Text()
    text.append(f">>X: {x}<<\n", style="bold magenta")
    text.append(f">>Y: {y}<<\n", style="bold green")
    text.append(f">>Distance from Origin: {distance}<<\n", style="bold yellow")

    return Panel(Align.center(text), title="Current Coordinates")


def RSSI_table(rssi_dict):

    rssi_table = Table()

    rssi_table.add_column("MAC Address", justify="center")
    rssi_table.add_column("Signal Strength", justify="center")

    for key, value in rssi_dict.items():
        rssi_table.add_row(key, str(value))

    return Panel(Align.center(rssi_table), title="RSSI Value")

def collecting_RSSI():
    
    text = Text()
    text.append(f"Collecting RSSI Value...")

    return Panel(text, title="RSSI Values")


    
if __name__ == "__main__":

    #Available Modes
    modes = ["Manual", "Auto (GNSS)"]
    selected_mode = 0

    #Scan cards and create a menu
    cards = list_all_net_interfaces()
    selected_card = 0

    selected_card = create_menu(cards, selected_card, "WLAN CARD SELECTION")


    collector = RSSI("/home/tmshah/Desktop/RSSI-Based-Localization/MAC.txt", cards[selected_card], 5)
    collector.load_file()

    collector.Monitor_Mode()

    selected_mode = create_menu(modes, selected_mode, "MODE SELECTION" )

    options = [cards[selected_card], modes[selected_mode]]
    
    

    #Manual Mode
    if modes[selected_mode] == modes[0]:

        layout = create_layout()

        layout["header"].update(create_header(options))
        layout["coords"].update(create_coords(collector.X, collector.Y))
        layout["RSSI"].update(RSSI_table(collector.average_signal_strength))
        layout["footer"].update(create_footer())

        with Live(layout, refresh_per_second=4, screen=True):
            while(True):
                key = keyboard.read_event()
                if key.event_type == keyboard.KEY_DOWN:
                    if key.name == "up":
                        collector.Y += 1
                        layout["header"].update(create_header(options))
                        layout["coords"].update(create_coords(collector.X, collector.Y))
                        layout["RSSI"].update(RSSI_table(collector.average_signal_strength))
                        layout["footer"].update(create_footer())
                    if key.name == "down":
                        collector.Y -= 1
                        layout["header"].update(create_header(options))
                        layout["coords"].update(create_coords(collector.X, collector.Y))
                        layout["RSSI"].update(RSSI_table(collector.average_signal_strength))
                        layout["footer"].update(create_footer())
                    if key.name == "right":
                        collector.X += 1
                        layout["header"].update(create_header(options))
                        layout["coords"].update(create_coords(collector.X, collector.Y))
                        layout["RSSI"].update(RSSI_table(collector.average_signal_strength))
                        layout["footer"].update(create_footer())

                    if key.name == "left":
                        collector.X -= 1
                        layout["header"].update(create_header(options))
                        layout["coords"].update(create_coords(collector.X, collector.Y))
                        layout["RSSI"].update(RSSI_table(collector.average_signal_strength))
                        layout["footer"].update(create_footer())
                    if key.name == "enter":

                        collector.start_thread()
                        
                        progress = Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            BarColumn(),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                        )

                        #Update the panel with rssi using a different layout:
                        
                        task = progress.add_task("Collecting RSSI Values", total = 6)
                        while collector.thread.is_alive():


        
                            layout["header"].update(create_header(options))
                            layout["coords"].update(create_coords(collector.X, collector.Y))
                            progress.update(task, advance=1)
                            layout["RSSI"].update(Panel(progress, title="RSSI Values being collected"))
                            layout["footer"].update(create_footer())

                            time.sleep(1)

                        
                        
                        layout["header"].update(create_header(options))
                        layout["coords"].update(create_coords(collector.X, collector.Y))
                        layout["RSSI"].update(RSSI_table(collector.average_signal_strength))
                        layout["footer"].update(create_footer())


                        

                    if key.name == 'esc':

                        exit()

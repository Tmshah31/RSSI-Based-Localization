from RSSIsystem import *




def list_all_net_interfaces():
    # Get all network interfaces
    interfaces = psutil.net_if_addrs()
    cards = []

    print("Available Network Cards:")
    for interface_name in interfaces:
        cards.append(interface_name)

    return cards




def create_menu(options, selected, menu_title):
    

    def render(options,selected, menu_title):
        text = Text()
        for i, opt in enumerate(options):
            if i == selected:
                text.append(f">{opt}\n", style="bold magenta")
            else:
                text.append(f" {opt}\n")

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

            live.update(render(options, selected, menu_title))

        rprint(f"{menu_title}: {options[selected]}")  

        return selected  


if __name__ == "__main__":

    modes = ["Manual", "Auto (GNSS)"]
    selected_mode = 0

    cards = list_all_net_interfaces()
    selected_card = 0

    # for i in range(len(cards)):
    #     print(f"{i}:{cards[i]}")

    # selected = int(input("Select the card for WIFI sniff:"))

    # print(f"{cards[selected]} has been chosen for sniff")

    selected_card = create_menu(cards, selected_card, "WLAN CARD SELECTION")


    collector = RSSI("/home/tshah/Desktop/RSSI-Based-Localization/MAC.txt", cards[selected_card], 5)
    collector.load_file()

    collector.Monitor_Mode()

    selected_mode = create_menu(modes, selected_mode, "MODE SELECTION" )
    
    

    #Manual Mode
    if modes[selected_mode] == modes[0]:
        
        while(True):
            key = keyboard.read_event(suppress=True)
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == "up":
                    collector.Y += 1
                    print(f"Y: {collector.Y}")
                if key.name == "down":
                    collector.Y -= 1
                    print(f"Y: {collector.Y}")
                if key.name == "right":
                    collector.X += 1
                    print(f"X: {collector.X}")
                if key.name == "left":
                    collector.X -= 1
                    print(f"X: {collector.X}")
                if key.name == "enter":

                    collector.start_thread()

                if key.name == 'esc':

                    exit()

import netifaces
import subprocess
import ipaddress
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()

def get_ip_address_and_netmask(interface):
    try:
        addrs = netifaces.ifaddresses(interface)
        ip_info = addrs[netifaces.AF_INET][0]
        return ip_info['addr'], ip_info['netmask']
    except (KeyError, IndexError):
        return None, None

def calculate_network_range(ip_address, netmask):
    network = ipaddress.IPv4Network(f"{ip_address}/{netmask}", strict=False)
    return str(network)

def run_netdiscover(interface, network_range):
    command = f"sudo netdiscover -i {interface} -r {network_range}"
    try:
        console.print(f"[bold green]Running command:[/bold green] [bold blue]{command}[/bold blue]", style="bold yellow")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Command '{command}' failed with error: {e}[/bold red]")

def main():
    # Červený ASCII art
    ascii_art = """
[bold red]
███████╗██╗  ██╗██╗███████╗██╗     
██╔════╝██║  ██║██║██╔════╝██║     
███████╗███████║██║█████╗  ██║     
╚════██║██╔══██║██║██╔══╝  ██║     
███████║██║  ██║██║███████╗███████╗
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
[/bold red]
    """
    console.print(ascii_art, justify="center")

    console.print(Panel(Text("Netdiscover Launcher", justify="center", style="bold cyan"), border_style="bold green"))

    interface = 'wlan0'
    ip_address, netmask = get_ip_address_and_netmask(interface)
    
    if ip_address and netmask:
        network_range = calculate_network_range(ip_address, netmask)
        console.print(f"[bold cyan]IP address of {interface}: [bold green]{ip_address}[/bold green]", style="bold magenta")
        console.print(f"[bold cyan]Network range: [bold yellow]{network_range}[/bold yellow]", style="bold magenta")
        run_netdiscover(interface, network_range)
    else:
        console.print(f"[bold red]Could not get IP address or netmask for interface {interface}[/bold red]")

if __name__ == "__main__":
    main()


import os
import re
import sys
import json
import asyncio
import datetime
import random
import colorsys
from telethon import TelegramClient
from telethon.errors import FloodWaitError, PeerIdInvalidError, RPCError
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

api_id = 123123
api_hash = 'api-hash'
CONFIG_FILE = "config.json"

console = Console()
logs_list = []

def rgb_to_str(rgb):
    return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"


def lerp(a, b, t):
    return int(a + (b - a) * t)


def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)


def random_neon_color():
    h = random.random()
    s = random.uniform(0.7, 1.0)
    l = random.uniform(0.45, 0.6)
    return hsl_to_rgb(h, s, l)


def generate_gradient(start_rgb, end_rgb, steps):
    gradient = []
    for i in range(steps):
        t = i / max(steps - 1, 1)
        gradient.append((
            lerp(start_rgb[0], end_rgb[0], t),
            lerp(start_rgb[1], end_rgb[1], t),
            lerp(start_rgb[2], end_rgb[2], t),
        ))
    return gradient


def generate_banner():
    lines = [
        "==================================================",
        "·▄▄▄▄   ▄▄▄· ▄▄▄  .▄▄▄      • ▌ ▄ ·. .▄▄ ·  ▄▄ • ",
        "██▪ ██ ▐█ ▀█ ▀▄ █·▐▀•▀█     ·██ ▐███▪▐█ ▀. ▐█ ▀ ▪",
        "▐█· ▐█▌▄█▀▀█ ▐▀▀▄ █▌·.█▌    ▐█ ▌▐▌▐█·▄▀▀▀█▄▄█ ▀█▄",
        "██. ██ ▐█ ▪▐▌▐█•█▌▐█▪▄█·    ██ ██▌▐█▌▐█▄▪▐█▐█▄▪▐█",
        "▀▀▀▀▀•  ▀  ▀ .▀  ▀·▀▀█.     ▀▀  █▪▀▀▀ ▀▀▀▀ ·▀▀▀▀ ",
        "[+] This project developed by H04x LLC.",
        "[@] t.me/sychoticdox",
        "=================================================="
    ]

    text = Text()
    start = hsl_to_rgb(random.random(), 1, 0.5)
    end = hsl_to_rgb(random.random(), 1, 0.5)
    gradient = generate_gradient(start, end, len(lines))

    for i, line in enumerate(lines):
        if line.startswith("["):  
            color = random_neon_color()
            text.append(line + "\n", style=rgb_to_str(color))
        else:
            color = gradient[i]
            text.append(line + "\n", style=rgb_to_str(color))

    return text

def add_log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    
    logs_list.append(formatted_message)
    if len(logs_list) > 10:
        logs_list.pop(0)
        
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(formatted_message + "\n")

def add_error(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] ERROR: {message}"
    
    with open("errors.txt", "a", encoding="utf-8") as f:
        f.write(formatted_message + "\n")

def make_layout():
    layout = Layout()
    layout.split(
        Layout(name="banner", size=12),
        Layout(name="body")
    )
    
    layout["banner"].update(generate_banner())
    
    log_content = "\n".join(logs_list)
    layout["body"].update(Panel(log_content, title="Sistem Günlükleri (Son 10)", border_style="white"))
    return layout

def parse_forward_link(link):
    pattern = r"t\.me/(?:c/)?([^/]+)/(\d+)"
    match = re.search(pattern, link)
    if match:
        channel = match.group(1)
        msg_id = int(match.group(2))
        if channel.isdigit():
            channel = int(f"-100{channel}")
        return channel, msg_id
    return None, None

async def main():
    if not os.path.exists(CONFIG_FILE):
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(generate_banner())
        
        id_file = console.input("[bold white]Kanal ID listesi dosya adı (örn: id.txt): [/bold white]")
        if not os.path.exists(id_file):
            console.print("[bold red]Hata: ID listesi dosyası bulunamadı.[/bold red]")
            return
            
        forward_link = console.input("\n[bold white]Yönlendirilecek (Forward) mesaj linki (t.me/...): [/bold white]")
        forward_channel, forward_msg_id = parse_forward_link(forward_link)
        if not forward_channel or not forward_msg_id:
            console.print("[bold red]Hata: Geçersiz Telegram mesaj link yapısı.[/bold red]")
            return

        console.print("\n[bold white]Zaman Aralığı Ayarı (Preset):[/bold white]")
        console.print("1 - 10 dakikada bir")
        console.print("2 - 15 dakikada bir")
        console.print("3 - 30 dakikada bir")
        console.print("4 - Özel süre tanımla (Dakika)")
        time_choice = console.input("[bold white]Seçiminiz (1/4): [/bold white]")
        
        if time_choice == "1":
            interval = 10 * 60
        elif time_choice == "2":
            interval = 15 * 60
        elif time_choice == "3":
            interval = 30 * 60
        elif time_choice == "4":
            custom_min = float(console.input("[bold white]Kaç dakikada bir gönderilsin?: [/bold white]"))
            interval = custom_min * 60
        else:
            console.print("[bold red]Geçersiz seçim, varsayılan 15 dakika ayarlandı.[/bold red]")
            interval = 15 * 60
            

        config_data = {
            "id_file": id_file,
            "forward_link": forward_link,
            "interval": interval
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as cf:
            json.dump(config_data, cf, indent=4, ensure_ascii=False)
        console.print("[bold green]\n[+] Ayarlar config.json dosyasına kaydedildi.[/bold green]")
        await asyncio.sleep(2)
    else:
        with open(CONFIG_FILE, "r", encoding="utf-8") as cf:
            config_data = json.load(cf)
        
        id_file = config_data.get("id_file")
        forward_link = config_data.get("forward_link")
        interval = config_data.get("interval", 15 * 60)
        
        forward_channel, forward_msg_id = parse_forward_link(forward_link)
        if not os.path.exists(id_file) or not forward_channel or not forward_msg_id:
            console.print("[bold red]Hata: config.json dosyasındaki veriler veya ID listesi geçersiz! Lütfen config.json dosyasını silip tekrar başlatın.[/bold red]")
            return

    with open(id_file, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip()]

    client = TelegramClient('session_auto_post', api_id, api_hash)
    await client.start()
    
    with Live(make_layout(), refresh_per_second=1, screen=False) as live:
        add_log(f"Saf Forward Modu başlatıldı. (Ayarlar {CONFIG_FILE} dosyasından alındı)")
        live.update(make_layout())
        
        while True:
            for target in targets:
                try:
                    if target.startswith("-100") or target.isdigit():
                        peer = int(target)
                    else:
                        peer = target
                        
                    await client.forward_messages(peer, forward_msg_id, forward_channel)
                    add_log(f"Başarılı: {target} adresine mesaj forward edildi.")
                except FloodWaitError as e:
                    err_msg = f"FloodWait Hatası: {e.seconds} saniye bekleniyor."
                    add_log(err_msg)
                    add_error(err_msg)
                    live.update(make_layout())
                    await asyncio.sleep(e.seconds)
                except PeerIdInvalidError:
                    err_msg = f"Geçersiz ID/Username Hatası: {target} bulunamadı."
                    add_log(err_msg)
                    add_error(err_msg)
                except RPCError as e:
                    if "CHAT_WRITE_FORBIDDEN" in str(e):
                        err_msg = f"Yazma Kısıtlaması ({target}): Gruba/Kanala yazılamıyor."
                    elif "FLOOD" in str(e) or "SLOWMODE" in str(e):
                        err_msg = f"Telegram Kısıtlaması/Spam Engeli: {str(e)}"
                    else:
                        err_msg = f"Telegram API Hatası: {str(e)}"
                    add_log(err_msg)
                    add_error(err_msg)
                except Exception as e:
                    err_msg = f"Hata ({target}): {str(e)}"
                    add_log(err_msg)
                    add_error(err_msg)
                
                live.update(make_layout())
                await asyncio.sleep(2 + random.uniform(0.2, 0.5))
            
            add_log(f"Döngü tamamlandı. {interval / 60} dakika bekleniyor...")
            live.update(make_layout())
            await asyncio.sleep(interval)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)

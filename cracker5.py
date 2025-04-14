#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# CrackSmith - Terminal Hash Cracker

import os, sys, json, time, signal, queue, bcrypt, psutil, threading, argparse, hashlib, requests
from datetime import timedelta, datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.text import Text
from rich.live import Live
from itertools import cycle

# === Configuration ===
DEFAULT_WORDLIST = "rockyou.txt"
RESUME_FILE = "resume.json"
REPORT_HTML = "crack_report.html"
spinner = cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
console = Console()
stop_flag = False
MAX_THREADS = os.cpu_count() or 4
THREAD_COUNT = 4

# Handle Ctrl+C
signal.signal(signal.SIGINT, lambda sig, frame: stop())
def stop():
    global stop_flag
    stop_flag = True
    console.print("\n[red]🛑 Cracking halted by user.[/red]")

class CrackerStats:
    def __init__(self):
        self.start_time = time.time()
        self.attempts = 0
        self.last_passwords = []
        self.total_passwords = 0
        self.cpu_usage = 0
        self.mem_usage = 0
        self.gpu_usage = 0
        self.found = False
        self.has_gpu = False
        try:
            from pynvml import nvmlInit
            nvmlInit()
            self.has_gpu = True
        except:
            pass

    def update(self, password):
        self.attempts += 1
        if self.attempts % 1000 == 0:
            clean = password.decode('utf-8', 'ignore')[:25]
            self.last_passwords = [clean] + self.last_passwords[:3]
        self.cpu_usage = psutil.cpu_percent()
        self.mem_usage = psutil.virtual_memory().percent

    @property
    def elapsed(self): return time.time() - self.start_time
    @property
    def rate(self): return self.attempts / self.elapsed if self.elapsed > 0 else 0
    @property
    def eta(self):
        if self.rate == 0 or self.total_passwords == 0: return "∞"
        return str(timedelta(seconds=int((self.total_passwords - self.attempts) / self.rate)))[:15]

def detect_hash_type(h):
    h = h.decode() if isinstance(h, bytes) else h
    if h.startswith("$2y$") or h.startswith("$2b$"): return "bcrypt"
    if len(h) == 32: return "md5"
    if len(h) == 40: return "sha1"
    if len(h) == 64: return "sha256"
    return "unknown"

def render_stats(stats, spinner_char, hash_type):
    header = Panel(Text(f"{spinner_char} CrackSmith", justify="center", style="bold red"), expand=False)
    info = Table.grid(expand=True)
    info.add_column(justify="right", style="bold")
    info.add_column()
    info.add_row("Hash Type:", hash_type)
    info.add_row("Wordlist:", WORDLIST_FILE)

    stats_table = Table.grid(expand=True)
    stats_table.add_column(justify="right", style="cyan")
    stats_table.add_column()
    stats_table.add_row("Attempts:", f"{stats.attempts:,}")
    stats_table.add_row("Left:", f"{max(0, stats.total_passwords - stats.attempts):,}")
    stats_table.add_row("Speed:", f"{stats.rate:,.1f}/s")
    stats_table.add_row("Threads:", f"{THREAD_COUNT} / {MAX_THREADS}")
    stats_table.add_row("Elapsed:", str(timedelta(seconds=int(stats.elapsed)))[:10])
    stats_table.add_row("ETA:", stats.eta)

    system = Table.grid(); system.add_column()
    load = f"CPU {stats.cpu_usage:.1f}% | RAM {stats.mem_usage:.1f}%"
    if stats.has_gpu: load += f" | GPU {stats.gpu_usage:.1f}%"
    system.add_row(f"[green]{load}[/green]")

    sample = Panel(Text("\n".join([f"→ {p}" for p in stats.last_passwords]) or "(no samples yet)", style="yellow"), title="Last Attempts")
    progress = Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.1f}%"), TimeRemainingColumn())
    task = progress.add_task("Cracking", total=stats.total_passwords, completed=stats.attempts)

    return Group(header, info, stats_table, system, progress, sample), progress, task

def load_wordlist(stats, q):
    try:
        with open(WORDLIST_FILE, 'rb') as f:
            lines = f.readlines()
            stats.total_passwords = len(lines)
            for i, line in enumerate(lines): q.put((i, line.strip()))
    except Exception as e:
        console.print(f"[red]❌ Error loading wordlist:[/red] {e}"); sys.exit(1)

def worker(stats, q, htype, target_hash):
    nhash = target_hash.replace(b"$2y$", b"$2b$") if htype == "bcrypt" else target_hash
    while not q.empty() and not stats.found and not stop_flag:
        try:
            i, pwd = q.get_nowait()
            pstr = pwd.decode('utf-8', 'ignore')
            match = False
            if htype == "bcrypt": match = bcrypt.checkpw(pwd, nhash)
            elif htype == "md5": match = hashlib.md5(pwd).hexdigest() == nhash.decode()
            elif htype == "sha1": match = hashlib.sha1(pwd).hexdigest() == nhash.decode()
            elif htype == "sha256": match = hashlib.sha256(pwd).hexdigest() == nhash.decode()
            if match: stats.found = pstr; save_resume(i); return
            stats.update(pwd)
        except queue.Empty: break

def save_resume(i): json.dump({"last_index": i}, open(RESUME_FILE, "w"))
def load_resume(): return json.load(open(RESUME_FILE)).get("last_index", 0) if os.path.exists(RESUME_FILE) else 0

def export_html_report(stats, hash_type):
    with open(REPORT_HTML, "w") as f:
        f.write(f"""
<html><head><title>CrackSmith Report</title></head>
<body><h2>CrackSmith Report</h2><ul>
<li><strong>Password:</strong> {stats.found}</li>
<li><strong>Attempts:</strong> {stats.attempts:,}</li>
<li><strong>Elapsed:</strong> {str(timedelta(seconds=int(stats.elapsed)))}</li>
<li><strong>Hash Type:</strong> {hash_type}</li>
<li><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
</ul></body></html>
""")

def send_discord_embed(stats, hash_type, settings):
    webhook = settings.get("discord_webhook")
    if not webhook: return
    embed = {
        "title": "🔐 CrackSmith Success",
        "description": "Password cracked successfully!",
        "color": 3066993,
        "fields": [
            {"name": "Password", "value": f"`{stats.found}`", "inline": False},
            {"name": "Attempts", "value": f"{stats.attempts:,}", "inline": True},
            {"name": "Elapsed", "value": str(timedelta(seconds=int(stats.elapsed))), "inline": True},
            {"name": "ETA", "value": stats.eta, "inline": True}
        ],
        "footer": {"text": "CrackSmith by Lovsan"},
        "timestamp": datetime.utcnow().isoformat()
    }
    if settings.get("discord_embed_logo"):
        embed["thumbnail"] = {"url": settings["discord_embed_logo"]}
    try:
        requests.post(webhook, json={"embeds": [embed]})
        console.print("[blue]💬 Discord embed sent![/blue]")
    except Exception as e:
        console.print(f"[red]⚠️ Discord webhook failed:[/red] {e}")

# === Menu and Execution ===
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--hash"); p.add_argument("--hashfile")
    p.add_argument("--wordlist", default=DEFAULT_WORDLIST)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--settings", default="settings.json")
    p.add_argument("--test", action="store_true")
    p.add_argument("--benchmark", action="store_true")
    return p.parse_args()

def main():
    args = parse_args()
    settings = json.load(open(args.settings)) if os.path.exists(args.settings) else {}
    global THREAD_COUNT, WORDLIST_FILE
    THREAD_COUNT = settings.get("threads", THREAD_COUNT)
    WORDLIST_FILE = args.wordlist

    if args.test:
        args.hash = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode()
        console.print(f"[cyan]Test hash for 'password123':[/cyan] {args.hash}")

    if args.benchmark:
        t0 = time.perf_counter()
        for _ in range(10000): bcrypt.hashpw(b"bench", bcrypt.gensalt(4))
        console.print(f"[green]Benchmark complete: {time.perf_counter() - t0:.2f}s for 10k hashes[/green]")
        return

    hashes = []
    if args.hashfile:
        with open(args.hashfile) as f: hashes = [line.strip().encode() for line in f if line.strip()]
    elif args.hash: hashes = [args.hash.encode()]
    else: hashes = [b"$2y$10$eupC0REYlNINHdZ7ntJvEu.8dZiU4y/favMCCeDAVQe9WPkxzPRVK"]

    for h in hashes:
        hash_type = detect_hash_type(h)
        stats = CrackerStats()
        q = queue.Queue()
        load_wordlist(stats, q)
        if args.resume:
            for _ in range(load_resume()): q.get_nowait()

        threads = [threading.Thread(target=worker, args=(stats, q, hash_type, h)) for _ in range(THREAD_COUNT)]
        [t.start() for t in threads]

        with Live(render_stats(stats, next(spinner), hash_type)[0], refresh_per_second=5, screen=True) as live:
            while any(t.is_alive() for t in threads):
                if stop_flag: break
                layout, progress, task = render_stats(stats, next(spinner), hash_type)
                progress.update(task, completed=stats.attempts)
                live.update(layout)
                time.sleep(0.5)
                if stats.found: break

        if stats.found:
            console.print(f"\n[bold green]✅ Password found: {stats.found}[/bold green]")
            export_html_report(stats, hash_type)
            send_discord_embed(stats, hash_type, settings)
            break
        elif stop_flag:
            console.print("[yellow]⏹️ Cracking stopped by user[/yellow]")
            break
        else:
            console.print(f"[red]❌ Not found in {stats.attempts:,} attempts[/red]")

if __name__ == "__main__":
    main()

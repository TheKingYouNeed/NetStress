#!/usr/bin/env python3
"""
NetStress EXTREME - Maximum Network Bandwidth Stress Tester
Uses async I/O, multiple CDN sources, and aggressive threading for maximum saturation.
https://github.com/TheKingYouNeed/NetStress
"""

import asyncio
import aiohttp
import signal
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# ============== CONFIGURATION ==============
NUM_ASYNC_WORKERS = 50      # Async connections per source
NUM_SOURCES = 5             # Number of different CDN sources
CHUNK_SIZE = 2 * 1024 * 1024  # 2MB chunks for faster throughput

# Multiple CDN sources for parallel downloads
DOWNLOAD_SOURCES = [
    "https://speed.cloudflare.com/__down?bytes=104857600",      # 100MB Cloudflare
    "https://speed.cloudflare.com/__down?bytes=209715200",      # 200MB Cloudflare
    "https://proof.ovh.net/files/100Mb.dat",                    # 100MB OVH
    "https://speedtest.tele2.net/100MB.zip",                    # 100MB Tele2
    "https://ash-speed.hetzner.com/100MB.bin",                  # 100MB Hetzner
]
# ===========================================

# Global control
keep_running = True
bytes_downloaded = 0
start_time = None

async def download_worker(session: aiohttp.ClientSession, url: str, worker_id: int):
    """Async worker that continuously downloads from a URL."""
    global keep_running, bytes_downloaded
    
    while keep_running:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                    if not keep_running:
                        break
                    bytes_downloaded += len(chunk)
        except asyncio.CancelledError:
            break
        except Exception:
            await asyncio.sleep(0.1)


async def run_source(url: str, num_workers: int):
    """Run multiple async workers for a single source."""
    connector = aiohttp.TCPConnector(limit=0, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(num_workers):
            task = asyncio.create_task(download_worker(session, url, i))
            tasks.append(task)
        
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                task.cancel()


def run_source_sync(url: str, num_workers: int):
    """Synchronous wrapper to run async source in a thread."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_source(url, num_workers))
    except Exception:
        pass


def format_speed(bytes_per_sec: float) -> str:
    """Format bytes/sec to human readable."""
    if bytes_per_sec >= 1_000_000_000:
        return f"{bytes_per_sec / 1_000_000_000:.2f} Gbps"
    elif bytes_per_sec >= 1_000_000:
        return f"{bytes_per_sec / 1_000_000:.2f} Mbps"
    elif bytes_per_sec >= 1_000:
        return f"{bytes_per_sec / 1_000:.2f} Kbps"
    else:
        return f"{bytes_per_sec:.2f} bps"


def signal_handler(sig, frame):
    """Handle Ctrl+C for clean shutdown."""
    global keep_running
    print("\n\033[1;91m[!] STOP SIGNAL RECEIVED. SHUTTING DOWN ALL ENGINES...\033[0m")
    keep_running = False
    time.sleep(1)
    print("\033[1;92m[+] All engines stopped. Goodbye!\033[0m")
    sys.exit(0)


def print_banner():
    """Print the startup banner."""
    total_connections = NUM_ASYNC_WORKERS * len(DOWNLOAD_SOURCES)
    print("\033[1;91m" + "=" * 70)
    print("   ⚡ NETSTRESS EXTREME - Maximum Bandwidth Saturation ⚡")
    print("=" * 70)
    print(f"\033[1;93m   CDN SOURCES: {len(DOWNLOAD_SOURCES)}")
    print(f"   ASYNC WORKERS PER SOURCE: {NUM_ASYNC_WORKERS}")
    print(f"   TOTAL PARALLEL CONNECTIONS: {total_connections}")
    print(f"   CHUNK SIZE: {CHUNK_SIZE // 1024 // 1024}MB")
    print("   DISK USAGE: 0 BYTES")
    print("   PRESS CTRL+C TO STOP")
    print("\033[1;91m" + "=" * 70 + "\033[0m\n")


def monitor_speed():
    """Monitor and display current download speed."""
    global bytes_downloaded, start_time, keep_running
    
    last_bytes = 0
    while keep_running:
        time.sleep(1)
        current_bytes = bytes_downloaded
        speed = (current_bytes - last_bytes) * 8  # Convert to bits
        last_bytes = current_bytes
        
        elapsed = time.time() - start_time
        total_downloaded = bytes_downloaded / (1024 * 1024 * 1024)  # GB
        
        print(f"\r\033[1;96m[LIVE] Speed: {format_speed(speed):>15} | "
              f"Downloaded: {total_downloaded:>7.2f} GB | "
              f"Time: {int(elapsed):>4}s\033[0m", end="", flush=True)


def main():
    """Main entry point."""
    global start_time, keep_running
    
    # Register Ctrl+C handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print_banner()
    print("\033[1;94m[*] Initializing extreme saturation engines...\033[0m")
    
    start_time = time.time()
    
    # Start speed monitor in background
    with ThreadPoolExecutor(max_workers=len(DOWNLOAD_SOURCES) + 1) as executor:
        # Start monitoring thread
        executor.submit(monitor_speed)
        
        # Start one thread per CDN source, each running async workers
        for url in DOWNLOAD_SOURCES:
            executor.submit(run_source_sync, url, NUM_ASYNC_WORKERS)
        
        print(f"\033[1;92m[+] {len(DOWNLOAD_SOURCES) * NUM_ASYNC_WORKERS} engines launched! Network MAXIMALLY saturated!\033[0m\n")
        
        try:
            while keep_running:
                time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(None, None)


if __name__ == "__main__":
    # Check for aiohttp
    try:
        import aiohttp
    except ImportError:
        print("\033[1;93m[*] Installing required dependency: aiohttp...\033[0m")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
        import aiohttp
    
    main()

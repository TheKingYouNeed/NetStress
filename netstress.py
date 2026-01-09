#!/usr/bin/env python3
"""
NetStress - High-Performance Network Bandwidth Stress Tester
A lightweight tool to saturate network bandwidth for testing purposes.
https://github.com/TheKingYouNeed/NetStress
"""

import time
import requests
import signal
import sys
from concurrent.futures import ThreadPoolExecutor

# ============== CONFIGURATION ==============
# Using 100MB chunks of data from Cloudflare's global CDN
TEST_FILE_URL = "https://speed.cloudflare.com/__down?bytes=104857600" 
NUM_THREADS = 10  # Number of parallel download streams
# ===========================================

# Global flag for clean shutdown
keep_running = True

def download_worker(thread_id: int) -> None:
    """
    Worker function that continuously downloads data to memory.
    Does not write to disk - all data is discarded after download.
    """
    global keep_running
    
    while keep_running:
        try:
            # Stream the request directly to memory
            response = requests.get(TEST_FILE_URL, stream=True, timeout=10)
            
            # Consume data as fast as the network allows
            for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                if not keep_running:
                    break
                # Data is discarded (sent to /dev/null equivalent)
                pass
            
        except requests.exceptions.RequestException:
            # Connection issues are expected during heavy saturation
            pass
        except Exception:
            pass 
        
        # Brief pause between downloads
        time.sleep(0.1)


def signal_handler(sig, frame) -> None:
    """Handle Ctrl+C for clean shutdown."""
    global keep_running
    print("\n\033[1;91m[!] STOP SIGNAL RECEIVED. CLEANING UP...\033[0m")
    keep_running = False
    print("\033[1;92m[+] Network stress test stopped. Zero disk space used. Goodbye!\033[0m")
    sys.exit(0)


def print_banner() -> None:
    """Print the startup banner."""
    print("\033[1;91m" + "=" * 60)
    print("   🌐 NETSTRESS - Network Bandwidth Stress Tester")
    print("=" * 60)
    print(f"\033[1;93m   PARALLEL STREAMS: {NUM_THREADS}")
    print("   DISK USAGE: 0 BYTES (Downloads to memory only)")
    print("   PRESS CTRL+C TO STOP INSTANTLY")
    print("\033[1;91m" + "=" * 60 + "\033[0m\n")


def main() -> None:
    """Main entry point."""
    # Register Ctrl+C handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print_banner()
    print("\033[1;94m[*] Starting download engines...\033[0m")
    
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        try:
            # Launch all download workers
            for i in range(NUM_THREADS):
                executor.submit(download_worker, i)
            
            print(f"\033[1;92m[+] All {NUM_THREADS} engines running. Network saturated!\033[0m\n")
            
            # Keep main thread alive
            while keep_running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            signal_handler(None, None)


if __name__ == "__main__":
    main()

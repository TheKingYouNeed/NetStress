# 🌐 NetStress - High-Performance Network Bandwidth Stress Tester

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/disk%20usage-0%20bytes-brightgreen.svg" alt="Zero Disk">
</p>

A lightweight, cross-platform Python tool for **stress testing network bandwidth** and measuring maximum throughput. Perfect for:

- 🔧 **Network Engineers**: Test QoS (Quality of Service) configurations
- 🏠 **Home Users**: Find out your real-world maximum download speed
- 🛡️ **Sysadmins**: Validate bandwidth limits and traffic shaping rules
- 📡 **ISP Testing**: Verify you're getting the speed you're paying for

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚀 **Multi-Threaded** | 10 parallel download streams for maximum saturation |
| 💾 **Zero Disk Usage** | Downloads directly to memory, no temp files created |
| ⚡ **Instant Stop** | Clean shutdown with `Ctrl+C` - no orphan processes |
| 🌍 **Global CDN** | Uses Cloudflare's edge network for consistent speeds worldwide |
| 🪶 **Lightweight** | Single file, minimal dependencies (`requests` only) |

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/TheKingYouNeed/NetStress.git
cd NetStress

# Install dependencies
pip install requests
```

### Usage

```bash
# Standard version (10 threads)
python netstress.py

# EXTREME version (250 async connections, 5 CDN sources)
python netstress_extreme.py

# Press Ctrl+C to stop at any time
```

## 🔥 EXTREME Version

The `netstress_extreme.py` offers maximum bandwidth saturation:

| Feature | Standard | EXTREME |
|---------|----------|---------|
| Connections | 10 | 250 |
| CDN Sources | 1 | 5 |
| Technology | Threading | Async I/O (aiohttp) |
| Live Speed Monitor | ❌ | ✅ |
| Chunk Size | 1MB | 2MB |

**Requirements for EXTREME:** `pip install aiohttp`

### One-Click Stop (Windows)
Double-click `STOP_STRESS_TEST.bat` to instantly terminate all running tests.

## 📊 Example Output

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   PRO BANDWIDTH SATURATOR (ZERO-DISK EDITION)   
   PARALLEL STREAMS: 10
   DISK USAGE: 0 BYTES (Downloads to memory only)
   PRESS CTRL+C TO STOP INSTANTLY
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

## ⚙️ Configuration

Edit the constants at the top of `netstress.py`:

```python
NUM_THREADS = 10  # Increase for more aggressive testing
TEST_FILE_URL = "https://speed.cloudflare.com/__down?bytes=104857600"  # 100MB chunks
```

## 🛡️ Responsible Use

This tool is intended for **testing your own network infrastructure**. Please use responsibly:

- ✅ Test your home/office network capacity
- ✅ Validate ISP speed claims
- ✅ Test router QoS settings
- ✅ Benchmark network equipment
- ❌ Do NOT use on networks you don't own/administer

## 📋 Requirements

- Python 3.8+
- `requests` library

## 📄 License

MIT License - feel free to use, modify, and distribute.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests
- Star ⭐ this repo if you find it useful!

---

<p align="center">
  Made with ❤️ for network engineers everywhere
</p>

<h1 align="center">🐀 RAT Vulnerabilities 🐀</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge" />
  <a href="https://t.me/swezy" target="_blank"><img src="https://img.shields.io/badge/Telegram-@Swezy-blue?style=for-the-badge&logo=telegram" /></a>
</p>

---

## 🚩 Project overview

**RAT Vulnerabilities** is a curated collection of *exploit examples* and *proofs‑of‑concept (PoCs)* inspired by vulnerabilities observed in Remote Administration Tools (RATs).  
This repository is intended for **educational** use only — specifically reverse‑engineering, vulnerability research, defensive testing, and exploit‑development learning in controlled environments.

> ⚠️ This repository **does not** promote or support malicious activity. Use responsibly and legally.

---

## ⭐ Supported RATs

| RAT | Directory |
|--------------|--------------|
| **XWorm**    | https://github.com/SwezyDev/RAT-Vulnerabilities/tree/main/XWorm |
| **AsyncRAT** | Soon |

---

## 📚 What you'll find here

- Carefully documented PoCs and exploit *examples* (sanitized and annotated).  
- Static analysis notes and reversing tips for researchers.  
- Reports and writeups describing observed vulnerability patterns, common pitfalls, and mitigations.

---

## 🛡️ Safety & Responsible Use

This project is explicitly for **legitimate security research**:

- Do **not** use contents of this repository to attack systems, exfiltrate data, or harm others.
- Do **not** run the Server (the RAT you want to try it on) on your personal workstation use isolated, disposable environments (e.g., VMs, sandboxes with snapshots) instead.

---

## 🧭 How to use this repo (recommended workflow)

1. **Clone** the repository for local inspection: examine PoC code, read writeups, and study the analysis notes.
2. Use the scripts on your **Own** insulated, disposable environments (e.g., VMs, sandboxes with snapshots) to see how it would look in a real case scenario.

> Suggested tools (for defenders/researchers): Process Hacker, Wireshark, DnSpy, DotPeek

---

## 📝 Repository structure 

```/
├─ XWorm/ # XWorm specific PoCs and writeups
│ ├─ create_text.py # Create a text on attacker's machine
│ ├─ flood_errors.py # Flood attacker's server with errors
│ ├─ flood_plugin.py # Flood attacker's server with plugins
│ ├─ flood_user.py # Flood attacker's server with users
│ ├─ information_spoofing.py # Send the attacker fake Information
│ ├─ live_chat.py # Talk with the attacker live
│ ├─ microphone_spoofing.py # Play an audio on attacker's machine
│ ├─ monitor_spoofing.py # Show a custom Picture/Video/Gif on attacker's machine
│ ├─ rce_exploit.py # Run remote code execution on attacker's machine
│ ├─ sniffer.py # Sniff request from the attacker's server and decrypt the Payload
│ └─ webcam_spoofing.py # Show a custom Picture/Video/Gif on attacker's machine
├─ AsyncRAT/ # coming soon
├─ LICENSE # License file
└─ README.md # Read me file
```

---

## 🧩 Contributing

Contributions are welcome from responsible researchers. Please follow these rules:

- Submit only **sanitized** and **working** PoCs. Do **not** upload malware or not working scripts.
- Include a clear writeup: summary, affected software/version (if known), analysis steps, and recommended mitigations.

---

## ⚖️ License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 🙌 Credits & contact

- Maintainer: [@SwezyDev](https://github.com/SwezyDev) — reach out via Telegram: [@Swezy](https://t.me/swezy)  
- Inspiration: public security research and community writeups.

---

## 📣 Final note

If you use or share findings from this repository, always prioritize ethics, legality, and minimizing harm. This collection aims to help defenders and researchers better understand RAT threats — not to enable abuse.
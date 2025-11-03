<h1 align="center">🐀 RAT Vulnerabilities 🐀</h1>

<p align="center">
  <a href="https://www.python.org" target="_blank"><img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python" /></a>
  <a href="https://t.me/swezy" target="_blank"><img src="https://img.shields.io/badge/Telegram-@Swezy-blue?style=for-the-badge&logo=telegram" /></a>
  <br>
  <code>Leave a ⭐ if you like this Repository</code>
</p>

---

## 🚩 Project overview

**RAT Vulnerabilities** is a curated collection of *exploit examples* and *proofs‑of‑concept (PoCs)* inspired by vulnerabilities observed in Remote Administration Tools (RATs).  
This repository is intended for **educational** use only — specifically reverse‑engineering, vulnerability research, defensive testing, and exploit‑development learning in controlled environments.

> [!CAUTION]
> This repository **does not** promote or support malicious activity. Use responsibly and legally.
> 
> **IMPORTANT — EDUCATIONAL / RESEARCH ONLY**
>
> This repository contains analysis, annotated writeups, and *sanitized* proofs-of-concept related to vulnerabilities historically observed in Remote Administration Tools (RATs).
>
> **This repository is strictly for legitimate security research, defensive testing, and education.** Do **NOT** use any material here to attack systems, exfiltrate data, or otherwise cause harm.
>
> If you believe content here violates GitHub policies, or if GitHub has restricted access to this repo, please contact the maintainer so we can address the concern immediately.

---

## ⭐ Supported RATs

<div align="center">

| RAT | Directory |
|--------------|--------------|
| **XWorm**    | https://github.com/SwezyDev/RAT-Vulnerabilities/tree/main/XWorm |

</div>

<p align="center">
  <sub>Do you want me to add more? Contact me on Telegram</sub>
</p>

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
├─ .github/ ➔ Contains GitHub issue templates
│ └─ ISSUE_TEMPLATE/ ➔ GitHub issue templates
│   ├─ bug_report.md ➔ For reporting bugs
│   └─ feature_request.md ➔ For suggesting new features
├─ XWorm/ ➔ XWorm specific PoCs and writeups
│ ├─ README.md ➔ Show a detailed version of this and description of the Scripts
│ ├─ auto_exploiter.py ➔ Exploit (RCE) mutiple C2s fast with your own Payload
│ ├─ create_text.py ➔ Create a text on attacker's machine
│ ├─ decrypt_payload.py ➔ Get all Information about the Client
│ ├─ flood_errors.py ➔ Flood attacker's server with errors
│ ├─ flood_plugin.py ➔ Flood attacker's server with plugins
│ ├─ flood_user.py ➔ Flood attacker's server with users
│ ├─ information_spoofing.py ➔ Send the attacker fake Information
│ ├─ live_chat.py ➔ Talk with the attacker live (sender only)
│ ├─ live_chat_v2.py ➔ Talk with the attacker live (send and receiver)
│ ├─ microphone_spoofing.py ➔ Play an audio on attacker's machine
│ ├─ monitor_spoofing.py ➔ Show a custom Picture/Video/Gif on attacker's machine
│ ├─ rce_exploit.py ➔ Run remote code execution on attacker's machine
│ ├─ reverse_shell.py ➔ Launch a remote shell on attacker's machine
│ ├─ sniffer.py ➔ Sniff request from the attacker's server and decrypt the Payload
│ └─ webcam_spoofing.py ➔ Show a custom Picture/Video/Gif on attacker's machine
├─ .gitignore ➔ Lists files and directories Git should ignore
├─ LICENSE ➔ License file
└─ README.md ➔ Read me file
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

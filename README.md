# 🧠 RetrieverLabs Hunt Generator

A simple web tool that turns raw security indicators (IOCs) into structured threat hunting queries.

---

## 🌐 Live Tool

👉 [https://retrieverlabs.streamlit.app](https://retrieverlabs.streamlit.app/)

Use it directly in your browser — no install needed.

---

## 🔍 What it does

Paste indicators like IPs, domains, hashes, or file paths and the tool will:

- Identify what type of indicator it is
- Route it to a hunting category (network, endpoint, authentication)
- Generate Splunk search queries

---

## 🧪 Example input
8.8.8.8
malware-test-domain.xyz
a3f5c2d1b4e6f7890c123456789abcdef123456789abcdef123456789abcdef
admin@company.com
C:\Users\Admin\AppData\malware.exe


---

## ⚡ Output

For each indicator you get:

- Type (IP, domain, hash, etc.)
- Investigation category
- Splunk query

---

## 🎯 Purpose

To speed up threat hunting by removing manual query building and standardizing investigations.

---

## 🔮 Future improvements

- Threat intel enrichment
- IOC scoring
- Save hunt history
- Copy-to-Splunk button

---

## ⚠️ Disclaimer

For defensive security and authorized use only.

---

## 🏷️ Built by

RetrieverLabs

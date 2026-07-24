import streamlit as st
import re

def defang(text):
    return (
        text
        .replace("http://", "hxxp://")
        .replace("https://", "hxxps://")
        .replace(".", "[.]")
    )

st.set_page_config(page_title="RTL Hunt Generator", layout="wide")

st.title("🛡️ RetrieverLabs Hunt Generator")

# -----------------------------
# IOC CLASSIFICATION
# -----------------------------
def classify(ioc):
    ip = r"^\d{1,3}(\.\d{1,3}){3}$"
    cidr = r"^\d{1,3}(\.\d{1,3}){3}\/\d{1,2}$"
    hash_ = r"^[a-fA-F0-9]{32,64}$"
    email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    url = r"^https?://"
    domain = r"([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"
    filepath = r"(C:\\|/).+"

    if re.match(ip, ioc):
        return "ip"
    if re.match(cidr, ioc):
        return "cidr"
    if re.match(hash_, ioc):
        return "hash"
    if re.match(email, ioc):
        return "email"
    if re.match(url, ioc):
        return "url"
    if re.match(filepath, ioc):
        return "filepath"
    if re.match(domain, ioc):
        return "domain"
    return "unknown"


# -----------------------------
# ROUTING LOGIC
# -----------------------------
def route(ioc_type):
    if ioc_type in ["ip", "domain", "cidr", "url"]:
        return "network"
    if ioc_type in ["hash", "filepath"]:
        return "endpoint"
    if ioc_type == "email":
        return "authentication"
    return "unknown"


# -----------------------------
# SPL GENERATOR (SIMPLIFIED SOC LOGIC)
# -----------------------------
def build_spl(ioc, ioc_type, route_type):

    if route_type == "network":
        return f'''
# NETWORK HUNT
index=web
| search "{ioc}"
| stats count by src_ip dest_ip http_host
'''

    if route_type == "endpoint":
        return f'''
# ENDPOINT HUNT (CrowdStrike)
index=crowdstrike
| search "{ioc}"
| stats count by host file_name process_name
'''

    if route_type == "authentication":
        return f'''
# AUTH HUNT
index=auth
| search user="{ioc}"
| stats count by user src_ip action
'''

    return "# No mapping available"


# -----------------------------
# UI
# -----------------------------
text = st.text_area("Enter IOCs (one per line)")

items = [x.strip() for x in text.splitlines() if x.strip()]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total IOCs", len(items))

mapped = 0
network = 0
endpoint = 0

st.divider()

for ioc in items:
    t = classify(ioc)
    r = route(t)

    if t != "unknown":
        mapped += 1
    if r == "network":
        network += 1
    if r == "endpoint":
        endpoint += 1

    st.subheader(defang(ioc))

    st.write(f"Type: **{t}** | Route: **{r}**")
    st.code(build_spl(ioc, t, r), language="sql")

with col2:
    st.metric("Mapped IOCs", mapped)

with col3:
    st.metric("Endpoint vs Network Split", f"{endpoint} / {network}")


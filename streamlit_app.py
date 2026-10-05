import streamlit as st
import requests

st.set_page_config(page_title="AISYS RFID Library Dashboard", layout="wide")

API_BASE = "http://localhost:8080"

st.title("AISYS RFID Library Management System")
st.caption("Operational Dashboard & Hardware Simulator")

# Dashboard Analytics
st.subheader("System Overview")
try:
    res = requests.get(f"{API_BASE}/api/v1/reports/dashboard").json()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Catalog Items", res["total_catalog_items"])
    col2.metric("RFID Tagged Items", res["rfid_tagged_items"])
    col3.metric("Active Loans", res["active_circulation_loans"])
    col4.metric("Security Gate Alarms", res["security_gate_alarms"], delta_color="inverse")
except Exception:
    st.error("Backend API Server is offline. Run 'uvicorn main:app' first.")

st.divider()

# Tabs for Operations
tab1, tab2, tab3 = st.tabs(["OPAC Search", "Handheld Inventory Scan", "🚨 Gate Alarm Simulator"])

with tab1:
    st.subheader("Catalog Search")
    query = st.text_input("Enter title, author, or accession number:")
    if query:
        search_res = requests.get(f"{API_BASE}/api/v1/catalog/search", params={"q": query}).json()
        st.write(f"Found **{search_res['count']}** item(s):")
        st.dataframe(search_res["items"])

with tab2:
    st.subheader("Handheld RFID Shelf Inventory")
    scanned = st.text_area("Scanned EPCs (comma separated)", "EPC-8888, EPC-UNKNOWN")
    shelf = st.text_input("Expected Shelf Location", "A1")
    if st.button("Run Stock Verification"):
        epc_list = [e.strip() for e in scanned.split(",") if e.strip()]
        res = requests.post(f"{API_BASE}/api/v1/inventory/handheld-scan", json={"scanned_epcs": epc_list, "expected_location": shelf}).json()
        if res["audio_alert"]:
            st.warning("AUDIBLE ALERT: Misplaced or missing items detected!")
        else:
            st.success("Shelf verified cleanly.")
        st.json(res)

with tab3:
    st.subheader("Security Gate Detector")
    epc = st.text_input("Passed EPC Tag", "EPC-8888")
    gate_id = st.text_input("Gate ID", "GATE-01")
    if st.button("Trigger Gate Sensor"):
        res = requests.post(f"{API_BASE}/api/v1/gate/detect", json={"rfid_epc": epc, "device_id": gate_id}).json()
        if res["gate_status"] == "ALARM_TRIGGERED":
            st.error(f"ALARM! Unauthorized removal of accession {res['accession_number']}. Snapshot: {res['cctv_captured']}")
        else:
            st.success("Clear passage.")
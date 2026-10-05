import pytest
from fastapi.testclient import TestClient
from main import app, Base, engine, SessionLocal, DBItem, DBMember

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    item1 = DBItem(accession_number="ACC-1001", title="Database Systems", author="Date, C.J.", is_reference=False)
    item2 = DBItem(accession_number="ACC-1002", title="Rare Manuscripts Vol I", author="Anonymous", is_reference=True)
    member1 = DBMember(card_number="CARD-001", rfid_uid="UID-999", name="John Doe", email="john@example.com", is_blocked=False, fine_balance=0.0)
    member_blocked = DBMember(card_number="CARD-002", name="Blocked User", email="blocked@example.com", is_blocked=True, fine_balance=0.0)
    member_fined = DBMember(card_number="CARD-003", name="Fined User", email="fined@example.com", is_blocked=False, fine_balance=150.0)

    db.add_all([item1, item2, member1, member_blocked, member_fined])
    db.commit()
    db.close()

def test_ac02_tag_binding():
    res = client.post("/api/v1/tagging/bind", json={"accession_number": "ACC-1001", "rfid_epc": "EPC-8888"})
    assert res.status_code == 200
    assert res.json()["item"]["rfid_epc"] == "EPC-8888"

def test_ac03_and_ac04_checkout_checkin_and_blocks():
    client.post("/api/v1/tagging/bind", json={"accession_number": "ACC-1001", "rfid_epc": "EPC-8888"})
    
    # Checkout
    res = client.post("/api/v1/circulation/checkout", json={"member_card": "CARD-001", "rfid_epc": "EPC-8888"})
    assert res.status_code == 200

    # Due Date Enquiry
    res_due = client.get("/api/v1/circulation/due-date-enquiry", params={"rfid_epc": "EPC-8888"})
    assert res_due.status_code == 200
    assert res_due.json()["status"] == "ISSUED"

    # Checkin
    res_in = client.post("/api/v1/circulation/checkin", json={"rfid_epc": "EPC-8888"})
    assert res_in.status_code == 200

    # Blocked User
    res_blocked = client.post("/api/v1/circulation/checkout", json={"member_card": "CARD-002", "rfid_epc": "EPC-8888"})
    assert res_blocked.status_code == 403

def test_catalog_search():
    res = client.get("/api/v1/catalog/search", params={"q": "Database"})
    assert res.status_code == 200
    assert res.json()["count"] == 1

def test_ac05_inventory_scan():
    client.post("/api/v1/tagging/bind", json={"accession_number": "ACC-1001", "rfid_epc": "EPC-8888"})
    res = client.post("/api/v1/inventory/handheld-scan", json={"scanned_epcs": ["EPC-8888", "EPC-UNKNOWN"], "expected_location": "A1"})
    assert res.status_code == 200

def test_ac06_gate_unauthorized_alarm():
    client.post("/api/v1/tagging/bind", json={"accession_number": "ACC-1001", "rfid_epc": "EPC-8888"})
    res = client.post("/api/v1/gate/detect", json={"rfid_epc": "EPC-8888", "device_id": "GATE-MAIN"})
    assert res.status_code == 200

def test_ac07_smart_card_login():
    db = SessionLocal()
    m = db.query(DBMember).filter(DBMember.card_number == "CARD-001").first()
    m.role = "STAFF"
    db.commit()
    db.close()

    res_ok = client.post("/api/v1/auth/smartcard-login", json={"card_uid": "UID-999"})
    assert res_ok.status_code == 200
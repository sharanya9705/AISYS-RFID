import os
import uuid
import datetime
import logging
import shutil
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query, Body
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Float, ForeignKey, Text, or_
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AISYS_ILMS")

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aisys_library.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Models ---
class DBItem(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    accession_number = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String)
    is_reference = Column(Boolean, default=False)
    rfid_epc = Column(String, unique=True, nullable=True)
    status = Column(String, default="AVAILABLE")
    shelf_location = Column(String, default="A1")

class DBMember(Base):
    __tablename__ = "members"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    card_number = Column(String, unique=True, index=True)
    rfid_uid = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    is_blocked = Column(Boolean, default=False)
    fine_balance = Column(Float, default=0.0)
    role = Column(String, default="PATRON")

class DBCirculation(Base):
    __tablename__ = "circulations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String, ForeignKey("items.id"))
    member_id = Column(String, ForeignKey("members.id"))
    issue_date = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    due_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)
    status = Column(String, default="ISSUED")

class DBGateEvent(Base):
    __tablename__ = "gate_events"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    epc = Column(String)
    accession_number = Column(String, nullable=True)
    is_authorized = Column(Boolean)
    snapshot_path = Column(String, nullable=True)
    alarm_triggered = Column(Boolean, default=False)

class DBAuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    actor = Column(String)
    action = Column(String)
    details = Column(Text)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================================
# 1. INITIALIZE FASTAPI APP (MUST COME BEFORE ANY ROUTE DECORATORS)
# =====================================================================
app = FastAPI(title="AISYS RFID Library Management System", version="1.0.0")

CONFIG_MAX_FINE_LIMIT = 50.0

# =====================================================================
# 2. WEB UI DASHBOARD ROUTE
# =====================================================================
@app.get("/", response_class=HTMLResponse)
def render_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AISYS RFID Library Management System</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 min-h-screen font-sans">
        <!-- Header -->
        <nav class="bg-slate-800 border-b border-slate-700 px-6 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <span class="bg-indigo-600 text-white font-bold text-xl px-3 py-1 rounded">AISYS</span>
                <h1 class="text-xl font-semibold">RFID Library Management System</h1>
            </div>
            <span class="bg-emerald-500/10 text-emerald-400 text-xs font-semibold px-3 py-1 rounded-full border border-emerald-500/20">
                System Status: Online (Air-Gapped)
            </span>
        </nav>

        <main class="p-6 max-w-7xl mx-auto space-y-6">
            <!-- Operations Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Catalog Search -->
                <div class="bg-slate-800 border border-slate-700 rounded-xl p-5 shadow-lg">
                    <h2 class="text-lg font-semibold mb-4 text-indigo-400 flex items-center gap-2">
                        OPAC Catalog Search
                    </h2>
                    <input type="text" name="q" placeholder="Search by title, author, ISBN..." 
                           class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-indigo-500 mb-4"
                           hx-get="/api/v1/catalog/search" hx-trigger="keyup changed delay:300ms" hx-target="#search-results">
                    <div id="search-results" class="text-sm text-slate-400">Type to search items...</div>
                </div>

                <!-- RFID Gate Simulator -->
                <div class="bg-slate-800 border border-slate-700 rounded-xl p-5 shadow-lg">
                    <h2 class="text-lg font-semibold mb-4 text-rose-400 flex items-center gap-2">
                        Security Gate Event Simulator
                    </h2>
                    <form onsubmit="event.preventDefault(); triggerGate();" class="space-y-4">
                        <div>
                            <label class="block text-xs font-medium text-slate-400 mb-1">Scanned RFID EPC</label>
                            <input type="text" id="rfid_epc" name="rfid_epc" value="EPC-8888" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200">
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-slate-400 mb-1">Gate Device ID</label>
                            <input type="text" id="device_id" name="device_id" value="GATE-MAIN-01" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200">
                        </div>
                        <button type="submit" class="w-full bg-rose-600 hover:bg-rose-500 text-white font-medium py-2 rounded-lg transition">
                            Simulate Gate Pass-Through
                        </button>
                    </form>
                    <div id="gate-alert" class="mt-4"></div>
                </div>
            </div>
        </main>

        <script>
            function triggerGate() {
                const epc = document.getElementById('rfid_epc').value;
                const dev = document.getElementById('device_id').value;
                fetch('/api/v1/gate/detect', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({rfid_epc: epc, device_id: dev})
                })
                .then(r => r.json())
                .then(data => {
                    const el = document.getElementById('gate-alert');
                    if (data.gate_status === 'ALARM_TRIGGERED') {
                        el.innerHTML = `<div class="bg-rose-500/10 border border-rose-500/30 text-rose-400 p-3 rounded-lg text-sm font-semibold animate-pulse">
                            UNAUTHORIZED REMOVAL DETECTED!<br>
                            Accession: ${data.accession_number}<br>
                            CCTV Captured: ${data.cctv_captured}
                        </div>`;
                    } else {
                        el.innerHTML = `<div class="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 p-3 rounded-lg text-sm">
                            PASS CLEAR: Item legally checked out.
                        </div>`;
                    }
                });
            }
        </script>
    </body>
    </html>
    """

# =====================================================================
# 3. SYSTEM HEALTH & ADMIN ENDPOINTS
# =====================================================================
@app.get("/health")
def get_health_status():
    return {
        "status": "HEALTHY",
        "system_version": "1.0.0-offline",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "database": "CONNECTED"
    }

# =====================================================================
# 4. FR 02: CATALOG SEARCH & OPAC
# =====================================================================
@app.get("/api/v1/catalog/search")
def search_catalog(q: str = Query(..., description="Query title, author, ISBN, or accession"), db: Session = Depends(get_db)):
    results = db.query(DBItem).filter(
        or_(
            DBItem.title.ilike(f"%{q}%"),
            DBItem.author.ilike(f"%{q}%"),
            DBItem.isbn.ilike(f"%{q}%"),
            DBItem.accession_number.ilike(f"%{q}%")
        )
    ).all()
    return {"query": q, "count": len(results), "items": results}

# =====================================================================
# 5. FR 05 / AC 02: RFID TAG BINDING
# =====================================================================
class TagBindRequest(BaseModel):
    accession_number: str
    rfid_epc: str

@app.post("/api/v1/tagging/bind")
def bind_rfid_tag(req: TagBindRequest, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.accession_number == req.accession_number).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item record not found.")
    
    existing_epc = db.query(DBItem).filter(DBItem.rfid_epc == req.rfid_epc).first()
    if existing_epc and existing_epc.id != item.id:
        raise HTTPException(status_code=400, detail="RFID EPC is already mapped to another item.")

    item.rfid_epc = req.rfid_epc
    db.commit()
    db.refresh(item)
    return {"status": "SUCCESS", "message": "RFID tag bound successfully", "item": {"title": item.title, "accession_number": item.accession_number, "rfid_epc": item.rfid_epc}}

# =====================================================================
# 6. FR 04 & AC 03, AC 04: CIRCULATION ENGINE
# =====================================================================
class CheckoutRequest(BaseModel):
    member_card: str
    rfid_epc: str

class CheckinRequest(BaseModel):
    rfid_epc: str

@app.post("/api/v1/circulation/checkout")
def checkout_item(req: CheckoutRequest, db: Session = Depends(get_db)):
    member = db.query(DBMember).filter(DBMember.card_number == req.member_card).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member card not recognized.")

    if member.is_blocked:
        raise HTTPException(status_code=403, detail="Checkout Blocked: Member account is explicitly suspended.")
    if member.fine_balance > CONFIG_MAX_FINE_LIMIT:
        raise HTTPException(status_code=403, detail=f"Checkout Blocked: Outstanding fines exceed limit.")

    item = db.query(DBItem).filter(DBItem.rfid_epc == req.rfid_epc).first()
    if not item:
        raise HTTPException(status_code=404, detail="No physical item associated with this RFID EPC.")

    if item.is_reference:
        raise HTTPException(status_code=403, detail="Checkout Blocked: Item designated as Reference Only.")

    if item.status == "ISSUED":
        raise HTTPException(status_code=400, detail="Item is currently checked out to another patron.")

    item.status = "ISSUED"
    due_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=14)
    txn = DBCirculation(item_id=item.id, member_id=member.id, due_date=due_date)
    db.add(txn)
    
    audit = DBAuditLog(actor=member.card_number, action="CHECKOUT", details=f"Issued item {item.accession_number}")
    db.add(audit)

    db.commit()
    return {"status": "SUCCESS", "transaction_id": txn.id, "due_date": due_date.isoformat(), "item_title": item.title}

@app.post("/api/v1/circulation/checkin")
def checkin_item(req: CheckinRequest, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.rfid_epc == req.rfid_epc).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found for given RFID tag.")

    txn = db.query(DBCirculation).filter(DBCirculation.item_id == item.id, DBCirculation.status == "ISSUED").first()
    if not txn:
        raise HTTPException(status_code=400, detail="Item is not currently checked out.")

    item.status = "AVAILABLE"
    txn.status = "RETURNED"
    txn.return_date = datetime.datetime.now(datetime.timezone.utc)

    audit = DBAuditLog(actor="SYSTEM_CHECKIN", action="CHECKIN", details=f"Returned item {item.accession_number}")
    db.add(audit)

    db.commit()
    return {"status": "SUCCESS", "message": f"Item '{item.title}' successfully returned."}

@app.get("/api/v1/circulation/due-date-enquiry")
def due_date_enquiry(rfid_epc: str, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.rfid_epc == rfid_epc).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")

    txn = db.query(DBCirculation).filter(DBCirculation.item_id == item.id, DBCirculation.status == "ISSUED").first()
    if not txn:
        return {"rfid_epc": rfid_epc, "status": "AVAILABLE", "due_date": None}

    return {"rfid_epc": rfid_epc, "status": "ISSUED", "due_date": txn.due_date.isoformat()}

# =====================================================================
# 7. FR 03: NCIP / SIP2 ADAPTER MOCKS
# =====================================================================
@app.post("/api/v1/interop/sip2/checkout")
def sip2_checkout_adapter(raw_sip2_msg: str = Body(..., media_type="text/plain"), db: Session = Depends(get_db)):
    logger.info(f"[SIP2 ADAPTER] Processing incoming message: {raw_sip2_msg}")
    return {"sip2_response": f"121N{datetime.datetime.now().strftime('%Y%m%d    %H%M%S')}AO|AA|AB|AJ|"}

@app.post("/api/v1/interop/ncip/checkout")
def ncip_checkout_adapter(ncip_xml: str = Body(..., media_type="application/xml"), db: Session = Depends(get_db)):
    logger.info("[NCIP 2.0 ADAPTER] Received NCIP ItemCheckedOut Request XML.")
    return JSONResponse(content={"NCIPMessage": {"ItemCheckedOutResponse": {"ResponseHeader": {"Status": "Success"}}}})

# =====================================================================
# 8. FR 06 & AC 05: HANDHELD INVENTORY SCAN
# =====================================================================
class InventoryScanBatch(BaseModel):
    scanned_epcs: List[str]
    expected_location: str

@app.post("/api/v1/inventory/handheld-scan")
def process_handheld_scan(batch: InventoryScanBatch, db: Session = Depends(get_db)):
    found_items = db.query(DBItem).filter(DBItem.rfid_epc.in_(batch.scanned_epcs)).all()
    found_epcs = {item.rfid_epc for item in found_items}
    
    misplaced = []
    for item in found_items:
        if item.shelf_location != batch.expected_location:
            misplaced.append({"accession_number": item.accession_number, "current_shelf": item.shelf_location, "found_at": batch.expected_location})

    shelf_items = db.query(DBItem).filter(DBItem.shelf_location == batch.expected_location, DBItem.status == "AVAILABLE").all()
    missing = [item.accession_number for item in shelf_items if item.rfid_epc not in found_epcs]

    return {
        "status": "COMPLETED",
        "audio_alert": True if misplaced or missing else False,
        "visual_indicator": "WARNING" if misplaced or missing else "GREEN",
        "total_scanned": len(batch.scanned_epcs),
        "misplaced_items": misplaced,
        "missing_items": missing
    }

# =====================================================================
# 9. FR 07, FR 09 & AC 06: SECURITY GATE & NOTIFICATIONS
# =====================================================================
class GatePassEvent(BaseModel):
    rfid_epc: str
    device_id: str

@app.post("/api/v1/gate/detect")
def gate_event_trigger(event: GatePassEvent, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.rfid_epc == event.rfid_epc).first()
    
    accession = item.accession_number if item else "UNKNOWN"
    is_unauthorized = False

    if not item or item.status == "AVAILABLE":
        is_unauthorized = True

    snapshot_filename = f"/cctv_captures/gate_{event.device_id}_{int(datetime.datetime.now(datetime.timezone.utc).timestamp())}.jpg"
    
    gate_record = DBGateEvent(
        epc=event.rfid_epc,
        accession_number=accession,
        is_authorized=not is_unauthorized,
        snapshot_path=snapshot_filename,
        alarm_triggered=is_unauthorized
    )
    db.add(gate_record)
    db.commit()

    if is_unauthorized:
        background_tasks.add_task(dispatch_security_notifications, accession, event.device_id, snapshot_filename)

    return {
        "gate_status": "ALARM_TRIGGERED" if is_unauthorized else "CLEAR",
        "accession_number": accession,
        "cctv_captured": snapshot_filename
    }

def dispatch_security_notifications(accession: str, device: str, photo_path: str):
    logger.warning(f"[EMAIL ADAPTER] Security Alert sent for item {accession} at Gate {device}.")
    logger.warning(f"[SMS ADAPTER] Security SMS dispatched to duty librarian.")
    logger.warning(f"[PRINT ADAPTER] Incident ticket slip generated.")

# =====================================================================
# 10. FR 11 & AC 07: SMART CARD AUTHENTICATION
# =====================================================================
class SmartCardLogin(BaseModel):
    card_uid: str

@app.post("/api/v1/auth/smartcard-login")
def smartcard_login(cred: SmartCardLogin, db: Session = Depends(get_db)):
    member = db.query(DBMember).filter(DBMember.rfid_uid == cred.card_uid).first()
    if not member or member.role not in ["STAFF", "ADMIN"]:
        raise HTTPException(status_code=401, detail="Unauthorized smart card or insufficient access rights.")
    return {"status": "AUTHENTICATED", "user": member.name, "role": member.role, "token": f"mock-jwt-token-for-{member.id}"}

# =====================================================================
# 11. FR 08 & AC 08: DASHBOARD METRICS
# =====================================================================
@app.get("/api/v1/reports/dashboard")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    total_items = db.query(DBItem).count()
    tagged_items = db.query(DBItem).filter(DBItem.rfid_epc.isnot(None)).count()
    active_loans = db.query(DBCirculation).filter(DBCirculation.status == "ISSUED").count()
    unauthorized_gate_events = db.query(DBGateEvent).filter(DBGateEvent.is_authorized == False).count()
    
    return {
        "total_catalog_items": total_items,
        "rfid_tagged_items": tagged_items,
        "active_circulation_loans": active_loans,
        "security_gate_alarms": unauthorized_gate_events,
        "system_health": "OPTIMAL"
    }
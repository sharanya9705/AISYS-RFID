# User Guide

## 1. Purpose
This guide explains how to use the AISYS library prototype for common staff and operator tasks.

## 2. Main modules
### Catalog and item management
- create or review item records
- bind RFID EPC values to accession records
- review item status and locations

### Circulation workflow
- scan member card
- scan an RFID-tagged item
- validate fine limit and membership status
- complete checkout or checkin

### Inventory workflow
- enter scanned EPCs
- specify expected shelf location
- identify missing or misplaced items

### Gate monitoring
- simulate gate read events
- trigger unauthorized removal detection
- review alarm and CCTV snapshot path information

## 3. Basic staff workflow
### Tag binding
1. Open the application or backend API.
2. Provide accession number and RFID EPC.
3. Submit the bind request.
4. Verify the result shows the tag mapped to the correct item.

### Checkout
1. Enter member card number.
2. Scan or input RFID EPC.
3. System validates item status and member restrictions.
4. If valid, item is checked out and due date is returned.

### Checkin
1. Read the RFID EPC when returning the item.
2. Submit the return request.
3. Item is marked available and circulation record is updated.

### Inventory
1. Enter all scanned EPCs.
2. Provide expected shelf location.
3. Review missing and misplaced items.

## 4. Dashboard usage
The dashboard displays:
- total items in the catalog
- tagged items
- current loans
- security alarms

## 5. Best practice
- validate each tag before issuing an item
- confirm that the member is not blocked or over fine limit
- verify shelf locations before inventory confirmation
- keep audit logs for recovery and support

## 6. Known limitation
This is a prototype demonstration and not a replacement for a full production library system or vendor-supported RFID environment.

# backend/app/email_utils.py
import os
import smtplib
from email.mime.text import MIMEText
import imaplib
import email
from .crud import create_proposal_db
from .models import Vendor, RFP
from sqlmodel import Session, select
from .db import engine
import asyncio
from .ai import parse_vendor_email

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")

def send_rfp_email(to_email: str, subject: str, structured_rfp: dict):
    # Send simple text email with structured RFP JSON
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        body = "Please find RFP below:\n\n" + str(structured_rfp)
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        s.sendmail(SMTP_USER, [to_email], msg.as_string())
    print("Sent RFP to", to_email)

def poll_inbox_and_create_proposals():
    """
    Connects to IMAP inbox, looks for unseen messages, tries to map the sender to a vendor,
    parses body via AI, and creates a Proposal record that links to the latest RFP (simple heuristic).
    """
    try:
        conn = imaplib.IMAP4_SSL(IMAP_HOST)
        conn.login(IMAP_USER, IMAP_PASS)
        conn.select("INBOX")
        typ, msgnums = conn.search(None, '(UNSEEN)')
        if typ != 'OK':
            return
        for num in msgnums[0].split():
            typ, data = conn.fetch(num, '(RFC822)')
            if typ != 'OK':
                continue
            msg = email.message_from_bytes(data[0][1])
            from_addr = email.utils.parseaddr(msg.get("From"))[1]
            subject = msg.get("Subject")
            # get body text
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    cdisp = str(part.get('Content-Disposition'))
                    if ctype == 'text/plain' and 'attachment' not in cdisp:
                        body = part.get_payload(decode=True).decode(errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors='ignore')
            # find vendor by email
            with Session(engine) as session:
                vendors = session.exec(select(Vendor).where(Vendor.email == from_addr)).all()
                vendor = vendors[0] if vendors else None
                # simple mapping: link to most recent RFP
                last_rfp = session.exec(select(RFP).order_by(RFP.id.desc()).limit(1)).first()
            # parse via AI (sync call to async function)
            import asyncio
            parsed = asyncio.get_event_loop().run_until_complete(parse_vendor_email(body))
            # create proposal if vendor and rfp exist
            if vendor and last_rfp:
                create_proposal_db(vendor.id, last_rfp.id, body, parsed)
            else:
                # if vendor not found, could create a placeholder vendor
                print("Vendor not found for email:", from_addr)
            # mark seen
            conn.store(num, '+FLAGS', '\\Seen')
        conn.close()
        conn.logout()
    except Exception as e:
        print("Error polling IMAP:", e)


from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import ipaddress

app = Flask(__name__)

DATABASE = "firewall.db"


# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# CREATE DATABASE TABLES
def initialize_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_ip TEXT NOT NULL,
            port TEXT NOT NULL,
            protocol TEXT NOT NULL,
            action TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_ip TEXT,
            port INTEGER,
            protocol TEXT,
            action TEXT,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# FIREWALL RULE ENGINE
def evaluate_packet(source_ip, port, protocol):

    conn = get_db()

    rules = conn.execute(
        "SELECT * FROM rules ORDER BY id ASC"
    ).fetchall()

    decision = "BLOCK"
    reason = "Default deny: No matching rule"

    for rule in rules:

        ip_match = (
            rule["source_ip"] == "ANY"
            or rule["source_ip"] == source_ip
        )

        port_match = (
            rule["port"] == "ANY"
            or rule["port"] == str(port)
        )

        protocol_match = (
            rule["protocol"] == "ANY"
            or rule["protocol"] == protocol
        )

        if ip_match and port_match and protocol_match:

            decision = rule["action"]
            reason = f"Matched rule #{rule['id']}"
            break

    conn.execute("""
        INSERT INTO logs
        (source_ip, port, protocol, action, reason)
        VALUES (?, ?, ?, ?, ?)
    """, (source_ip, port, protocol, decision, reason))

    conn.commit()
    conn.close()

    return decision, reason


# DASHBOARD
@app.route("/")
def index():

    conn = get_db()

    rules = conn.execute(
        "SELECT * FROM rules ORDER BY id ASC"
    ).fetchall()

    logs = conn.execute(
        "SELECT * FROM logs ORDER BY id DESC LIMIT 20"
    ).fetchall()

    total_rules = conn.execute(
        "SELECT COUNT(*) FROM rules"
    ).fetchone()[0]

    total_logs = conn.execute(
        "SELECT COUNT(*) FROM logs"
    ).fetchone()[0]

    blocked = conn.execute(
        "SELECT COUNT(*) FROM logs WHERE action='BLOCK'"
    ).fetchone()[0]

    allowed = conn.execute(
        "SELECT COUNT(*) FROM logs WHERE action='ALLOW'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        rules=rules,
        logs=logs,
        total_rules=total_rules,
        total_logs=total_logs,
        blocked=blocked,
        allowed=allowed
    )


# ADD FIREWALL RULE
@app.route("/add_rule", methods=["POST"])
def add_rule():

    source_ip = request.form["source_ip"].strip()
    port = request.form["port"].strip()
    protocol = request.form["protocol"]
    action = request.form["action"]

    try:
        if source_ip.upper() != "ANY":
            ipaddress.ip_address(source_ip)

        if port.upper() != "ANY":
            if not port.isdigit() or not 1 <= int(port) <= 65535:
                raise ValueError()

        if protocol not in ["TCP", "UDP", "ANY"]:
            raise ValueError()

        if action not in ["ALLOW", "BLOCK"]:
            raise ValueError()

    except ValueError:
        return "Invalid firewall rule input", 400

    conn = get_db()

    conn.execute("""
        INSERT INTO rules (source_ip, port, protocol, action)
        VALUES (?, ?, ?, ?)
    """, (source_ip.upper() if source_ip.upper() == "ANY" else source_ip,
          port.upper() if port.upper() == "ANY" else port,
          protocol, action))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# DELETE RULE
@app.route("/delete_rule/<int:rule_id>", methods=["POST"])
def delete_rule(rule_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM rules WHERE id = ?",
        (rule_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# TEST NETWORK TRAFFIC
@app.route("/test_packet", methods=["POST"])
def test_packet():

    source_ip = request.form["source_ip"].strip()
    port = request.form["port"].strip()
    protocol = request.form["protocol"]

    try:
        ipaddress.ip_address(source_ip)

        if not port.isdigit() or not 1 <= int(port) <= 65535:
            raise ValueError()

        if protocol not in ["TCP", "UDP"]:
            raise ValueError()

    except ValueError:
        return {"error": "Invalid IP address, port or protocol"}, 400

    decision, reason = evaluate_packet(
        source_ip, int(port), protocol
    )

    return {
        "decision": decision,
        "reason": reason
    }


if __name__ == "__main__":

    initialize_db()

    app.run(debug=True)

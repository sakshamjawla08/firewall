# 🔥 Firewall Rule Engine

A Python-based **Firewall Rule Engine** built using Flask and SQLite that simulates basic firewall functionality by evaluating network traffic against predefined security rules.

The application provides a web-based dashboard to manage firewall rules, test network packets, and monitor allowed and blocked traffic.

## 🚀 Features

- **Firewall Rule Management:** Add and delete firewall rules.
- **IP Address Filtering:** Filter traffic using specific IPv4/IPv6 addresses or `ANY`.
- **Port Filtering:** Control traffic using specific port numbers or `ANY`.
- **Protocol Filtering:** Support for TCP, UDP, and ANY protocols.
- **Traffic Evaluation:** Automatically ALLOW or BLOCK packets based on matching rules.
- **Default Deny Policy:** Blocks traffic when no matching rule is found.
- **Traffic Logging:** Stores packet evaluation results in an SQLite database.
- **Dashboard:** Displays firewall rules, traffic statistics, and recent activity.
- **Input Validation:** Validates IP addresses, ports, protocols, and firewall actions.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database management |
| HTML/CSS | Frontend interface |
| Jinja2 | Dynamic HTML rendering |

## 📁 Project Structure

```text
Firewall-Rule-Engine/
│
├── app.py
├── firewall.db
├── requirements.txt
├── templates/
│   └── index.html
│
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Firewall-Rule-Engine.git
```

### 2. Navigate to the Project Directory

```bash
cd Firewall-Rule-Engine
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

```text
http://127.0.0.1:5000/
```

## 🔐 How It Works

The Firewall Rule Engine evaluates incoming simulated network packets against firewall rules stored in the SQLite database.

**Evaluation Process:**

1. Receive source IP address, port number, and protocol.
2. Retrieve firewall rules from the database in ascending ID order.
3. Compare packet details with each rule.
4. If a matching rule is found, execute its action (`ALLOW` or `BLOCK`).
5. If no matching rule exists, apply the default deny policy.
6. Save the evaluation result and reason in the traffic logs.

### Example Firewall Rules

| Source IP | Port | Protocol | Action |
|---|---|---|---|
| 192.168.1.10 | 80 | TCP | ALLOW |
| 192.168.1.20 | 443 | TCP | BLOCK |
| ANY | 53 | UDP | ALLOW |
| ANY | ANY | ANY | BLOCK |

## 📊 Dashboard

The dashboard displays:

- Total Firewall Rules
- Total Traffic Logs
- Allowed Packets
- Blocked Packets
- Configured Firewall Rules
- Recent Traffic Activity

## 🧪 Testing

You can test network traffic by providing:

- Source IP Address
- Destination Port
- Network Protocol (TCP/UDP)

The engine returns:

- **ALLOW:** Traffic matches an ALLOW rule.
- **BLOCK:** Traffic matches a BLOCK rule or no matching rule exists.
- **Reason:** Explains why the packet was allowed or blocked.

## ⚠️ Disclaimer

This project is an educational simulation of firewall rule evaluation. It does not directly intercept, inspect, or filter real network packets. It is intended for learning Python, Flask, database management, and basic network security concepts.

## 👨‍💻 Author

**Saksham Jawla**

GitHub: [@sakshamjawla08](https://github.com/sakshamjawla08)

---

⭐ If you find this project useful, consider giving it a star!

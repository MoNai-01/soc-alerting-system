# 🚨 SOC Alerting System (Filebeat + Logstash + Email Alerts)

A simple but powerful Security Operations Center (SOC) alerting setup that detects:
- SSH brute-force login attempts
- SQL Injection (SQLi)
- Cross-site Scripting (XSS)

## 📌 Summary

This project simulates a real-world SOC pipeline using open source tools:
- 🐍 Python for alerting
- 📦 Filebeat for log shipping
- 🔍 Logstash for parsing + detection
- 📊 Kibana for visualization
- ✉️  Email for real-time alerting

> Designed and tested on Kali Linux and Ubuntu ELK VM inside VirtualBox.

---

## 🧠 Architecture

![SOC Architecture](dashboards/soc_alert_architecture.png)

---

## ⚙️ Requirements

Install the following tools on the corresponding VMs:
🛠️ On Kali Linux VM:

    Apache2 (for web server logs)

    Filebeat 7.17+

    Python 3.8+

    pip install python-dotenv

🛠️ On Ubuntu Server VM:

    Elasticsearch 7.17+

    Logstash 7.17+

    Kibana 7.17+

## ⚙️ How to Run

### 🖥️ Setup

Clone the repo

```bash
git clone https://github.com/MoNai-01/soc-alerting-system.git
cd soc-alerting-system
```
### 🐧 Ubuntu Server VM (SIEM Stack)
1. Install Elastic Stack
```bash
sudo apt update
sudo apt install elasticsearch logstash kibana
```
2. Enable and Start Services
```bash
sudo systemctl enable elasticsearch logstash kibana
sudo systemctl start elasticsearch logstash kibana
```
3. Configure Logstash
```bash
sudo cp logstash/01-logstash.conf /etc/logstash/conf.d/
sudo systemctl restart logstash
```
4. Setup Python Email Script
```bash
pip install python-dotenv
cp scripts/email_alert.py /opt/
cp .env.example /opt/.env
nano /opt/.env
```
4.1. Add
```bash
EMAIL_ADDRESS=youremail@gmail.com
EMAIL_PASSWORD=your_app_password
```

### 🧪 Kali Linux VM (Log Generator + Filebeat + Email Alerts)
1. Enable and install Apache2 and Filebeat
```bash
sudo apt update
sudo apt install apache2 filebeat
sudo systemctl enable filebeat
sudo systemctl start apache2
```
2. Configure Filebeat
```bash
sudo cp filebeat/filebeat.yml /etc/filebeat/filebeat.yml
sudo systemctl restart filebeat
```

### 💣 Simulate Attacks (localhost)
🚨 SSH Brute Force
```bash
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.x.x
```
🚨 SQL Injection
````bash
curl "http://192.168.x.x/?id=1%27%20OR%20%271%27%3D%271"
```
🚨 XSS Payload
```bash
curl "http://192.168.x.x/?q=<script>alert(1)</script>"
````

### Start Alert Script
```bash
sudo python3 /opt/email_alert.py
```

## 📊 Access Dashboard
http://<ubuntu-elk-ip>:5601

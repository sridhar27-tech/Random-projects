
# NovaPulse 🌌

**Real-time collaborative pulse monitoring & analytics dashboard**  
*Track, visualize, and analyze system metrics with beautiful real-time insights.*

![NovaPulse Banner](https://raw.githubusercontent.com/novapulse/.github/main/profile/banner.png)

![GitHub stars](https://img.shields.io/github/stars/novapulse/novapulse?style=social)
![License](https://img.shields.io/github/license/novapulse/novapulse)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue)

---

## ✨ Features

- **Real-time Metrics Streaming** using WebSockets
- **Beautiful Interactive Dashboards** built with React + Recharts
- **Multi-source Integration** — Docker, Kubernetes, Prometheus, AWS CloudWatch
- **AI-powered Anomaly Detection** (using Isolation Forest + Prophet)
- **Alerting System** with Slack, Discord, and Email notifications
- **Team Collaboration** — Shared dashboards and comment threads
- **Self-hosted** or Cloud-ready deployment

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/novapulse/novapulse.git
cd novapulse

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

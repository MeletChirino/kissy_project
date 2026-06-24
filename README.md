# Confections Workshop V1

A private, lightweight, and frictionless administrative system designed for a small-scale custom sewing and embroidery workshop. The system combines an AI-driven Telegram interface to eliminate technical friction with a clean Streamlit dashboard for monitoring business operations.

## 🎯 Core Features

### 1. Telegram AI Engine (Ingress)
- **Natural Language Input:** Send messages via Telegram (e.g., "Expense: 500 on fabrics" or "New order accepted").
- **LLM Parsing:** Automatically maps unstructured text into structured JSON payloads for orders, items, payments, or expenses.
- **Instant Feedback:** The bot confirms the transaction details with a confirmation card.

### 2. Streamlit Central Dashboard (Egress)
A read-only monitoring suite featuring:
- **Work Workflow (Kanban):** Tracking `orders`.`order_status`.
- **Payment Deadlines (Calendar):** Monitoring `payments`.`payment_date`.

## 🛠 Technology Stack

- **Backend & Database:** PostgreSQL + NocoDB (Relational database interface & REST API generation).
- **Frontend/Dashboard:** Streamlit (Python) embedding NocoDB iFrames.
- **AI Layer:** Custom Python container handling Telegram Bot API and LLM integration via Ollama.
- **Infrastructure:** Dockerized environment for easy deployment on homelab hardware.

## 🚀 Deployment & Setup

### Infrastructure
The system uses `docker-compose` to run the core stack:
- **PostgreSQL:** Persistence layer (`confections_core` database).
- **NocoDB:** Relational management interface (API endpoint at port 8080).

### Database Provisioning
To maintain version control and ensure scalability, the database schema is managed via infrastructure as code. The repository includes a `setup_db.py` script to:
1. **Authenticate** with the NocoDB instance.
2. **Initialize** the project workspace.
3. **Create Tables:** Programmatically build base tables for clients, expenses, orders, items, etc.
4. **Relations:** Establish Foreign Key links across the schema.

## 📊 Data Architecture

The system tracks three core domains:

| Table | Description | Key Metrics/Links |
| :--- | :--- | :--- |
| **Clients** | Customer records & preferences | Name, Phone |
| **Orders** | Main order headers | Status, Promised Date, Balance |
| **Order Items** | Specific product details | Type, Embroidery Details, Measurements |
| **Embroidery Jobs** | Outsourced tracker | Vendor Status, Costs |
| **Payments** | Installment & Credit tracking | Payment Method, Date |
| **Expenses** | General overhead & materials | Category (Fabrics, Threads, etc.) |

## 🗺 Roadmap

- **Phase 1:** Deploy Docker infrastructure and initialize Postgres/NocoDB.
- **Phase 2:** Develop Streamlit dashboard with Kanban/Calendar integrations.
- **Phase 3:** Build Telegram Bot service and LLM parsing routines.
- **Phase 4:** Implement cron-based proactive notifications for overdue balances.

# 📑 System Architecture & Stack Document: Kissy Project

## 1. Executive Summary

A private, lightweight, and frictionless administrative system designed for a small-scale custom sewing and embroidery workshop. The system features a headless relational database backend, a voice/text-driven AI input channel via Telegram to eliminate technical friction for the operator, and a clean, read-only monitoring dashboard built in Streamlit using embedded views.

## 2. Technology Stack & Infrastructure (Homelab Deployment)

The entire ecosystem will run on a local Docker infrastructure.

- Database & Headless Backend: PostgreSQL as the storage engine + NocoDB as the relational interface and REST API generator.

- User Interface / Informational Dashboard: Streamlit (Python-based container) embedding native NocoDB iFrames (Kanban & Calendar views) and rendering financial KPI cards.

- AI Integration & Automation Layer ("The Brain"): A custom Python container handling the Telegram Bot API and an LLM engine to parse unstructured natural language into structured JSON payloads.

## 3. Relational Data Model (NocoDB / Postgres Schema)

### 3.1. Table: clients

Stores customer contact records and historical preferences.

- id (Integer, Primary Key, Auto-Increment)
- full_name (String/Single Line Text, Required)
- phone (String/Phone Number)
- special_notes (Long Text) -> e.g., "Prefers hypoallergenic fabrics."

### 3.2. Table: orders

Represents the main order header/metadata.

- id (Integer, Primary Key, Auto-Increment)
- client_id (Integer, Foreign Key linked to clients.id, Many-to-One)
- date_received (Date)
- date_delivery_promised (Date)
- total_amount (Decimal/Currency) -> Sum of related order_items.
- outstanding_balance (Decimal/Currency) -> Formula: total_amount minus Sum of related payments.
- payment_status (Select/Enum: Pending, Partially Paid, Fully Paid)
- order_status (Select/Enum: On Hold, In Production, Ready for Embroidery, Being Embroidered, Finished, Delivered)

### 3.3. Table: order_items

Handles the line items within an order, capturing specifications for standardized or custom tailored pieces.

- id (Integer, Primary Key, Auto-Increment)
- order_id (Integer, Foreign Key linked to orders.id, Many-to-One)
- product_type (Select/Enum: Towel, Bathrobe, Baby Onesie, Custom Tailored)
- quantity (Integer, Default: 1)
- unit_price (Decimal/Currency)
- requires_embroidery (Boolean, Default: False)
- embroidery_text (String/Single Line Text) -> The exact name/phrase to engrave.
- design_details (Long Text) -> For custom pieces e.g., "Long sleeve with pink lace".
- measurements (Long Text) -> e.g., "Chest: X cm, Length: Y cm".

### 3.4. Table: embroidery_jobs

Tracks operations outsourced to the external embroidery vendor.

- id (Integer, Primary Key, Auto-Increment)
- order_item_id (Integer, Foreign Key linked to order_items.id, One-to-One)
- embroidery_status (Select/Enum: Pending Shipment, With Vendor, Received OK, Rejected/Error)
- date_sent (Date, Nullable)
- date_returned (Date, Nullable)
- vendor_cost (Decimal/Currency) -> Outsourced processing cost.

### 3.5. Table: payments

Tracks installment plans and credit-based milestone payments (every 15 to 20 days).

- id (Integer, Primary Key, Auto-Increment)
- order_id (Integer, Foreign Key linked to orders.id, Many-to-One)
- payment_date (Date)
- amount (Decimal/Currency)
- payment_method (Select/Enum: Cash, Bank Transfer, Other)
- notes (String/Single Line Text)

### 3.6. Table: expenses

Manages general shop overhead, hardware maintenance, and raw material expenses.

- id (Integer, Primary Key, Auto-Increment)
- date (Date)
- category (Select/Enum: Fabrics, Threads, Vendor Payments, Utilities, Machine Maintenance, Other)
- amount (Decimal/Currency)
- description (String/Single Line Text)

## 4. System Interfaces & Workflows

### 4.1. The Telegram AI Engine (Ingress Layer)

- Text Input: User sends a text message via Telegram.
- Intent Parsing (LLM): The transcribed text is sent to the LLM with a system prompt to map data to a JSON object matching the schemas of orders/order_items, payments, or expenses.
- API Execution: The Python automation engine makes REST requests to NocoDB endpoints.
- User Feedback: The bot responds with a clean confirmation card summarizing the parsed transaction.

### 4.2. The Streamlit Central Dashboard (Egress Layer)

Structured in three read-only browser tabs using native Streamlit modules and HTML/iFrame embeddings:

- Tab 1: Work Workflow (Kanban): Embeds NocoDB's Shared Kanban View tracking orders.order_status.
- Tab 2: Payment Deadlines (Calendar): Embeds NocoDB's Shared Calendar View tracking payments.payment_date.
- Tab 3: Financial Analytics:
  - Renders metrics blocks (st.metric) calculating Total Collected (SUM of payments), Total Spent (SUM of expenses), and Net Profit.
  - Displays a simple st.bar_chart charting monthly expense distributions against income.

## 5. Development Roadmap (Sprint Breakdown)

- Phase 1 (Core Backend): Deploy docker-compose.yml containing PostgreSQL and NocoDB. Initialize tables and relationships.
- Phase 2 (Dashboard Integration): Write the app.py script for Streamlit. Configure st.components.v1.iframe components pointing to the public NocoDB views. Add KPI tracking cards.
- Phase 3 (Telegram Pipeline): Build the Python Telegram bot service. Write LLM parsing routines to process statements such as "Expense: 500 on fabrics" or "New order for customer X" into REST queries.
- Phase 4 (Asynchronous Notifications): Code a cron-like daemon executing a daily scan over the payments table to identify credit balances over 20 days old, sending proactive notifications to the operator via Telegram.

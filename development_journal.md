# Development Journal - Kissy Project

## Project Overview
A private administrative system for a custom sewing/embroidery workshop featuring an AI-driven Telegram interface and a Streamlit dashboard.

---

## Session Log: 2026-06-24
**Context:** Initial project setup, documentation refinement, and database infrastructure provisioning.

### Summary of Actions:
1. **Documentation Generation:** Created `README.md` by synthesizing data from `architecture_plan.md` and `deployment_and_setup.md`.
   - Consolidated system architecture, core features (Telegram AI Ingress, Streamlit Egress), and technology stack (PostgreSQL, NocoDB, Ollama).

2. **Requirement Refinements:**
   - **LLM Integration:** Updated the documentation to specify **Ollama** as the local LLM provider for parsing natural language into structured JSON.
   - **Feature Scope:** Removed "Financial Analytics" from the Streamlit Dashboard description per user instruction to focus on workflow tracking.

3. **Database Infrastructure (IaC):** Generated `setup_db.py` to automate relational database provisioning via NocoDB's Metadata API.
   - **Tables Created:** `clients`, `orders`, `order_items`, `embroidery_jobs`, `payments`, and `expenses`.
   - **Relational Constraints:** Configured One-to-Many relationships (e.g., Linking orders to clients, items to orders) using NocoDB's Remote APIed methods.
   - **Dynamic Mapping:** Ensured that status fields (`order_status`, `payment_status`) were configured as Select/Enum types with prescribed options.

### Decisions & Technical Notes:
- **Hardware:** Target deployment is a local Docker environment on homelab hardware.
- **Automation Strategy:** Database schema management is handled via Python scripts rather than manual UI interaction to ensure version control and consistency.
- **LLM Role:** The model (Ollama) is tasked with parsing unstructured text from Telegram into structured JSON payloads for transaction records.

---
*Next steps: Initialize Docker environment and run `setup_db.py`.*

# 🚀 Deployment & Database Setup Guide: Kissy Project

## 1. Infrastructure (Docker Compose)
This multi-container setup initializes the PostgreSQL database engine and binds it to NocoDB as the primary metadata and data storage layer.

```yaml
version: '3.8'

services:
  postgres_db:
    image: postgres:15-alpine
    container_name: confections_postgres
    environment:
      POSTGRES_DB: confections_core
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: changeme_db_password
    volumes:
      = ./postgres_data:/var/lib/postgresql/data
    networks:
      - confections_net
    restart: always

  nocodb_backend:
    image: nocodb/nocodb:latest
    container_name: confections_nocodb
    environment:
      NC_DB: "pg://postgres_db:5432?u=admin&p=changeme_db_password&d=confections_core"
      NC_AUTH_JWT_SECRET: "changeme_jwt_secret_key"
    ports:
      - "8080:8080"
    volumes:
      - ./nocodb_data:/usr/app/data
    depends_on:
      - postgres_db
    networks:
      - confections_net
    restart: always

networks:
  confections_net:
    driver: bridge
```
## 2. Infrastructure as Code (IaC) Database Provisioning

To ensure scalability, avoid manual UI interactions, and maintain version control, the database schema defined in `architecture_plan.md` must be deployed programmatically using NocoDB's Metadata REST API.

### 2.1. Provisioning Protocol (The `setup_db.py` Strategy)

The automated Python setup script must execute the following sequential operations:

1. **Authentication:** Authenticate against the NocoDB instance (`http://localhost:8080`) to retrieve the `xc-auth` token or initialize using a static Auth Token.
2. **Project Initialization:** Programmatically verify or create the workspace project container.
3. **Table Creation:** Send POST requests to `/api/v1/meta/projects/{projectId}/tables` containing the UI Data Type (`uidt`) payload for each independent table (`clients`, `expenses`).
4. **Relational Constraints:** Once base tables exist, execute relational API requests to map Foreign Key links (e.g., linking `orders` to `clients`, and `order_items` to `orders`).
    

### 2.2. Core UI Data Types (UIDT) Mapping for LLM Generation

When prompting the local AI to build the setup script, map fields using NocoDB's specific type definitions:

- Text fields -> `"uidt": "SingleLineText"`
- Long descriptions/notes -> `"uidt": "LongText"`
- Numeric/Currency -> `"uidt": "Decimal"` or `"Number"`
- Status/Enums -> `"uidt": "Select"` (pass options array)
- Dates -> `"uidt": "Date"`
- Relations -> `"uidt": "LinkToAnotherRecord"` (Many-to-One / One-to-Many configurations)

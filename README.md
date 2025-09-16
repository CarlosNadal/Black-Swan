## 🦢 Black Swan — Wi-Fi Reconnaissance & Visualization Tool

Black Swan is a full-stack project designed to bring BloodHound-style visualization to wireless reconnaissance.
It parses airodump-ng CSV output, maps Access Points (APs) and connected clients, and prepares a structured dataset for interactive visualization and attack orchestration.

## 🔑 Key Features

- **CSV → JSON Parsing:** Python script converts raw airodump-ng CSV into clean, structured JSON.

- **Client-AP Mapping:** Automatically links stations to their associated APs.

- **Frontend-Ready:** Outputs data ready for React-based visualization.

- **Extensible Design:** Future integration with FastAPI backend and attack modules (handshake capture, deauth, PMKID, Evil Twin).

- **Red Team Focus:** Built for reconnaissance and adversary simulation workflows.

```mermaid
flowchart TD
    A["Wi-Fi Recon (airodump-ng)"] --> B["Parse CSV (parse_airodump.py)"]
    B --> C["Structured JSON (recon_output.json)"]
    C --> D["React Frontend Visualization"]
    D --> E["Target Selection & Attack Launch (Future)"]

    style A fill:#ffedcc,stroke:#e69b00,stroke-width:2px
    style B fill:#d1f0ff,stroke:#007acc,stroke-width:2px
    style C fill:#e7e7e7,stroke:#555,stroke-width:2px
    style D fill:#e6ffe6,stroke:#009900,stroke-width:2px
    style E fill:#fff0f5,stroke:#cc0066,stroke-width:2px
```

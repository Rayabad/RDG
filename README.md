# Universal RDG Optimization Engine (v2.2.0-Stable)

[![GitHub Actions](https://shields.io)](https://github.com)
[![License: MIT](https://shields.io)](https://opensource.org)
[![DOI](https://shields.io)](https://zenodo.org)

An asynchronous, high-concurrency microservice engine designed to bridge quantum-mechanical Density Functional Theory (DFT) data loops with experimental Molecular Beam Epitaxy (MBE) synthesis telemetries. Built using modern Python architectures, this package automates real-time thermodynamic recipe corrections to maximize semiconductor device yield prior to expensive cleanroom vacuum execution loops.

---

## 🔬 Core Physics & Algorithmic Design

The software ingest structural and target device parameters to neutralize atomic layer drift through two main calculations:

1. **Quantum Deviation Matrix ($\Delta E_{quantum}$)**: Calculates the absolute deviation between an idealized target energy threshold derived from optical requirements ($\lambda$) and the baseline simulated material bandgap:
   $$\Delta E_{quantum} = \left| E_{bandgap} - \frac{1239.84}{\lambda_{target}} \right|$$

2. **Thermodynamic Rebalancing**: Maps the calculated energy drift to an automated thermal compensation vector ($\Delta T$) inversely scaled against physical crystal growth rates ($G_{rate}$):
   $$T_{recommended} = T_{substrate} + \frac{\Delta E_{quantum} \times 150.0}{G_{rate}}$$

---

## 🏗️ Production Architecture Features

* **Non-Blocking Concurrent Loops**: Offloads synchronous, heavy matrix calculations using `asyncio.to_thread()` to safeguard the FastAPI web loop under high-throughput cleanroom API requests.
* **Modern Lifespan Isolation**: Replaces deprecated startup/shutdown event hooks with isolated, thread-safe asynchronous transaction context managers (`contextlib.asynccontextmanager`).
* **Cross-Disciplinary Schema Guards**: Utilizes Pydantic v2 `model_validator` properties to block chemical flux configurations when non-III-V variants (such as `ZnO` or `Bi2Sr2CaCu2O8`) are submitted.
* **Streaming Read Performance**: Employs indexed B-Tree scanning constraints coupled with streaming limit/offset pagination to mitigate memory overhead.

---

## 🚀 Quick Start & Testing Lab

### Local Quick Start (In-Memory Testing)

1. **Clone the repository and install dependencies**:
   ```bash
   git clone https://github.com
   cd your-repo
   pip install fastapi uvicorn pydantic sqlmodel aiosqlite httpx pytest pytest-asyncio
   ```

2. **Boot the API Server Gateway**:
   ```bash
   uvicorn app:app --host 127.0.0.1 --port 8000
   ```

3. **Fire a Sample Cleanroom Payload**:
   Open a separate terminal window and dispatch a payload using `curl`:
   ```bash
   curl -X POST "http://127.0.0" \
        -H "Content-Type: application/json" \
        -d '{
          "material_system": "III-V_GaAs",
          "dft_inputs": {"lattice_constant_angstrom": 5.653, "bandgap_ev": 1.424, "defect_energy_density": 0.012},
          "mbe_logs": {"substrate_temperature_c": 580.0, "flux_ratio_v_iii": 15.4, "growth_rate_um_per_hr": 1.0},
          "targets": {"target_wavelength_nm": 850.0, "min_carrier_mobility": 8500.0}
        }'
   ```

4. **Verify the Output Schema**:
   The engine will return an mathematically balanced yield recipe layout:
   * **Rec. MBE Substrate Heat Layer**: `585.20 °C` (Stabilized via standard round-to-nearest-even rules)
   * **Target Flux V/III Distribution**: `16.17` Ratio
   * **Fabrication Structural Yield**: `99.31%`

---

## 📊 API Endpoint Reference

| Endpoint | HTTP Method | Description | Content-Type |
| :--- | :--- | :--- | :--- |
| `/api/v2/optimize` | `POST` | Ingests raw cleanroom datasets, executes math in isolated threads, and writes variables to the permanent ledger. | `application/json` |
| `/api/v2/history` | `GET` | Fetches historical runs with streaming limits and indexed `material_system` performance parameters. | `application/json` |
| `/docs` | `GET` | Interactive Swagger UI visual playground for local telemetry tracking. | `text/html` |

---

## 🛠️ Verification & Continuous Integration

An automated cloud testing matrix executes with every repository update via GitHub Actions. To run the validation checks manually on your local system run:
```bash
pytest test_app.py -v
```

---

## 🎓 Open-Science Attribution & Citation

If you use this software engine or its thermodynamic calculation core in an academic publication, please cite the corresponding Zenodo artifact package:

```bibtex
@software{doe_jane_2026_rdg,
  author       = {Doe, Jane},
  title        = {Universal RDG Optimization Engine: Asynchronous Data Ingestion and Quantum-Thermodynamic Realignment Framework},
  version      = {v2.0.0-stable},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.placeholder},
  url          = {https://doi.org}
}
```

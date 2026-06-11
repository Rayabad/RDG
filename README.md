# RDG - Material Recipe Optimizer

FastAPI service for optimizing semiconductor material growth recipes (III-V compounds via Molecular Beam Epitaxy).

## What it does

The service accepts material parameters (from DFT calculations and MBE growth logs) and returns an optimized substrate temperature and predicted device yield.

**Main endpoint:**
- `POST /api/v2/optimize`

**Input example:**
```json
{
  "material_system": "III-V_GaAs",
  "dft_inputs": {
    "lattice_constant_angstrom": 5.653,
    "bandgap_ev": 1.424,
    "defect_energy_density": 0.012
  },
  "mbe_logs": {
    "substrate_temperature_c": 580.0,
    "flux_ratio_v_iii": 15.4,
    "growth_rate_um_per_hr": 1.0
  },
  "targets": {
    "target_wavelength_nm": 850.0,
    "min_carrier_mobility": 8500.0
  }
}

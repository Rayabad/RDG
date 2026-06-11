import pytest
from httpx import ASGITransport, AsyncClient

from app import app


@pytest.mark.asyncio
async def test_successful_optimization():
    """Verifies that valid III-V_GaAs cleanroom inputs yield the exact expected physics recipe."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "material_system": "III-V_GaAs",
            "dft_inputs": {
                "lattice_constant_angstrom": 5.653,
                "bandgap_ev": 1.424,
                "defect_energy_density": 0.012,
            },
            "mbe_logs": {
                "substrate_temperature_c": 580.0,
                "flux_ratio_v_iii": 15.4,
                "growth_rate_um_per_hr": 1.0,
            },
            "targets": {
                "target_wavelength_nm": 850.0,
                "min_carrier_mobility": 8500.0,
            },
        }
        response = await ac.post("/api/v2/optimize", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert data["material_system"] == "III-V_GaAs"
        assert data["optimized_recipe"]["recommended_substrate_temp_c"] == 585.2
        assert data["optimized_recipe"]["predicted_device_yield_percent"] == 99.31


@pytest.mark.asyncio
async def test_material_flux_validation_blocker():
    """Verifies that an invalid flux ratio on a III-V system is caught by the schema parser."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        invalid_payload = {
            "material_system": "III-V_GaAs",
            "dft_inputs": {
                "lattice_constant_angstrom": 5.653,
                "bandgap_ev": 1.424,
                "defect_energy_density": 0.012,
            },
            "mbe_logs": {
                "substrate_temperature_c": 580.0,
                "flux_ratio_v_iii": 0.0,
                "growth_rate_um_per_hr": 1.0,
            },
            "targets": {
                "target_wavelength_nm": 850.0,
                "min_carrier_mobility": 8500.0,
            },
        }
        response = await ac.post("/api/v2/optimize", json=invalid_payload)

        assert response.status_code == 422

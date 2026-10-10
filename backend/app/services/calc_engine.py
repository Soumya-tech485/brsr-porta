from typing import Dict, Any

def calc_scope_1(fuel_quantities: Dict[str, float], emission_factors: Dict[str, float]) -> float:
    """Calculate Scope 1 emissions in tCO2e."""
    total = 0.0
    for fuel, qty in fuel_quantities.items():
        factor = emission_factors.get(fuel, 0.0)
        total += qty * factor
    return round(total, 4)

def calc_scope_2(electricity_kwh: float, grid_factor: float) -> float:
    """Calculate Scope 2 emissions in tCO2e."""
    return round(electricity_kwh * grid_factor, 4)

def calc_intensity_per_rupee(metric_value: float, revenue_in_cr: float) -> float:
    """Calculate intensity per rupee in Cr."""
    if revenue_in_cr <= 0:
        return 0.0
    return round(metric_value / revenue_in_cr, 6)

def calc_ppp_intensity(metric_value: float, revenue_in_inr: float, ppp_rate: float) -> float:
    """Calculate intensity PPP-adjusted (per Mn USD)."""
    if ppp_rate <= 0 or revenue_in_inr <= 0:
        return 0.0
    revenue_in_mn_inr = revenue_in_inr / 1_000_000
    revenue_in_mn_usd_ppp = revenue_in_mn_inr / ppp_rate
    return round(metric_value / revenue_in_mn_usd_ppp, 6)

def calc_ltifr(lost_time_injuries: float, total_hours_worked: float) -> float:
    """Calculate Lost Time Injury Frequency Rate."""
    if total_hours_worked <= 0:
        return 0.0
    return round((lost_time_injuries * 1_000_000) / total_hours_worked, 4)

def calc_energy_total(energy_sources: Dict[str, float], calorific_values: Dict[str, float]) -> Dict[str, float]:
    """Calculate total energy in GJ and % renewable."""
    total_renewable = 0.0
    total_non_renewable = 0.0
    
    for source, qty in energy_sources.items():
        # electricity is in kWh, convert to GJ directly (0.0036)
        if "electricity" in source:
            gj = qty * 0.0036
        else:
            gj = qty * calorific_values.get(source, 0.0)
            
        if "non_renewable" in source:
            total_non_renewable += gj
        else:
            total_renewable += gj
            
    total = total_renewable + total_non_renewable
    pct_renewable = (total_renewable / total * 100) if total > 0 else 0.0
    
    return {
        "total_gj": round(total, 4),
        "renewable_gj": round(total_renewable, 4),
        "non_renewable_gj": round(total_non_renewable, 4),
        "pct_renewable": round(pct_renewable, 2)
    }

def calc_turnover_rate(leavers: float, opening: float, closing: float) -> float:
    """Calculate Turnover Rate."""
    avg_headcount = (opening + closing) / 2
    if avg_headcount <= 0:
        return 0.0
    return round((leavers * 100) / avg_headcount, 2)

def calc_percentage(part: float, total: float) -> float:
    """Generic percentage calculation for Gender Wage %, MSME %, etc."""
    if total <= 0:
        return 0.0
    return round((part / total) * 100, 2)

def calc_accounts_payable_days(accounts_payable: float, cost_of_purchases: float) -> float:
    """Calculate Accounts Payable Days."""
    if cost_of_purchases <= 0:
        return 0.0
    return round((accounts_payable * 365) / cost_of_purchases, 2)

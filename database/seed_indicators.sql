USE esgraph;

INSERT INTO indicator (code, format_version, section, principle, tier, is_core, level, data_type, unit, aggregation_rule, formula_key, evidence_required, evidence_hint, sub_keys, sort_order) VALUES
-- 1. GHG Footprint
('GHG_S1', '2024', 'C', '6', 'Essential', TRUE, 'site', 'numeric', 'tCO2e', 'sum', 'scope_1_calc', TRUE, 'fuel purchase invoices / stock register', '["diesel", "petrol", "coal", "natural_gas"]', 10),
('GHG_S2', '2024', 'C', '6', 'Essential', TRUE, 'site', 'numeric', 'tCO2e', 'sum', 'scope_2_calc', TRUE, 'electricity utility bill', '["grid_electricity"]', 20),

-- 2. Water Footprint
('WATER_WITHDRAWAL', '2024', 'C', '6', 'Essential', TRUE, 'site', 'numeric', 'kL', 'sum', 'water_withdrawal', TRUE, 'meter readings / tanker records', '["surface", "ground", "third_party", "seawater", "other"]', 30),
('WATER_DISCHARGE', '2024', 'C', '6', 'Essential', TRUE, 'site', 'numeric', 'kL', 'sum', 'water_discharge', TRUE, 'discharge meter / manifest', '["surface", "ground", "third_party", "seawater", "other"]', 40),

-- 3. Energy Footprint
('ENERGY_CONS', '2024', 'C', '6', 'Essential', TRUE, 'site', 'numeric', 'GJ', 'sum', 'energy_total', TRUE, 'utility bills / fuel records', '["electricity_renewable", "electricity_non_renewable", "fuel_renewable", "fuel_non_renewable"]', 50),

-- 4. Circularity (Waste)
('WASTE_GEN', '2024', 'C', '6', 'Essential', TRUE, 'site', 'numeric', 'MT', 'sum', 'waste_total', TRUE, 'manifests / vendor receipts', '["plastic", "e_waste", "bio_medical", "c_and_d", "battery", "hazardous", "non_hazardous"]', 60),
('WASTE_REC', '2024', 'C', '6', 'Essential', TRUE, 'site', 'numeric', 'MT', 'sum', 'waste_recovered', TRUE, 'recovery certificates', '["plastic", "e_waste", "bio_medical", "c_and_d", "battery", "hazardous", "non_hazardous"]', 65),
('WASTE_DISP', '2024', 'C', '6', 'Essential', TRUE, 'site', 'numeric', 'MT', 'sum', 'waste_disposed', TRUE, 'disposal receipts', '["incineration", "landfill", "other"]', 68),

-- 5. Employee well-being & safety
('WORKFORCE', '2024', 'C', '3', 'Essential', TRUE, 'site', 'numeric', 'count', 'snapshot_last', 'headcount', TRUE, 'payroll / muster roll', '["emp_perm_m", "emp_perm_f", "emp_temp_m", "emp_temp_f", "work_perm_m", "work_perm_f", "work_temp_m", "work_temp_f"]', 70),
('SAFETY_LTIFR', '2024', 'C', '3', 'Essential', TRUE, 'site', 'numeric', 'ratio', 'ratio_from_components', 'ltifr_calc', TRUE, 'incident register', '["lost_time_injuries", "hours_worked"]', 80),
('SAFETY_INCIDENTS', '2024', 'C', '3', 'Essential', TRUE, 'site', 'numeric', 'count', 'sum', 'safety_incidents', TRUE, 'incident register', '["recordable_injuries", "high_consequence", "fatalities_emp", "fatalities_work"]', 85),
('WELLBEING_SPEND', '2024', 'C', '3', 'Essential', TRUE, 'site', 'numeric', 'INR', 'sum', 'wellbeing_spend', TRUE, 'financial records', '["spend"]', 88),

-- 6. Gender Diversity
('WAGES_GENDER', '2024', 'C', '5', 'Essential', TRUE, 'site', 'numeric', 'INR', 'sum', 'wages_gender', TRUE, 'payroll', '["gross_wages_female", "gross_wages_total"]', 90),
('POSH_COMPLAINTS', '2024', 'C', '5', 'Essential', TRUE, 'site', 'numeric', 'count', 'sum', 'posh_complaints', TRUE, 'icc records', '["received", "upheld"]', 95),

-- 7. Inclusive Development
('PROCUREMENT_MSME', '2024', 'C', '8', 'Essential', TRUE, 'site', 'numeric', 'INR', 'sum', 'procurement_msme', TRUE, 'purchase records', '["from_msme", "from_india", "total"]', 100),
('JOB_CREATION', '2024', 'C', '8', 'Essential', TRUE, 'site', 'numeric', 'INR', 'sum', 'job_creation', TRUE, 'payroll', '["wages_rural", "wages_semi_urban", "wages_total"]', 105),

-- 8. Fairness to customers & suppliers
('CYBER_INCIDENTS', '2024', 'C', '9', 'Essential', TRUE, 'corporate', 'numeric', 'count', 'sum', 'cyber_incidents', FALSE, 'IT incident log', '["data_breaches"]', 110),
('ACCOUNTS_PAYABLE', '2024', 'C', '9', 'Essential', TRUE, 'corporate', 'numeric', 'INR', 'value', 'accounts_payable', FALSE, 'financial statement', '["payable_amount", "cost_of_goods"]', 115),

-- 9. Openness of business
('CONCENTRATION', '2024', 'C', '9', 'Essential', TRUE, 'corporate', 'numeric', 'INR', 'value', 'concentration', FALSE, 'financial statement', '["purchases_trading_houses", "sales_dealers"]', 120),
('RELATED_PARTY', '2024', 'C', '9', 'Essential', TRUE, 'corporate', 'numeric', 'INR', 'value', 'related_party', FALSE, 'financial statement', '["purchases", "sales", "loans"]', 125),

-- 10. Value Chain
('VALUE_CHAIN_ASSESSED', '2024', 'C', 'N/A', 'Leadership', TRUE, 'corporate', 'numeric', 'percent', 'value', 'value_chain_assessed', FALSE, 'supplier assessment records', '["assessed_partners"]', 130);

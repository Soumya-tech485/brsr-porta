USE esgraph;

-- Demo Entities (1 group, 3 subsidiaries, 2 BUs each, 12 sites total)
INSERT INTO entity (id, name, type, parent_id, state, country, is_active) VALUES
(1, 'MEIL Group', 'group', NULL, 'Telangana', 'India', TRUE),

(2, 'Subsidiary A (Infra)', 'subsidiary', 1, 'Maharashtra', 'India', TRUE),
(3, 'Subsidiary B (Energy)', 'subsidiary', 1, 'Gujarat', 'India', TRUE),
(4, 'Subsidiary C (Water)', 'subsidiary', 1, 'Karnataka', 'India', TRUE),

(5, 'BU Roadworks', 'bu', 2, 'Maharashtra', 'India', TRUE),
(6, 'BU Bridges', 'bu', 2, 'Telangana', 'India', TRUE),
(7, 'BU Hydropower', 'bu', 3, 'Gujarat', 'India', TRUE),
(8, 'BU Solar', 'bu', 3, 'Rajasthan', 'India', TRUE),
(9, 'BU Water Treatment', 'bu', 4, 'Karnataka', 'India', TRUE),
(10, 'BU Irrigation', 'bu', 4, 'Andhra Pradesh', 'India', TRUE),

(11, 'Site A-1 (Highway)', 'site', 5, 'Maharashtra', 'India', TRUE),
(12, 'Site A-2 (Expressway)', 'site', 5, 'Uttar Pradesh', 'India', TRUE),
(13, 'Site A-3 (River Bridge)', 'site', 6, 'Bihar', 'India', TRUE),
(14, 'Site A-4 (Flyover)', 'site', 6, 'Telangana', 'India', TRUE),

(15, 'Site B-1 (Hydro Plant)', 'site', 7, 'Gujarat', 'India', TRUE),
(16, 'Site B-2 (Dam)', 'site', 7, 'Madhya Pradesh', 'India', TRUE),
(17, 'Site B-3 (Solar Park)', 'site', 8, 'Rajasthan', 'India', TRUE),
(18, 'Site B-4 (Wind Farm)', 'site', 8, 'Tamil Nadu', 'India', TRUE),

(19, 'Site C-1 (WTP Urban)', 'site', 9, 'Karnataka', 'India', TRUE),
(20, 'Site C-2 (Desalination)', 'site', 9, 'Tamil Nadu', 'India', TRUE),
(21, 'Site C-3 (Canal Network)', 'site', 10, 'Andhra Pradesh', 'India', TRUE),
(22, 'Site C-4 (Lift Irrigation)', 'site', 10, 'Telangana', 'India', TRUE);

-- Demo Users (3 users per role + 1 admin)
-- password is 'password123'
INSERT INTO user (id, name, email, password_hash, role, is_active) VALUES
(1, 'Group ESG Admin', 'admin@meil.com', '$2b$12$FegYrViXfgCDTQ5aMEWQiuTvVe.hmXrX0G79SOzPxqZW99JSihHL.', 'admin', TRUE),

(2, 'Manager A', 'managerA@meil.com', '$2b$12$FegYrViXfgCDTQ5aMEWQiuTvVe.hmXrX0G79SOzPxqZW99JSihHL.', 'manager', TRUE),
(3, 'Manager B', 'managerB@meil.com', '$2b$12$FegYrViXfgCDTQ5aMEWQiuTvVe.hmXrX0G79SOzPxqZW99JSihHL.', 'manager', TRUE),
(4, 'Manager C', 'managerC@meil.com', '$2b$12$FegYrViXfgCDTQ5aMEWQiuTvVe.hmXrX0G79SOzPxqZW99JSihHL.', 'manager', TRUE),

(5, 'Engineer 1', 'engineer1@meil.com', '$2b$12$FegYrViXfgCDTQ5aMEWQiuTvVe.hmXrX0G79SOzPxqZW99JSihHL.', 'engineer', TRUE),
(6, 'Engineer 2', 'engineer2@meil.com', '$2b$12$FegYrViXfgCDTQ5aMEWQiuTvVe.hmXrX0G79SOzPxqZW99JSihHL.', 'engineer', TRUE),
(7, 'Engineer 3', 'engineer3@meil.com', '$2b$12$FegYrViXfgCDTQ5aMEWQiuTvVe.hmXrX0G79SOzPxqZW99JSihHL.', 'engineer', TRUE);

-- User Sites
INSERT INTO user_site (user_id, entity_id) VALUES
(1, 1),
(2, 11), (2, 12), (2, 13), (2, 14), -- Manager A owns Sub A sites
(3, 15), (3, 16), (3, 17), (3, 18), -- Manager B owns Sub B sites
(4, 19), (4, 20), (4, 21), (4, 22), -- Manager C owns Sub C sites
(5, 11), (5, 12), -- Engineer 1 assigned to some Sub A sites
(6, 15), (6, 16), -- Engineer 2 assigned to some Sub B sites
(7, 19), (7, 20); -- Engineer 3 assigned to some Sub C sites

-- Reporting Periods (2 prior FYs of baselines + Current FY)
INSERT INTO reporting_period (id, fy_label, start_date, end_date, boundary, status, format_version) VALUES
(1, 'FY 2024-25', '2024-04-01', '2025-03-31', 'consolidated', 'open', '2024'),
(2, 'FY 2023-24', '2023-04-01', '2024-03-31', 'consolidated', 'locked', '2024'),
(3, 'FY 2022-23', '2022-04-01', '2023-03-31', 'consolidated', 'locked', '2024');

-- Emission Factors
INSERT INTO emission_factor (id, source_type, key_name, factor, unit, source_note, valid_from, is_placeholder) VALUES
(1, 'fuel', 'diesel', 2.68, 'tCO2e/kL', 'Synthetic demo data - DEFRA 2023 placeholder', '2022-04-01', TRUE),
(2, 'electricity', 'grid_electricity', 0.71, 'tCO2e/MWh', 'Synthetic demo data - CEA 2023 placeholder', '2022-04-01', TRUE);

-- Financials
INSERT INTO financials (entity_id, period_id, revenue_inr, ppp_rate, cost_of_purchases_inr, accounts_payable_inr, source_note) VALUES
(1, 1, 153680.00, 20.343, 85000.00, 12000.00, 'Synthetic demo financials');

-- Site Entries (Generating some data for 12 months for Site 11)
-- Normal data
INSERT INTO site_entry (entity_id, period_id, month_date, indicator_id, sub_key, value_num, status, entered_by, verified_by) VALUES
(11, 1, '2024-04-01', 1, 'diesel', 4000, 'verified', 5, 2),
(11, 1, '2024-05-01', 1, 'diesel', 4100, 'verified', 5, 2),
(11, 1, '2024-06-01', 1, 'diesel', 4200, 'verified', 5, 2),
(11, 1, '2024-07-01', 1, 'diesel', 3900, 'verified', 5, 2),
(11, 1, '2024-08-01', 1, 'diesel', 3800, 'verified', 5, 2),
(11, 1, '2024-09-01', 1, 'diesel', 3700, 'verified', 5, 2),
(11, 1, '2024-10-01', 1, 'diesel', 4300, 'verified', 5, 2),
(11, 1, '2024-11-01', 1, 'diesel', 4400, 'verified', 5, 2),
(11, 1, '2024-12-01', 1, 'diesel', 4500, 'verified', 5, 2),
(11, 1, '2025-01-01', 1, 'diesel', 4600, 'verified', 5, 2),
(11, 1, '2025-02-01', 1, 'diesel', 4200, 'verified', 5, 2),
(11, 1, '2025-03-01', 1, 'diesel', 4100, 'submitted', 5, NULL),

(15, 1, '2024-04-01', 1, 'diesel', 3000, 'verified', 6, 3),
(15, 1, '2024-05-01', 1, 'diesel', 3100, 'verified', 6, 3),
(15, 1, '2024-06-01', 1, 'diesel', 3200, 'verified', 6, 3),
(15, 1, '2024-07-01', 1, 'diesel', 3300, 'verified', 6, 3),
(15, 1, '2024-08-01', 1, 'diesel', 3400, 'verified', 6, 3),
(15, 1, '2024-09-01', 1, 'diesel', 3500, 'verified', 6, 3),
(15, 1, '2024-10-01', 1, 'diesel', 3600, 'verified', 6, 3),
(15, 1, '2024-11-01', 1, 'diesel', 3700, 'verified', 6, 3),
(15, 1, '2024-12-01', 1, 'diesel', 18500, 'verified', 6, 3), -- ML Anomaly injected
(15, 1, '2025-01-01', 1, 'diesel', 3800, 'verified', 6, 3),
(15, 1, '2025-02-01', 1, 'diesel', 3900, 'draft', 6, NULL);

-- Water entries with mismatch rule trigger
INSERT INTO site_entry (entity_id, period_id, month_date, indicator_id, sub_key, value_num, status, entered_by, verified_by) VALUES
(11, 1, '2024-04-01', 3, 'surface', 5000, 'verified', 5, 2),
(11, 1, '2024-04-01', 4, 'surface', 2000, 'verified', 5, 2);

-- Safety entries (1 fatality)
INSERT INTO site_entry (entity_id, period_id, month_date, indicator_id, sub_key, value_num, status, entered_by, verified_by) VALUES
(19, 1, '2024-06-01', 9, 'fatalities_work', 1, 'verified', 7, 4);

-- Add some sample flags
INSERT INTO flag (entity_id, period_id, indicator_id, rule_key, severity, message, source, is_resolved) VALUES
(15, 1, 1, 'anomaly_zscore', 'critical', 'Diesel consumption +310% vs site median', 'ml', FALSE),
(11, 1, 3, 'water_mismatch', 'warning', 'Water withdrawal and discharge mismatch > 10%', 'rule', FALSE),
(19, 1, 9, 'safety_fatality', 'critical', '1 worker fatality reported', 'rule', FALSE);

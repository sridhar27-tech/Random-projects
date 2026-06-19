-- Database Schema for Rejection Rate Analytics System
-- PostgreSQL Database

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS predictions CASCADE;
DROP TABLE IF EXISTS recommendations CASCADE;
DROP TABLE IF EXISTS batches CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'operator',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Manufacturing batches table
CREATE TABLE batches (
    batch_id SERIAL PRIMARY KEY,
    batch_number VARCHAR(50) UNIQUE NOT NULL,
    machine_temperature DECIMAL(5,2),
    operator_experience_years INTEGER,
    production_speed DECIMAL(6,2),
    raw_material_quality DECIMAL(5,2),
    maintenance_hours DECIMAL(5,2),
    shift VARCHAR(20),
    humidity_percent DECIMAL(5,2),
    machine_age_years INTEGER,
    inspection_thoroughness DECIMAL(5,2),
    supplier_rating DECIMAL(3,1),
    defect_history_count INTEGER,
    actual_status VARCHAR(20),
    created_by INTEGER REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions table
CREATE TABLE predictions (
    prediction_id SERIAL PRIMARY KEY,
    batch_id INTEGER REFERENCES batches(batch_id) ON DELETE CASCADE,
    predicted_status VARCHAR(20) NOT NULL,
    rejection_probability DECIMAL(5,2),
    acceptance_probability DECIMAL(5,2),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    predicted_by INTEGER REFERENCES users(user_id),
    model_version VARCHAR(20) DEFAULT '1.0'
);

-- Recommendations table
CREATE TABLE recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    issue_description TEXT,
    action_plan TEXT,
    expected_impact VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    implemented_date TIMESTAMP,
    created_by INTEGER REFERENCES users(user_id)
);

-- Create indexes for better performance
CREATE INDEX idx_batches_created_at ON batches(created_at);
CREATE INDEX idx_batches_shift ON batches(shift);
CREATE INDEX idx_batches_status ON batches(actual_status);
CREATE INDEX idx_predictions_batch ON predictions(batch_id);
CREATE INDEX idx_predictions_date ON predictions(prediction_date);
CREATE INDEX idx_recommendations_priority ON recommendations(priority);
CREATE INDEX idx_recommendations_status ON recommendations(status);

-- Insert sample users
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@factory.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztK8TjVuS5f6', 'admin'),
('operator1', 'operator1@factory.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztK8TjVuS5f6', 'operator'),
('supervisor', 'supervisor@factory.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztK8TjVuS5f6', 'supervisor');
-- Default password for all: 'password123'

-- Insert sample batch data
INSERT INTO batches (
    batch_number, machine_temperature, operator_experience_years, 
    production_speed, raw_material_quality, maintenance_hours, 
    shift, humidity_percent, machine_age_years, 
    inspection_thoroughness, supplier_rating, defect_history_count,
    actual_status, created_by
) VALUES
('BATCH-001', 75.5, 12, 98.5, 92.0, 6.5, 'Morning', 45.0, 5, 85.0, 8.5, 1, 'accepted', 1),
('BATCH-002', 82.3, 8, 105.2, 78.0, 3.2, 'Night', 52.0, 11, 72.0, 6.8, 5, 'rejected', 2),
('BATCH-003', 73.8, 15, 95.0, 95.5, 8.0, 'Morning', 43.0, 3, 90.0, 9.2, 0, 'accepted', 1),
('BATCH-004', 88.5, 5, 112.0, 68.0, 2.5, 'Afternoon', 58.0, 13, 65.0, 5.5, 8, 'rejected', 2),
('BATCH-005', 76.0, 10, 100.0, 88.0, 5.5, 'Morning', 46.0, 6, 82.0, 8.0, 2, 'accepted', 1);

-- Insert sample predictions
INSERT INTO predictions (batch_id, predicted_status, rejection_probability, acceptance_probability, predicted_by) VALUES
(1, 'accepted', 15.5, 84.5, 1),
(2, 'rejected', 78.2, 21.8, 1),
(3, 'accepted', 8.3, 91.7, 1),
(4, 'rejected', 85.6, 14.4, 1),
(5, 'accepted', 22.1, 77.9, 1);

-- Insert sample recommendations
INSERT INTO recommendations (category, priority, title, issue_description, action_plan, expected_impact, created_by) VALUES
('Raw Materials', 'HIGH', 'Improve Material Quality Control', 
 'Rejected batches have 76.1% avg quality vs 91.0% for accepted batches',
 'Set minimum quality threshold at 85% and implement quarterly supplier audits',
 '15-20% reduction in rejection rates', 1),
 
('Training', 'HIGH', 'Operator Training Program',
 'Operators on rejected batches have 10.1 years vs 12.3 years for accepted',
 'Implement mentorship program pairing new operators with veterans (10+ years)',
 '10-15% reduction in rejection rates', 1),
 
('Equipment', 'MEDIUM', 'Temperature Control Systems',
 'Temperature variance too high (±10.3°C)',
 'Install automated temperature control systems with ±2°C tolerance',
 '8-12% reduction in rejection rates', 1),
 
('Maintenance', 'HIGH', 'Preventive Maintenance Schedule',
 'Machines on rejected batches receive less maintenance',
 'Schedule preventive maintenance every 200 production hours minimum',
 '12-18% reduction in rejection rates', 1);

-- Create view for batch statistics
CREATE OR REPLACE VIEW batch_statistics AS
SELECT 
    COUNT(*) as total_batches,
    COUNT(CASE WHEN actual_status = 'rejected' THEN 1 END) as rejected_count,
    COUNT(CASE WHEN actual_status = 'accepted' THEN 1 END) as accepted_count,
    ROUND(COUNT(CASE WHEN actual_status = 'rejected' THEN 1 END)::NUMERIC / COUNT(*)::NUMERIC * 100, 2) as rejection_rate,
    ROUND(AVG(machine_temperature), 2) as avg_temperature,
    ROUND(AVG(raw_material_quality), 2) as avg_material_quality,
    ROUND(AVG(operator_experience_years), 2) as avg_operator_experience
FROM batches;

-- Create view for prediction accuracy
CREATE OR REPLACE VIEW prediction_accuracy AS
SELECT 
    COUNT(*) as total_predictions,
    COUNT(CASE WHEN b.actual_status = p.predicted_status THEN 1 END) as correct_predictions,
    ROUND(COUNT(CASE WHEN b.actual_status = p.predicted_status THEN 1 END)::NUMERIC / COUNT(*)::NUMERIC * 100, 2) as accuracy_percentage
FROM predictions p
JOIN batches b ON p.batch_id = b.batch_id
WHERE b.actual_status IS NOT NULL;

-- Create view for shift analysis
CREATE OR REPLACE VIEW shift_analysis AS
SELECT 
    shift,
    COUNT(*) as total_batches,
    COUNT(CASE WHEN actual_status = 'rejected' THEN 1 END) as rejected_count,
    ROUND(COUNT(CASE WHEN actual_status = 'rejected' THEN 1 END)::NUMERIC / COUNT(*)::NUMERIC * 100, 2) as rejection_rate
FROM batches
WHERE shift IS NOT NULL
GROUP BY shift
ORDER BY rejection_rate DESC;

-- Grant permissions (adjust as needed)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_user;

COMMIT;

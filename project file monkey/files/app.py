from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.batch_model import BatchModel
from models.prediction_model import PredictionModel
from models.recommendation_model import RecommendationModel
from models.user_model import UserModel
from database import db
import logging

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =====================================================
# AUTHENTICATION ENDPOINTS
# =====================================================

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = UserModel.authenticate_user(username, password)
        
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@app.route('/api/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user_id = UserModel.create_user(data)
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': str(e)}), 500

# =====================================================
# BATCH ENDPOINTS
# =====================================================

@app.route('/api/batches', methods=['GET'])
def get_batches():
    """Get all batches with pagination"""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        batches = BatchModel.get_all_batches(limit, offset)
        
        return jsonify({
            'success': True,
            'data': batches,
            'count': len(batches)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching batches: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batches/<int:batch_id>', methods=['GET'])
def get_batch(batch_id):
    """Get specific batch by ID"""
    try:
        batch = BatchModel.get_batch_by_id(batch_id)
        
        if batch:
            return jsonify({
                'success': True,
                'data': batch
            }), 200
        else:
            return jsonify({'error': 'Batch not found'}), 404
            
    except Exception as e:
        logger.error(f"Error fetching batch: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batches', methods=['POST'])
def create_batch():
    """Create a new batch"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['batch_number', 'machine_temperature', 'operator_experience_years',
                          'production_speed', 'raw_material_quality', 'maintenance_hours',
                          'shift', 'humidity_percent', 'machine_age_years',
                          'inspection_thoroughness', 'supplier_rating', 'defect_history_count']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        batch_id = BatchModel.create_batch(data)
        
        return jsonify({
            'success': True,
            'message': 'Batch created successfully',
            'batch_id': batch_id
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating batch: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batches/<int:batch_id>/status', methods=['PUT'])
def update_batch_status(batch_id):
    """Update batch status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'error': 'Status required'}), 400
        
        success = BatchModel.update_batch_status(batch_id, status)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Batch status updated'
            }), 200
        else:
            return jsonify({'error': 'Batch not found'}), 404
            
    except Exception as e:
        logger.error(f"Error updating batch: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batches/<int:batch_id>', methods=['DELETE'])
def delete_batch(batch_id):
    """Delete a batch"""
    try:
        success = BatchModel.delete_batch(batch_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Batch deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Batch not found'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting batch: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batches/search', methods=['GET'])
def search_batches():
    """Search batches by batch number"""
    try:
        search_term = request.args.get('q', '')
        limit = request.args.get('limit', 50, type=int)
        
        batches = BatchModel.search_batches(search_term, limit)
        
        return jsonify({
            'success': True,
            'data': batches,
            'count': len(batches)
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching batches: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batches/status/<status>', methods=['GET'])
def get_batches_by_status(status):
    """Get batches by status"""
    try:
        limit = request.args.get('limit', 100, type=int)
        batches = BatchModel.get_batches_by_status(status, limit)
        
        return jsonify({
            'success': True,
            'data': batches,
            'count': len(batches)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching batches by status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batches/shift/<shift>', methods=['GET'])
def get_batches_by_shift(shift):
    """Get batches by shift"""
    try:
        limit = request.args.get('limit', 100, type=int)
        batches = BatchModel.get_batches_by_shift(shift, limit)
        
        return jsonify({
            'success': True,
            'data': batches,
            'count': len(batches)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching batches by shift: {e}")
        return jsonify({'error': str(e)}), 500

# =====================================================
# PREDICTION ENDPOINTS
# =====================================================

@app.route('/api/predict', methods=['POST'])
def predict_rejection():
    """Predict rejection for a batch"""
    try:
        data = request.get_json()
        
        # Make prediction
        prediction = PredictionModel.predict_rejection(data)
        
        # If batch_id provided, save to database
        if 'batch_id' in data:
            user_id = session.get('user_id', 1)
            PredictionModel.create_prediction(
                data['batch_id'], 
                prediction, 
                user_id
            )
        
        return jsonify({
            'success': True,
            'prediction': prediction
        }), 200
        
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """Get all predictions"""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        predictions = PredictionModel.get_all_predictions(limit, offset)
        
        return jsonify({
            'success': True,
            'data': predictions,
            'count': len(predictions)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching predictions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    """Get specific prediction"""
    try:
        prediction = PredictionModel.get_prediction_by_id(prediction_id)
        
        if prediction:
            return jsonify({
                'success': True,
                'data': prediction
            }), 200
        else:
            return jsonify({'error': 'Prediction not found'}), 404
            
    except Exception as e:
        logger.error(f"Error fetching prediction: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions/batch/<int:batch_id>', methods=['GET'])
def get_batch_predictions(batch_id):
    """Get all predictions for a batch"""
    try:
        predictions = PredictionModel.get_predictions_by_batch(batch_id)
        
        return jsonify({
            'success': True,
            'data': predictions,
            'count': len(predictions)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching batch predictions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions/recent', methods=['GET'])
def get_recent_predictions():
    """Get recent predictions"""
    try:
        limit = request.args.get('limit', 10, type=int)
        predictions = PredictionModel.get_recent_predictions(limit)
        
        return jsonify({
            'success': True,
            'data': predictions,
            'count': len(predictions)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching recent predictions: {e}")
        return jsonify({'error': str(e)}), 500

# =====================================================
# RECOMMENDATION ENDPOINTS
# =====================================================

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get all recommendations"""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        recommendations = RecommendationModel.get_all_recommendations(limit, offset)
        
        return jsonify({
            'success': True,
            'data': recommendations,
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/<int:rec_id>', methods=['GET'])
def get_recommendation(rec_id):
    """Get specific recommendation"""
    try:
        recommendation = RecommendationModel.get_recommendation_by_id(rec_id)
        
        if recommendation:
            return jsonify({
                'success': True,
                'data': recommendation
            }), 200
        else:
            return jsonify({'error': 'Recommendation not found'}), 404
            
    except Exception as e:
        logger.error(f"Error fetching recommendation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations', methods=['POST'])
def create_recommendation():
    """Create a new recommendation"""
    try:
        data = request.get_json()
        user_id = session.get('user_id', 1)
        data['created_by'] = user_id
        
        rec_id = RecommendationModel.create_recommendation(data)
        
        return jsonify({
            'success': True,
            'message': 'Recommendation created successfully',
            'recommendation_id': rec_id
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating recommendation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/<int:rec_id>/status', methods=['PUT'])
def update_recommendation_status(rec_id):
    """Update recommendation status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'error': 'Status required'}), 400
        
        success = RecommendationModel.update_recommendation_status(rec_id, status)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Recommendation status updated'
            }), 200
        else:
            return jsonify({'error': 'Recommendation not found'}), 404
            
    except Exception as e:
        logger.error(f"Error updating recommendation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/priority/<priority>', methods=['GET'])
def get_recommendations_by_priority(priority):
    """Get recommendations by priority"""
    try:
        limit = request.args.get('limit', 50, type=int)
        recommendations = RecommendationModel.get_recommendations_by_priority(priority, limit)
        
        return jsonify({
            'success': True,
            'data': recommendations,
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        return jsonify({'error': str(e)}), 500

# =====================================================
# STATISTICS ENDPOINTS
# =====================================================

@app.route('/api/statistics/batches', methods=['GET'])
def get_batch_statistics():
    """Get batch statistics"""
    try:
        stats = BatchModel.get_batch_statistics()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics/shift-analysis', methods=['GET'])
def get_shift_analysis():
    """Get shift analysis"""
    try:
        analysis = BatchModel.get_shift_analysis()
        
        return jsonify({
            'success': True,
            'data': analysis
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching shift analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics/prediction-accuracy', methods=['GET'])
def get_prediction_accuracy():
    """Get prediction accuracy statistics"""
    try:
        accuracy = PredictionModel.get_prediction_accuracy()
        
        return jsonify({
            'success': True,
            'data': accuracy
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching prediction accuracy: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics/recommendations-summary', methods=['GET'])
def get_recommendations_summary():
    """Get recommendations summary"""
    try:
        summary = RecommendationModel.get_recommendations_summary()
        
        return jsonify({
            'success': True,
            'data': summary
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching recommendations summary: {e}")
        return jsonify({'error': str(e)}), 500

# =====================================================
# HEALTH CHECK
# =====================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Rejection Analytics API',
        'version': '1.0'
    }), 200

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Rejection Analytics API',
        'version': '1.0',
        'endpoints': {
            'authentication': '/api/login, /api/logout, /api/register',
            'batches': '/api/batches',
            'predictions': '/api/predictions, /api/predict',
            'recommendations': '/api/recommendations',
            'statistics': '/api/statistics/*'
        }
    }), 200

# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# =====================================================
# RUN SERVER
# =====================================================

if __name__ == '__main__':
    logger.info("🚀 Starting Rejection Analytics Backend Server...")
    logger.info("📊 API Documentation: http://localhost:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)

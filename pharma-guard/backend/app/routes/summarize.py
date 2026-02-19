"""
PharmaGuard Summarize Route
"""
from flask import Blueprint, request, jsonify
from app.services.ai_service import AIService
from app.services.integrity_service import IntegrityService

summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route('/', methods=['POST'])
def summarize_product():
    """
    Summarize product information using AI
    
    Request body:
    {
        "product_name": str,
        "product_category": str,
        "batch_number": str,
        "serial_number": str,
        "manufacture_date": str,
        "expiry_date": str,
        "additional_info": str (optional)
    }
    
    Returns:
    {
        "summary": str,
        "compliance_check": dict,
        "risk_assessment": dict
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract product information
        product_info = {
            'product_name': data.get('product_name'),
            'product_category': data.get('product_category'),
            'batch_number': data.get('batch_number'),
            'serial_number': data.get('serial_number'),
            'manufacture_date': data.get('manufacture_date'),
            'expiry_date': data.get('expiry_date'),
            'additional_info': data.get('additional_info', '')
        }
        
        # Validate required fields
        required_fields = ['product_name', 'product_category', 'batch_number']
        missing_fields = [field for field in required_fields if not product_info.get(field)]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Generate AI summary
        ai_service = AIService()
        summary = ai_service.summarize_product(product_info)
        
        # Perform integrity check
        integrity_service = IntegrityService()
        integrity_result = integrity_service.verify_product_integrity(product_info)
        
        # Generate compliance check
        compliance_check = ai_service.check_compliance(product_info)
        
        # Generate risk assessment
        risk_assessment = ai_service.assess_risk(product_info)
        
        return jsonify({
            'summary': summary,
            'integrity_check': integrity_result,
            'compliance_check': compliance_check,
            'risk_assessment': risk_assessment
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@summarize_bp.route('/batch', methods=['POST'])
def summarize_batch():
    """
    Summarize multiple products at once
    
    Request body:
    {
        "products": [
            { product_info 1 },
            { product info 2 }
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'products' not in data:
            return jsonify({'error': 'No products provided'}), 400
        
        products = data['products']
        
        if not isinstance(products, list):
            return jsonify({'error': 'Products must be a list'}), 400
        
        results = []
        ai_service = AIService()
        integrity_service = IntegrityService()
        
        for product in products:
            summary = ai_service.summarize_product(product)
            integrity_result = integrity_service.verify_product_integrity(product)
            
            results.append({
                'product': product,
                'summary': summary,
                'integrity_check': integrity_result
            })
        
        return jsonify({
            'results': results,
            'total_processed': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@summarize_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for summarize service"""
    return jsonify({
        'status': 'healthy',
        'service': 'summarize'
    }), 200

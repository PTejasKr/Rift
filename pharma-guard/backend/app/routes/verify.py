"""
PharmaGuard Verification Route
"""
from flask import Blueprint, request, jsonify
from app.services.blockchain_service import BlockchainService
from app.services.integrity_service import IntegrityService
from app.services.signer import Signer
from app.database import get_db_context
from app.models import Product, Verification
import uuid

verify_bp = Blueprint('verify', __name__)

@verify_bp.route('/product', methods=['POST'])
def verify_product():
    """
    Verify product authenticity using blockchain and merkle tree
    
    Request body:
    {
        "serial_number": str,
        "qr_token": str (optional),
        "user_wallet_address": str (optional)
    }
    
    Returns:
    {
        "verified": bool,
        "product_info": dict,
        "verification_details": dict,
        "blockchain_status": dict,
        "integrity_status": dict
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        serial_number = data.get('serial_number')
        qr_token = data.get('qr_token')
        user_wallet_address = data.get('user_wallet_address')
        
        if not serial_number and not qr_token:
            return jsonify({
                'error': 'Either serial_number or qr_token is required'
            }), 400
        
        # Get product from database
        with get_db_context() as db:
            product = None
            if serial_number:
                product = db.query(Product).filter_by(serial_number=serial_number).first()
            elif qr_token:
                product = db.query(Product).filter_by(qr_token=qr_token).first()
            
            if not product:
                return jsonify({
                    'verified': False,
                    'error': 'Product not found'
                }), 404
            
            product_info = product.to_dict()
            
            # Verify using blockchain
            blockchain_service = BlockchainService()
            blockchain_status = blockchain_service.verify_on_blockchain(
                product.merkle_root,
                product.blockchain_txn_hash
            )
            
            # Verify using merkle tree
            integrity_service = IntegrityService()
            integrity_status = integrity_service.verify_merkle_proof(
                product.merkle_root,
                data.get('merkle_proof')
            )
            
            # Log verification
            verification = Verification(
                product_id=product.id,
                user_wallet_address=user_wallet_address,
                verification_status='success' if (blockchain_status.get('verified') and integrity_status.get('verified')) else 'failed',
                verification_method='blockchain_merkle',
                txn_hash=str(uuid.uuid4())
            )
            db.add(verification)
            
            return jsonify({
                'verified': blockchain_status.get('verified') and integrity_status.get('verified'),
                'product_info': product_info,
                'verification_details': {
                    'verification_id': verification.id,
                    'timestamp': verification.verification_timestamp.isoformat()
                },
                'blockchain_status': blockchain_status,
                'integrity_status': integrity_status
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@verify_bp.route('/blockchain', methods=['POST'])
def verify_blockchain():
    """
    Verify product on blockchain only
    
    Request body:
    {
        "merkle_root": str,
        "txn_hash": str
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        merkle_root = data.get('merkle_root')
        txn_hash = data.get('txn_hash')
        
        if not merkle_root or not txn_hash:
            return jsonify({
                'error': 'merkle_root and txn_hash are required'
            }), 400
        
        blockchain_service = BlockchainService()
        result = blockchain_service.verify_on_blockchain(merkle_root, txn_hash)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@verify_bp.route('/signature', methods=['POST'])
def verify_signature():
    """
    Verify cryptographic signature
    
    Request body:
    {
        "data": str,
        "signature": str,
        "public_key": str
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        message = data.get('data')
        signature = data.get('signature')
        public_key = data.get('public_key')
        
        if not all([message, signature, public_key]):
            return jsonify({
                'error': 'data, signature, and public_key are required'
            }), 400
        
        signer = Signer()
        is_valid = signer.verify_signature(message, signature, public_key)
        
        return jsonify({
            'valid': is_valid,
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@verify_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for verify service"""
    return jsonify({
        'status': 'healthy',
        'service': 'verify'
    }), 200

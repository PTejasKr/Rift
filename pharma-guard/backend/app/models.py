"""
PharmaGuard Database Models
"""
from datetime import datetime
from app.main import db

class Organization(db.Model):
    """Organization model for pharmaceutical companies"""
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    org_name = db.Column(db.String(255), nullable=False)
    org_category = db.Column(db.String(100))
    org_wallet_address = db.Column(db.String(100), unique=True)
    branding_color = db.Column(db.String(20), default='#000000')
    logo_url = db.Column(db.String(500))
    
    # Relationships
    users = db.relationship('User', backref='organization', lazy='dynamic')
    products = db.relationship('Product', backref='organization', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'org_name': self.org_name,
            'org_category': self.org_category,
            'org_wallet_address': self.org_wallet_address,
            'branding_color': self.branding_color,
            'logo_url': self.logo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class User(db.Model):
    """User model with RBAC"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    user_role = db.Column(db.String(50), default='manager')
    wallet_address = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'user_role': self.user_role,
            'org_id': self.org_id,
            'wallet_address': self.wallet_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    """Product model for pharmaceutical items"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    product_category = db.Column(db.String(100))
    batch_number = db.Column(db.String(100))
    serial_number = db.Column(db.String(100), unique=True)
    manufacture_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    qr_token = db.Column(db.String(255), unique=True)
    merkle_root = db.Column(db.String(255))
    blockchain_txn_hash = db.Column(db.String(100))
    
    # Relationships
    verifications = db.relationship('Verification', backref='product', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'product_category': self.product_category,
            'batch_number': self.batch_number,
            'serial_number': self.serial_number,
            'manufacture_date': self.manufacture_date.isoformat() if self.manufacture_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'qr_token': self.qr_token,
            'merkle_root': self.merkle_root,
            'blockchain_txn_hash': self.blockchain_txn_hash,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Verification(db.Model):
    """Verification log model"""
    __tablename__ = 'verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_wallet_address = db.Column(db.String(100))
    verification_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    txn_hash = db.Column(db.String(100), unique=True)
    verification_status = db.Column(db.String(50), default='success')
    verification_method = db.Column(db.String(50))  # 'blockchain', 'merkle', 'ai'
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_wallet_address': self.user_wallet_address,
            'verification_timestamp': self.verification_timestamp.isoformat() if self.verification_timestamp else None,
            'txn_hash': self.txn_hash,
            'verification_status': self.verification_status,
            'verification_method': self.verification_method
        }

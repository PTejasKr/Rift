"""
PharmaGuard Cryptographic Signer
"""
import os
import hashlib
import hmac
import base64
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

class Signer:
    """Service for cryptographic signing and verification of product data"""
    
    def __init__(self):
        self.algorithm = 'ECDSA'
        self.curve = ec.SECP256R1()
    
    def generate_key_pair(self):
        """
        Generate a new ECDSA key pair
        
        Returns:
            tuple: (private_key_pem, public_key_pem)
        """
        private_key = ec.generate_private_key(self.curve, default_backend())
        public_key = private_key.public_key()
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem.decode('utf-8'), public_pem.decode('utf-8')
    
    def sign(self, data, private_key_pem=None):
        """
        Sign data with ECDSA
        
        Args:
            data: Data to sign (will be hashed)
            private_key_pem: Optional private key in PEM format
            
        Returns:
            tuple: (signature, public_key)
        """
        # Generate key pair if not provided
        if not private_key_pem:
            private_pem, public_pem = self.generate_key_pair()
        else:
            private_pem = private_key_pem
            public_pem = None
        
        # Load private key
        private_key = serialization.load_pem_private_key(
            private_pem.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        
        # Generate public key if not returned
        if not public_pem:
            public_key = private_key.public_key()
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
        
        # Hash the data
        if isinstance(data, str):
            data = data.encode('utf-8')
        data_hash = hashlib.sha256(data).digest()
        
        # Sign the hash
        signature = private_key.sign(data_hash, ec.ECDSA(hashes.SHA256()))
        
        # Encode signature to base64
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        return signature_b64, public_pem
    
    def verify_signature(self, data, signature_b64, public_key_pem):
        """
        Verify an ECDSA signature
        
        Args:
            data: The original data that was signed
            signature_b64: Base64 encoded signature
            public_key_pem: Public key in PEM format
            
        Returns:
            bool: True if signature is valid
        """
        try:
            # Load public key
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode('utf-8'),
                backend=default_backend()
            )
            
            # Decode signature from base64
            signature = base64.b64decode(signature_b64.encode('utf-8'))
            
            # Hash the data
            if isinstance(data, str):
                data = data.encode('utf-8')
            data_hash = hashlib.sha256(data).digest()
            
            # Verify signature
            public_key.verify(signature, data_hash, ec.ECDSA(hashes.SHA256()))
            
            return True
            
        except Exception as e:
            return False
    
    def create_hmac(self, data, secret_key=None):
        """
        Create HMAC signature
        
        Args:
            data: Data to sign
            secret_key: Secret key for HMAC (generated if not provided)
            
        Returns:
            tuple: (hmac_signature, secret_key)
        """
        if not secret_key:
            secret_key = os.urandom(32)
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        signature = hmac.new(secret_key, data, hashlib.sha256).digest()
        
        return base64.b64encode(signature).decode('utf-8'), base64.b64encode(secret_key).decode('utf-8')
    
    def verify_hmac(self, data, signature_b64, secret_key_b64):
        """
        Verify HMAC signature
        
        Args:
            data: Original data
            signature_b64: Base64 encoded HMAC signature
            secret_key_b64: Base64 encoded secret key
            
        Returns:
            bool: True if HMAC is valid
        """
        try:
            secret_key = base64.b64decode(secret_key_b64.encode('utf-8'))
            signature = base64.b64decode(signature_b64.encode('utf-8'))
            
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            expected_signature = hmac.new(secret_key, data, hashlib.sha256).digest()
            
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception:
            return False
    
    def hash_data(self, data, algorithm='sha256'):
        """
        Hash data using specified algorithm
        
        Args:
            data: Data to hash
            algorithm: Hash algorithm (sha256, sha512, etc.)
            
        Returns:
            str: Hexadecimal hash string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if algorithm == 'sha256':
            return hashlib.sha256(data).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(data).hexdigest()
        elif algorithm == 'blake2b':
            return hashlib.blake2b(data).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    def verify_hash(self, data, hash_value, algorithm='sha256'):
        """
        Verify data against a hash
        
        Args:
            data: Data to verify
            hash_value: Expected hash value
            algorithm: Hash algorithm used
            
        Returns:
            bool: True if hash matches
        """
        computed_hash = self.hash_data(data, algorithm)
        return hmac.compare_digest(computed_hash, hash_value)

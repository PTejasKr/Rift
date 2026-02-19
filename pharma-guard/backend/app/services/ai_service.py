"""
PharmaGuard AI Service
"""
import os
import json
from datetime import datetime, timedelta

class AIService:
    """Service for AI-powered product analysis and summarization"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.ai_model = os.getenv('AI_MODEL', 'gpt-4')
    
    def summarize_product(self, product_info):
        """
        Generate AI-powered summary of product information
        
        Args:
            product_info: Dictionary containing product details
            
        Returns:
            str: AI-generated summary
        """
        # In production, this would call OpenAI or Anthropic API
        # For now, we'll generate a summary based on the product info
        
        summary_parts = []
        
        if product_info.get('product_name'):
            summary_parts.append(f"Product: {product_info['product_name']}")
        
        if product_info.get('product_category'):
            summary_parts.append(f"Category: {product_info['product_category']}")
        
        if product_info.get('batch_number'):
            summary_parts.append(f"Batch: {product_info['batch_number']}")
        
        if product_info.get('serial_number'):
            summary_parts.append(f"Serial: {product_info['serial_number']}")
        
        if product_info.get('manufacture_date'):
            summary_parts.append(f"Manufactured: {product_info['manufacture_date']}")
        
        if product_info.get('expiry_date'):
            summary_parts.append(f"Expires: {product_info['expiry_date']}")
        
        if product_info.get('additional_info'):
            summary_parts.append(f"Additional Info: {product_info['additional_info']}")
        
        # Generate compliance notes
        compliance_notes = self._generate_compliance_notes(product_info)
        
        summary = " | ".join(summary_parts)
        summary += f"\n\nCompliance Status: {compliance_notes['status']}"
        summary += f"\nNotes: {compliance_notes['notes']}"
        
        return summary
    
    def check_compliance(self, product_info):
        """
        Check product against regulatory compliance requirements
        
        Args:
            product_info: Dictionary containing product details
            
        Returns:
            dict: Compliance check results
        """
        compliance_result = {
            'status': 'compliant',
            'checks': [],
            'warnings': [],
            'violations': []
        }
        
        # Check expiry date
        if product_info.get('expiry_date'):
            try:
                expiry = datetime.strptime(product_info['expiry_date'], '%Y-%m-%d')
                if expiry < datetime.now():
                    compliance_result['violations'].append('Product has expired')
                    compliance_result['status'] = 'non-compliant'
                elif expiry < datetime.now() + timedelta(days=90):
                    compliance_result['warnings'].append('Product expires within 90 days')
            except ValueError:
                compliance_result['warnings'].append('Invalid expiry date format')
        
        # Check manufacture date
        if product_info.get('manufacture_date'):
            try:
                manufacture = datetime.strptime(product_info['manufacture_date'], '%Y-%m-%d')
                if manufacture > datetime.now():
                    compliance_result['violations'].append('Manufacture date is in the future')
                    compliance_result['status'] = 'non-compliant'
            except ValueError:
                compliance_result['warnings'].append('Invalid manufacture date format')
        
        # Check required fields
        required = ['product_name', 'product_category', 'batch_number', 'serial_number']
        for field in required:
            if not product_info.get(field):
                compliance_result['violations'].append(f'Missing required field: {field}')
                compliance_result['status'] = 'non-compliant'
        
        # Add standard checks
        compliance_result['checks'].append({
            'name': 'Required Fields',
            'status': 'passed' if not compliance_result['violations'] else 'failed'
        })
        
        compliance_result['checks'].append({
            'name': 'Date Validation',
            'status': 'passed' if not compliance_result['violations'] else 'failed'
        })
        
        return compliance_result
    
    def assess_risk(self, product_info):
        """
        Assess risk level of the product
        
        Args:
            product_info: Dictionary containing product details
            
        Returns:
            dict: Risk assessment results
        """
        risk_assessment = {
            'risk_level': 'low',
            'risk_factors': [],
            'recommendations': []
        }
        
        # Check expiry
        if product_info.get('expiry_date'):
            try:
                expiry = datetime.strptime(product_info['expiry_date'], '%Y-%m-%d')
                days_until_expiry = (expiry - datetime.now()).days
                
                if days_until_expiry < 0:
                    risk_assessment['risk_factors'].append('Product is expired')
                    risk_assessment['risk_level'] = 'high'
                    risk_assessment['recommendations'].append('Do not use - product has expired')
                elif days_until_expiry < 30:
                    risk_assessment['risk_factors'].append('Product expires within 30 days')
                    risk_assessment['risk_level'] = 'medium'
                    risk_assessment['recommendations'].append('Use before expiration')
                elif days_until_expiry < 90:
                    risk_assessment['risk_factors'].append('Product expires within 90 days')
                    if risk_assessment['risk_level'] != 'medium':
                        risk_assessment['risk_level'] = 'low-medium'
            except ValueError:
                risk_assessment['risk_factors'].append('Invalid expiry date')
                risk_assessment['risk_level'] = 'medium'
        
        # Check product category for high-risk products
        high_risk_categories = ['vaccines', 'biologics', 'controlled substances']
        category = product_info.get('product_category', '').lower()
        
        if any(cat in category for cat in high_risk_categories):
            risk_assessment['risk_factors'].append(f'High-risk category: {category}')
            risk_assessment['risk_level'] = 'high' if risk_assessment['risk_level'] == 'low' else risk_assessment['risk_level']
            risk_assessment['recommendations'].append('Enhanced verification required')
        
        # Add general recommendations
        if risk_assessment['risk_level'] == 'low':
            risk_assessment['recommendations'].append('Standard verification procedures apply')
        
        return risk_assessment
    
    def _generate_compliance_notes(self, product_info):
        """Generate compliance notes based on product info"""
        notes = []
        status = 'compliant'
        
        if product_info.get('expiry_date'):
            try:
                expiry = datetime.strptime(product_info['expiry_date'], '%Y-%m-%d')
                if expiry < datetime.now():
                    notes.append('EXPIRED PRODUCT - DO NOT USE')
                    status = 'non-compliant'
                elif expiry < datetime.now() + timedelta(days=90):
                    notes.append('Expiring soon - verify before use')
            except ValueError:
                notes.append('Check expiration date format')
        
        if product_info.get('product_category'):
            category = product_info['product_category'].lower()
            if 'temperature' in category or 'cold' in category:
                notes.append('Temperature-sensitive - verify cold chain')
        
        return {
            'status': status,
            'notes': '; '.join(notes) if notes else 'All checks passed'
        }

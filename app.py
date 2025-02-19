from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse
import ssl
import socket
import whois
import datetime
import ipaddress
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_domain_age(domain):
    """
    Comprehensive domain age check with detailed error handling
    """
    try:
        domain_info = whois.whois(domain)
        
        # Extract creation date with multiple fallback strategies
        creation_date = None
        if hasattr(domain_info, 'creation_date'):
            if isinstance(domain_info.creation_date, list):
                creation_date = domain_info.creation_date[0]
            elif isinstance(domain_info.creation_date, datetime.datetime):
                creation_date = domain_info.creation_date
        
        # Check for alternative date fields
        if not creation_date:
            date_fields = ['created', 'creation', 'registered', 'reg_date']
            for field in date_fields:
                if hasattr(domain_info, field):
                    date_value = getattr(domain_info, field)
                    if isinstance(date_value, (datetime.datetime, list)):
                        creation_date = date_value[0] if isinstance(date_value, list) else date_value
                        break
        
        if creation_date:
            age = (datetime.datetime.now() - creation_date).days
            return {
                'age_days': age,
                'creation_date': creation_date.strftime('%Y-%m-%d'),
                'registrar': domain_info.registrar or 'Unknown'
            }
        
        return None
    except Exception as e:
        logger.error(f"Unexpected error in domain age check: {e}")
        return None

def verify_ssl_certificate(domain):
    """
    Enhanced SSL certificate verification with detailed checks
    """
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                cert = secure_sock.getpeercert()
                
                # Extract certificate details
                return {
                    'is_valid': True,
                    'subject': dict(x[0] for x in cert['subject']),
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'expiration': datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                }
    except ssl.SSLCertVerificationError as e:
        logger.warning(f"SSL Certificate Verification Error: {e}")
        return {'is_valid': False, 'error': str(e)}
    except socket.timeout:
        logger.warning(f"SSL connection timeout for {domain}")
        return {'is_valid': False, 'error': 'Connection Timeout'}
    except Exception as e:
        logger.error(f"Unexpected SSL verification error: {e}")
        return {'is_valid': False, 'error': 'Verification Failed'}

def is_ip_address(domain):
    """
    Check if the domain is an IP address
    """
    try:
        ipaddress.ip_address(domain)
        return True
    except ValueError:
        return False

def analyze_url(url):
    """
    Comprehensive URL analysis with multiple risk checks
    """
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.split(':')[0]
        
        # Skip analysis for IP addresses
        if is_ip_address(domain):
            return {
                'is_fake': True,
                'message': 'IP Address Detection',
                'details': 'Direct IP address URLs are suspicious'
            }

        # Risk assessment dictionary
        risks = []
        is_fake = False

        # Domain age check
        domain_age_info = check_domain_age(domain)
        if domain_age_info:
            if domain_age_info['age_days'] < 180:
                risks.append(f"Recently registered domain (Age: {domain_age_info['age_days']} days)")
                is_fake = True
            
        # SSL verification
        ssl_result = verify_ssl_certificate(domain)
        if not ssl_result['is_valid']:
            risks.append(f"Invalid SSL Certificate: {ssl_result.get('error', 'Unknown Error')}")
            is_fake = True

        # Suspicious keywords
        suspicious_keywords = ['clone', 'fake', 'mirror', 'replica', 'test', 'mock']
        if any(keyword in url.lower() for keyword in suspicious_keywords):
            risks.append("Suspicious URL keywords detected")
            is_fake = True

        # Prepare result
        return {
            'is_fake': is_fake,
            'message': "App Authenticity" if not is_fake else "Potential Fake App Detected",
            'details': f"Risks identified: {', '.join(risks)}" if risks else "No immediate risks found",
            'domain_info': {
                'domain': domain,
                'age_info': domain_age_info
            }
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in URL analysis: {e}")
        return {
            'is_fake': True, 
            'message': 'Analysis Error', 
            'details': f'Unexpected error during URL verification: {e}'
        }

@app.route('/check_app', methods=['POST'])
def check_app():
    """
    Flask route for app URL verification
    """
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'is_fake': True, 
                'message': 'Invalid URL', 
                'details': 'No URL provided for verification'
            }), 400

        # Validate URL format
        try:
            parsed_url = urllib.parse.urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
        except Exception:
            return jsonify({
                'is_fake': True, 
                'message': 'Invalid URL', 
                'details': 'Provided URL is not well-formed'
            }), 400

        result = analyze_url(url)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Server error in check_app route: {e}")
        return jsonify({
            'is_fake': True, 
            'message': 'Server Error', 
            'details': 'An unexpected server error occurred'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
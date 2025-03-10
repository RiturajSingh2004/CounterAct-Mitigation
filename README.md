# CounterAct-Mitigation
## CounterAct-Mitigation (ver2.0)
Flak is replaced with FastAPI, phishing detection API is included, hosted on Render
## CounterAct-Mitigation (ver1.0)
CounterAct Mitigation is a Browser Extension that check the authenticity and detail of current webpage to ensure safety of you and your system.<br>
A robust web application authentication system that helps verify the legitimacy of web applications by analyzing various security parameters. This system combines a Flask backend API with a Chrome extension frontend to provide real-time authenticity checks for web applications.<br>

## 🌟 Key Features<br>

### Security Analysis<br>
- Domain age verification with comprehensive error handling<br>
- SSL certificate validation and detailed certificate information<br>
- IP address detection and validation<br>
- Suspicious keyword detection<br>
- Multi-factor risk assessment<br>

### Technical Implementation<br>
- RESTful API architecture using Flask<br>
- Cross-Origin Resource Sharing (CORS) support<br>
- Comprehensive error handling and logging<br>
- Chrome extension with popup interface<br>
- Dark/Light theme support with persistent settings<br>

### Requirements.txt<br>
Flask==2.1.0<br>
flask-cors==3.0.10<br>
python-whois==0.8.0<br>
urllib3==1.26.8<br>
ipaddress==1.0.23<br>

## 🛠️ Technologies Used<br>

### Backend<br>
- Python 3.x<br>
- Flask framework<br>
- Libraries:<br>
  - `flask-cors`: For handling cross-origin requests<br>
  - `whois`: For domain registration information<br>
  - `ssl`: For certificate validation<br>
  - `socket`: For network operations<br>
  - `logging`: For system monitoring<br>
  - `urllib`: For URL parsing and validation<br>
  - `ipaddress`: For IP address validation<br>

### Frontend (Chrome Extension)<br>
- HTML5<br>
- CSS3<br>
- JavaScript<br>
- Chrome Extension APIs<br>

## 🔧 Installation & Setup<br>

### Backend Setup<br>
1. Install Python dependencies:
```bash
pip install flask flask-cors python-whois
```

2. Start the Flask server:
```bash
python app.py
```
The server will run on `http://localhost:5000`

### Chrome Extension Setup
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the extension directory containing the manifest and frontend files

## 🔍 Features In Detail

### Domain Age Verification
- Checks domain registration date
- Multiple fallback strategies for date extraction
- Age-based risk assessment

### SSL Certificate Validation
- Validates SSL certificate authenticity
- Extracts certificate details including:
  - Subject information
  - Issuer details
  - Expiration date
- Connection timeout handling

### URL Analysis
- Comprehensive URL parsing and validation
- IP address detection
- Suspicious keyword monitoring
- Risk factor aggregation

### User Interface
- Clean and intuitive popup interface
- Real-time loading indicators
- Error messaging system
- Dark/Light theme toggle with local storage persistence
- Detailed results display including:
  - Authentication status
  - Risk detail
  - Domain information
  - Age verification results

## 🔐 Security Measures

- Input validation for all URL submissions
- Error handling for network timeouts
- SSL verification error catching
- Protection against malformed URLs
- Logging system for security monitoring

## 📝 API Endpoints

### POST `/check_app`
Analyzes a provided URL for authenticity.

**Request Body:**
```json
{
    "url": "https://example.com"
}
```

**Response Format:**
```json
{
    "is_fake": boolean,
    "message": string,
    "details": string,
    "domain_info": {
        "domain": string,
        "age_info": {
            "age_days": number,
            "creation_date": string,
            "registrar": string
        }
    }
}
```

## 🚀 Performance Considerations

- Asynchronous API calls
- Efficient error handling
- Minimal DOM manipulation
- Theme preference caching
- Optimized certificate validation

## 📋 Requirements

### Backend
- Python 3.x
- Flask
- Internet connection for WHOIS and SSL verification
- Proper SSL configuration
- Network access for domain queries

### Frontend
- Chrome browser
- JavaScript enabled
- Local storage access
- Network connectivity

## 🤝 Open for Contributing
## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

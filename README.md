# CounterAct-Mitigation
CounterAct Mitigation is a Chrome extension that check the authenticity and detail of current webpage to ensure safety of you and your system.<br>
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
1. Install Python dependencies:<br>
```bash<br>
pip install flask flask-cors python-whois<br>
```<br>

2. Start the Flask server:<br>
```bash<br>
python app.py<br>
```<br>
The server will run on `http://localhost:5000`<br>

### Chrome Extension Setup<br>
1. Open Chrome and navigate to `chrome://extensions/`<br>
2. Enable "Developer mode"<br>
3. Click "Load unpacked"<br>
4. Select the extension directory containing the manifest and frontend files<br>

## 🔍 Features In Detail<br>

### Domain Age Verification<br>
- Checks domain registration date<br>
- Multiple fallback strategies for date extraction<br>
- Age-based risk assessment<br>

### SSL Certificate Validation<br>
- Validates SSL certificate authenticity<br>
- Extracts certificate details including:<br>
  - Subject information<br>
  - Issuer details<br>
  - Expiration date<br>
- Connection timeout handling<br>

### URL Analysis<br>
- Comprehensive URL parsing and validation<br>
- IP address detection<br>
- Suspicious keyword monitoring<br>
- Risk factor aggregation<br>

### User Interface<br>
- Clean and intuitive popup interface<br>
- Real-time loading indicators<br>
- Error messaging system<br>
- Dark/Light theme toggle with local storage persistence<br>
- Detailed results display including:<br>
  - Authentication status<br>
  - Risk details<br>
  - Domain information<br>
  - Age verification results<br>

## 🔐 Security Measures<br>

- Input validation for all URL submissions<br>
- Error handling for network timeouts<br>
- SSL verification error catching<br>
- Protection against malformed URLs<br>
- Logging system for security monitoring<br>

## 📝 API Endpoints<br>

### POST `/check_app`<br>
Analyzes a provided URL for authenticity.<br>

**Request Body:**<br>
```json<br>
{<br>
    "url": "https://example.com"<br>
}<br>
```<br>

**Response Format:**<br>
```json<br>
{<br>
    "is_fake": boolean,<br>
    "message": string,<br>
    "details": string,<br>
    "domain_info": {<br>
        "domain": string,<br>
        "age_info": {<br>
            "age_days": number,<br>
            "creation_date": string,<br>
            "registrar": string<br>
        }<br>
    }<br>
}<br>
```<br>

## 🚀 Performance Considerations<br>

- Asynchronous API calls<br>
- Efficient error handling<br>
- Minimal DOM manipulation<br>
- Theme preference caching<br>
- Optimized certificate validation<br>

## 📋 Requirements<br>

### Backend<br>
- Python 3.x<br>
- Flask<br>
- Internet connection for WHOIS and SSL verification<br>
- Proper SSL configuration<br>
- Network access for domain queries<br>

### Frontend<br>
- Chrome browser<br>
- JavaScript enabled<br>
- Local storage access<br>
- Network connectivity<br>

## 🤝 Open for Contributing<br>
## 📄 License<br>
This project is licensed under the MIT License - see the LICENSE file for details.<br>

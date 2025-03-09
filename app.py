import os
from fastapi import FastAPI, Request
import urllib.parse
import ssl
import socket
import whois
import datetime
import ipaddress
import logging
import aiohttp

app = FastAPI()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def check_domain_age(domain):
    try:
        domain_info = whois.whois(domain)
        creation_date = None
        if hasattr(domain_info, "creation_date"):
            if isinstance(domain_info.creation_date, list):
                creation_date = domain_info.creation_date[0]
            elif isinstance(domain_info.creation_date, datetime.datetime):
                creation_date = domain_info.creation_date
        if not creation_date:
            date_fields = ["created", "creation", "registered", "reg_date"]
            for field in date_fields:
                if hasattr(domain_info, field):
                    date_value = getattr(domain_info, field)
                    if isinstance(date_value, (datetime.datetime, list)):
                        creation_date = (
                            date_value[0]
                            if isinstance(date_value, list)
                            else date_value
                        )
                        break

        if creation_date:
            age = (datetime.datetime.now() - creation_date).days
            return {
                "age_days": age,
                "creation_date": creation_date.strftime("%Y-%m-%d"),
                "registrar": domain_info.registrar or "Unknown",
            }

        return None
    except whois.parser.PywhoisError as e:
        logger.warning(f"WHOIS lookup error for {domain}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in domain age check: {e}")
        return None


def verify_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                cert = secure_sock.getpeercert()
                return {
                    "is_valid": True,
                    "subject": dict(x[0] for x in cert["subject"]),
                    "issuer": dict(x[0] for x in cert["issuer"]),
                    "expiration": datetime.datetime.strptime(
                        cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
                    ),
                }
    except ssl.SSLCertVerificationError as e:
        logger.warning(f"SSL Certificate Verification Error: {e}")
        return {"is_valid": False, "error": str(e)}
    except socket.timeout:
        logger.warning(f"SSL connection timeout for {domain}")
        return {"is_valid": False, "error": "Connection Timeout"}
    except Exception as e:
        logger.error(f"Unexpected SSL verification error: {e}")
        return {"is_valid": False, "error": "Verification Failed"}


def is_ip_address(domain):
    try:
        ipaddress.ip_address(domain)
        return True
    except ValueError:
        return False


async def check_website_legitimacy(domain):
    """
    Check website legitimacy using PhishTank API.
    """
    url = "https://urlscan.io/api/v1/scan/"
    api_key = os.environ["URLSCAN_API_KEY"]
    headers = {
        "Content-Type": "application/json",
        "API-Key": api_key,
    }
    print(domain)
    payload = {
        "url": f"http://{domain}",
        "public": "on",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                print(await response.text())
                response_data = await response.json()
                if response.status == 200:
                    return {
                        "is_legitimate": True,
                        "details": "Domain scan completed successfully",
                        "scan_id": response_data.get("uuid"),
                    }
                else:
                    return {
                        "is_legitimate": False,
                        "details": response_data.get("message", "Unknown error"),
                    }
    except Exception as e:
        logger.error(f"Error checking website legitimacy: {e}")
        return {
            "is_legitimate": False,
            "details": "Error checking website legitimacy",
        }


async def analyze_url(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.split(":")[0]

        if is_ip_address(domain):
            return {
                "is_fake": True,
                "message": "IP Address Detection",
                "details": "Direct IP address URLs are suspicious",
            }

        risks = []
        is_fake = False

        domain_age_info = check_domain_age(domain)
        if domain_age_info:
            if domain_age_info["age_days"] < 180:
                risks.append(
                    f"Recently registered domain (Age: {domain_age_info['age_days']} days)"
                )
                is_fake = True

        ssl_result = verify_ssl_certificate(domain)
        if not ssl_result["is_valid"]:
            risks.append(
                f"Invalid SSL Certificate: {ssl_result.get('error', 'Unknown Error')}"
            )
            is_fake = True

        suspicious_keywords = ["clone", "fake", "mirror", "replica", "test", "mock"]
        if any(keyword in url.lower() for keyword in suspicious_keywords):
            risks.append("Suspicious URL keywords detected")
            is_fake = True

        legitimacy_result = await check_website_legitimacy(domain)
        if not legitimacy_result["is_legitimate"]:
            risks.append(legitimacy_result["details"])
            is_fake = True

        return {
            "is_fake": is_fake,
            "message": "App Authenticity"
            if not is_fake
            else "Potential Fake App Detected",
            "details": f"Risks identified: {', '.join(risks)}"
            if risks
            else "No immediate risks found",
            "domain_info": {"domain": domain, "age_info": domain_age_info},
            "legitimacy_info": legitimacy_result,
        }

    except Exception as e:
        logger.error(f"Unexpected error in URL analysis: {e}")
        return {
            "is_fake": True,
            "message": "Analysis Error",
            "details": f"Unexpected error during URL verification: {e}",
        }


@app.post("/check_app")
async def check_app(request: Request):
    try:
        data = await request.json()
        url = data["url"].strip()

        if not url:
            return {
                "is_fake": True,
                "message": "Invalid URL",
                "details": "No URL provided for verification",
            }

        try:
            parsed_url = urllib.parse.urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
        except Exception:
            return {
                "is_fake": True,
                "message": "Invalid URL",
                "details": "Provided URL is not well-formed",
            }

        result = await analyze_url(url)
        return result

    except Exception as e:
        logger.error(f"Server error in check_app route: {e}")
        return {
            "is_fake": True,
            "message": "Server Error",
            "details": "An unexpected server error occurred",
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)

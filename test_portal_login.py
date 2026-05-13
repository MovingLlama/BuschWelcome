import logging
import sys
import requests
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography import x509

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)

def test_login(username, password, client_type):
    print(f"\nTesting login for {username} with Client-Type: {client_type}...")
    
    # Generate CSR
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, username)]))
        .sign(priv, hashes.SHA256())
    )
    csr_pem = csr.public_bytes(serialization.Encoding.PEM)
    csr_b64 = base64.b64encode(csr_pem).decode()

    url = "https://api.eu.mybuildings.abb.com/certificate/request"
    
    resp = requests.post(
        url,
        auth=requests.auth.HTTPDigestAuth(username, password),
        json={
            "client-csr": csr_b64,
            "client-name": "test-client-123",
            "client-type": client_type,
        },
        timeout=10,
    )
    
    if resp.status_code in (200, 201):
        print("✅ Login successful! Got certificate.")
    else:
        print(f"❌ Login failed: HTTP {resp.status_code}")
        print(f"Response: {resp.text[:200]}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 test_portal_login.py <username> <password>")
        sys.exit(1)
        
    user = sys.argv[1]
    pwd = sys.argv[2]
    
    # Test ABB Android Client Type
    test_login(user, pwd, "com.abb.ispf.client.globalip.app.abb.android")
    
    # Test BJE Android Client Type (Busch-Jaeger)
    test_login(user, pwd, "com.abb.ispf.client.globalip.app.bje.android")
    
    # Test generic BJE Client Type
    test_login(user, pwd, "com.abb.ispf.client.globalip.app.bje")


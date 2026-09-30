# Sandbox Boundary Audit: Gap Closure & Verification Report
Timestamp: 2026-09-29 06:43:36 UTC
Host Uptime:  06:43:36 up  4:49,  0 user,  load average: 0.07, 0.05, 0.07

## 1. Session Durability & Lifecycle State
```
PID 1 Info:
    PID COMMAND                          STARTED     ELAPSED
      1 systemd         Tue Sep 29 01:54:24 2026    04:49:11

Checking Previous Session Markers:
FOUND: /home/hatch/.probe2-marker | SHA256: [HASH REDACTED]
FOUND: /root/.probe2-marker      | SHA256: [HASH REDACTED]
FOUND: /var/tmp/.probe2-marker   | SHA256: [HASH REDACTED]
FOUND: /etc/.probe2-marker       | SHA256: [HASH REDACTED]
FOUND: /tmp/.probe2-marker       | SHA256: [HASH REDACTED]
```

## 2. Complete TLS Chain & Intermediate CA Details

### Local Anchor Metadata
```
--- File: /run/hatch/cell-anchors/hatch-egress-ca.pem ---
subject=CN = Hatch Sandbox Egress CA, O = Hatch
issuer=CN = Hatch Sandbox Egress CA, O = Hatch
notBefore=Jan  1 00:00:00 1975 GMT
notAfter=Jan  1 00:00:00 4096 GMT
SHA1 Fingerprint=[REDACTED]
--- File: /run/hatch/cell-anchors/hatch-ingress-ca.pem ---
subject=C = US, O = Meta Platforms Inc., CN = Meta Hatch Intermediate CA
issuer=C = US, O = Meta Platforms Inc., CN = Meta Hatch Root CA
notBefore=May  7 23:11:26 2026 GMT
notAfter=May  6 23:11:26 2028 GMT
SHA1 Fingerprint=9D:19:A7:AD:4E:D3:C3:AA:D8:76:F1:18:E6:A7:EF:33:45:1F:9F:5A
```
### Meta Hatch Intermediate CA Extraction
Certificate Subject: subject=CN = Hatch Sandbox Egress CA, O = Hatch
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            [REDACTED]
        Signature Algorithm: ecdsa-with-SHA256
        Issuer: CN = Hatch Sandbox Egress CA, O = Hatch
        Validity
            Not Before: Jan  1 00:00:00 1975 GMT
            Not After : Jan  1 00:00:00 4096 GMT
        Subject: CN = Hatch Sandbox Egress CA, O = Hatch
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (256 bit)
                pub:
                    [REDACTED]
                ASN1 OID: prime256v1
                NIST CURVE: P-256
        X509v3 extensions:
            X509v3 Key Usage: critical
                Certificate Sign, CRL Sign
            X509v3 Subject Key Identifier: 
                [REDACTED]
            X509v3 Basic Constraints: critical
                CA:TRUE
            Netscape Comment: 
                Don't panic - generated locally inside your Hatch instance.
    Signature Algorithm: ecdsa-with-SHA256
    Signature Value:
        [REDACTED]

Certificate Subject: subject=C = US, O = Meta Platforms Inc., CN = Meta Hatch Intermediate CA
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            f1:0d:2d:a2:73:ee:ed:f4:c6:70:73:f1:41:60:0f:bf:13:0f:75:23
        Signature Algorithm: ecdsa-with-SHA256
        Issuer: C = US, O = Meta Platforms Inc., CN = Meta Hatch Root CA
        Validity
            Not Before: May  7 23:11:26 2026 GMT
            Not After : May  6 23:11:26 2028 GMT
        Subject: C = US, O = Meta Platforms Inc., CN = Meta Hatch Intermediate CA
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (256 bit)
                pub:
                    04:bb:49:70:50:30:0d:ac:ae:1b:3c:96:ef:c6:4e:
                    74:e0:2b:05:e6:81:8d:0d:aa:e8:18:1c:36:e7:ed:
                    57:68:e5:3f:89:4d:28:4d:20:49:42:68:cd:c2:7a:
                    b1:48:f7:3f:29:61:52:7d:e9:b2:99:91:d6:1a:6e:
                    56:00:6a:e1:eb
                ASN1 OID: prime256v1
                NIST CURVE: P-256
        X509v3 extensions:
            X509v3 Basic Constraints: critical
                CA:TRUE, pathlen:0
            X509v3 Subject Key Identifier: 
                4A:CB:BF:05:50:F1:20:41:D0:1B:86:F3:94:1D:A5:F0:72:60:F2:47
            X509v3 Authority Key Identifier: 
                keyid:A4:E7:8D:C2:AC:6F:4F:3F:93:F1:F5:F6:1E:F5:2B:3A:64:5F:BE:36
                DirName:/C=US/O=Meta Platforms Inc./CN=Meta Hatch Root CA
                serial:03:52:29:7E:26:82:F8:A4:DF:F0:AD:E0:66:74:9C:D4:AC:2C:0A:47
            X509v3 Key Usage: critical
                Digital Signature, Certificate Sign, CRL Sign
            X509v3 CRL Distribution Points: 
                Full Name:
                  URI:https://meta.publickeyinfra.com/arl/hatch
    Signature Algorithm: ecdsa-with-SHA256
    Signature Value:
        30:44:02:20:76:84:7f:4b:a5:6c:dd:34:b2:8e:f9:e2:c5:99:
        47:6f:12:85:74:c6:35:19:31:f8:5e:05:49:c6:99:79:b1:d0:
        02:20:2f:9f:99:96:eb:a7:28:3d:2b:d4:57:92:6a:1f:d1:f5:
        8d:fc:98:e0:06:f5:17:ee:8d:90:a0:7d:ba:74:d2:36


## 3. Proxy Routing & Header Processing

### HTTP Host Header Mismatch Test
```
> Host: forbidden-internal.domain
< HTTP/1.1 200 OK
< Server: cloudflare
```

### Arbitrary SNI Interception Test
```
* Connected to hatch-egress-proxy (fdXX:XXXX:XXXX:XX::1) port 3128
< HTTP/1.1 200 Connection Established
*  subject: CN=internal.unauthorized.local
*  subjectAltName: host "internal.unauthorized.local" matched cert's "internal.unauthorized.local"
*  issuer: CN=Hatch Sandbox Egress CA; O=Hatch
```

--- Audit Complete. Report written to /tmp/probe-3/AUDIT_GAP_CLOSURE_REPORT.md ---

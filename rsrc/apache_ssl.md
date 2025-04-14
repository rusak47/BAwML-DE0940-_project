Enable ssl module
> sudo a2enmod ssl

After each config update check it and restart apache server
> sudo apache2ctl configtest
>
> sudo systemctl restart apache2

### Enable ssl for your domain

```
<VirtualHost *:443>
...
        SSLEngine on
        
        SSLProtocol             all -SSLv3 -TLSv1 -TLSv1.1
        SSLHonorCipherOrder     on
        SSLCompression          off
        SSLSessionTickets       off

        # keeps the strongest ciphers (GCM, CCM, and ChaCha20-based) and eliminates all weak CBC-based ciphers
        SSLCipherSuite          ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-CCM:ECDHE-ECDSA-AES256-CCM

        SSLCertificateFile      /var/certs/letsencrypt/<domain_name>/cert.pem
        SSLCertificateKeyFile  /var/certs/letsencrypt/<domain_name>/privkey.pem

        SSLCertificateChainFile /var/certs/letsencrypt/domo.hunting.ai/chain.pem

...
</VirtualHost>
```

### Add strong Diffie-Hellman (DH) parameters, which are used in the generation of encryption keys
>
> sudo openssl dhparam -out /var/certs/dhparam.pem 4096

Add to VirtualHost :443 section:

```
> sudo vi /etc/apache2/sites-enabled/<domain_name>-ssl.conf 

    SSLOpenSSLConfCmd DHParameters "/var/certs/dhparam.pem"        
```

# Scan security level

[SSL labs](https://www.ssllabs.com/ssltest/analyze.html?d=domain_name&latest)

[Fair SSL](https://www.fairssl.net/en/scan/?protocol=https&hostname=domain_name&port=&scanningType=extended)

[Digicert](https://www.digicert.com/help/)

### Rating

```
> SSL Labs Rating: A (final A+)
```

```
> Fair SSL Rating (experimental) 
  Header Response         Medium risk

 A record via:           supplied IP "ip_addr"
 rDNS (ip_addr):  --
 Service detected:       HTTP
 ...

 Rating specs (not complete)  SSL Labs's 'SSL Server Rating Guide' (version 2009q from 2020-01-30)
 Specification documentation  https://github.com/ssllabs/research/wiki/SSL-Server-Rating-Guide
 Protocol Support (weighted)  100 (30)
 Key Exchange     (weighted)  100 (30)
 Cipher Strength  (weighted)  90 (36)
 Final Score                  96
 Overall Grade                A (final A+)
 Grade cap reasons            Grade capped to A. HSTS is not offered

----------------------------------------
 Scan created with the amazing open source SSL/TLS scanning engine testssl.sh (3.2rc4-24jan2025 OpenSSL 1.0.2-bad) using the command:
testssl.sh --ip=one --full --phone-out --hints --cipher-per-proto --html --json-pretty https://<domain_name>:443

Testssl.sh is free software. Distribution and modification under GPLv2 permitted.
Usage without any warranties and at own risk. Download from testssl.sh

This scan is provided free of charge. Please recommend this service to others.
To allow fair usage if doing many or repeated scans run the scan locally.
```

# Add missing security configs (A+)

### Harden Apache Response Headers

```
> sudo vi /etc/apache2/conf-enabled/security.conf 

    # Hide Apache version and OS
    ServerTokens Prod
    ServerSignature Off
```

### Check OCSP stapling

OCSP (Online Certificate Status Protocol) is a method for checking if an SSL/TLS certificate has been revoked. Normally, this check happens on client side.
This creates several problems:

- Extra connection delay while waiting for the CA
- Privacy concerns (the CA can track which sites users visit)
- Potential failure point if the CA's OCSP server is down

OCSP Stapling solves these issues by having your web server:

- Periodically check with the CA for the certificate's status
- Cache this validation response
- "Staple" (attach) this response directly to the certificate when sending it to browsers

Check certificate has necessary data:
> openssl x509 -in /var/certs/letsencrypt/<domain_name>/cert.pem -text -noout | grep -A 6 "Authority Information Access"
>
```
Authority Information Access: 
                OCSP - URI:http://e5.o.lencr.org
                CA Issuers - URI:http://e5.i.lencr.org/
            X509v3 Subject Alternative Name: 
                DNS:<domain_name>
            X509v3 Certificate Policies: 
                Policy: 2.23.140.1.2.1
```

Add to VirtualHost :443 section:

```
> sudo vi /etc/apache2/sites-enabled/<domain_name>-ssl.conf 

        SSLUseStapling on
        SSLStaplingResponseMaxAge 43200       
```

Once enabled, check that its working:

```
$ openssl s_client -connect <domain_name>:443 -status |grep OCSP
depth=2 C = US, O = Internet Security Research Group, CN = ISRG Root X1
verify return:1
depth=1 C = US, O = Let's Encrypt, CN = E5
verify return:1
depth=0 CN = <domain_name>
verify return:1
OCSP response: 
OCSP Response Data:
    OCSP Response Status: successful (0x0)
    Response Type: Basic OCSP Response
```

## Enable HTTP Strict Transport Security (HSTS)

HSTS tells browsers to always use HTTPS for your domain, even if a user tries to access it via HTTP.

> sudo a2enmod headers

```
> sudo vi /etc/apache2/sites-enabled/<domain_name>-ssl.conf 

        # Enable HSTS with a 1 year duration (31536000 seconds)
        Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
```

# Potential issues

- ### service is available via IP - no https

  - ### Correct Apache rewrite rules for Virtual Hosts

    First, for *:80 redirect.

    ```
    > sudo vi /etc/apache2/sites-enabled/<domain_name>.conf
        # place it above any rewrite rule and proxy directions
        RewriteEngine On
        RewriteCond %{HTTP_HOST} !^your\.domain\.name$ [NC]
        RewriteCond %{HTTP_HOST} ^(\d{1,3}\.){3}\d{1,3}$  [OR]
        RewriteCond %{HTTP_HOST} ^(1\.1\.1\.1|2\.2\.2\.2)$
        RewriteRule ^ https://<domain_name>%{REQUEST_URI} [R=301,L]

    > sudo apache2ctl configtest
    > sudo systemctl restart apache2

    ```

    Check that redirection happens. All http requests using ip should result in Http status 301 Moved Permanently!

    ```
    > curl -s -D - http://ip1/search --insecure -o /dev/null | grep -E 'HTTP/|Location:'
    > curl -s -D - ip1/search --insecure -o /dev/null | grep -E 'HTTP/|Location:'
    > curl -s -D - http://ip1 --insecure -o /dev/null | grep -E 'HTTP/|Location:'
        HTTP/1.1 301 Moved Permanently
        Location: https://<domain_name>/<REQUEST_URI>
    ```

    If everything is working as expected, proceed to configure port :443. Place the same rewrite instructions as mentioned above, following the notes provided. Ensure that these rewrite rules are placed before any others, as their order is important.
    The result of curl requsts now with https should be the same.

- ### BREACH (CVE-2013-3587)                    potentially NOT ok, "gzip" HTTP compression detected. - only supplied "/" tested

  - Can be ignored for static pages or if no secrets in the page

- ### DNS CAA -                                Missing
  
  DNS CAA (Certification Authority Authorization) is a DNS record that specifies which Certificate Authorities (CAs) are authorized to issue certificates for your domain. Adding a CAA record is an additional security layer that helps prevent unauthorized certificate issuance.

    Once configured you can check it by:

  ```
    > dig @ns1.digitalocean.com CAA  <domain_name>

    ;; ANSWER SECTION:
    <domain_name>. 3600 IN CAA 0 issuewild "letsencrypt.org"
    <domain_name>. 3600 IN CAA 0 issue "letsencrypt.org"
    <domain_name>. 3600 IN CAA 0 iodef "mailto:webmaster@email"
  ```

  **NB** Be aware that it won't work for free subdomains, that you don't own with root domain, i.e. that offers freedns.

  ```
     > dig CAA  <domain_name>
    ;; AUTHORITY SECTION:
    <main_domain>.  2362 IN SOA ns1.afraid.org. dnsadmin.afraid.org. 2504130002 86400 7200 2419200 3600

  ```

- ### Certificate Transparency WARNING - Only 2 SCTs included but Google recommends 3 or more

    Manually Check the SCT Count (You want 3 or more entries here.):

    **NB** Let’s Encrypt and ZeroSSL usually include only 2 SCTs by default.

    ```
        > echo | openssl s_client -connect domo.hunting.ai:443 -servername domo.hunting.ai | openssl x509 -text -noout | grep -i "Signed Certificate Timestamp" 


        depth=2 C = US, O = Internet Security Research Group, CN = ISRG Root X1
        verify return:1
        depth=1 C = US, O = Let's Encrypt, CN = E5
        verify return:1
        depth=0 CN = domo.hunting.ai
        verify return:1
                        Signed Certificate Timestamp:
                        Signed Certificate Timestamp:
    ```

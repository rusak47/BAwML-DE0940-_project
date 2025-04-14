[Obtaining your free SSL certificate](https://blog.miguelgrinberg.com/post/using-free-let-s-encrypt-ssl-certificates-in-2025)

[more preferable way](https://www.inmotionhosting.com/support/website/ssl/lets-encrypt-ssl-ubuntu-with-certbot/)

[](https://linuxcommandlibrary.com/man/certbot)
[About letsencrypt](https://letsencrypt.org/getting-started/)

> sudo apt install certbot python3-certbot-apache

> sudo certbot certonly     --agree-tos -m your_email --webroot -w /var/www/your_domain/html -d domain_name  -v

The arguments passed to the certonly subcommand are as follows:
- --agree-tos: indicate that you agree to the terms of service
- -m <email-address>: your email address, to receive important notifications about your SSL certificate such as expiration reminders
- --webroot: select the webroot verification method
- -w /var/www/your_domain/html: configure the webroot directory
- -d <domain-or-subdomain>: the domain or subdomain you want the SSL certificate to apply to. This option can be repeated to attach multiple domains and subdomains to the same certificate.
- --deploy-hook "systemctl reload nginx": the command to run after a certificate is obtained or renewed

The result may look like:
```
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator webroot, Installer None
Requesting a certificate for <domain_name>
Performing the following challenges:
http-01 challenge for <domain_name>
Using the webroot path /var/www/<domain_name>/html for all unmatched domains.
Waiting for verification...
Cleaning up challenges

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/<domain_name>/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/<domain_name>/privkey.pem
This certificate expires on 2025-07-12.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.
Subscribe to the EFF mailing list (email: <your_email>).

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

```
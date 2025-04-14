## Enable apache proxy
[](https://serverfault.com/questions/715905/why-am-i-getting-an-invalid-command-proxypass-error-when-i-start-my-apache-2)
Enable all necessary modules:
```
sudo a2enmod proxy
sudo a2enmod proxy_http
```

[](https://stackoverflow.com/questions/10144634/htaccess-invalid-command-rewriteengine-perhaps-misspelled-or-defined-by-a-m)


```
sudo a2enmod rewrite
```

> sudo systemctl restart apache2

## Configure apache for reverse proxy
[](https://medium.com/@tharos70/streamlit-and-apache-a-guide-to-reverse-proxy-configuration-78af7a3c4467)

[](https://discuss.streamlit.io/t/configuring-apache-2-4-for-proxy/1866/6)

[](https://serverfault.com/questions/1024091/two-apache-servers-on-same-machine-with-same-port)

https://webmasters.stackexchange.com/questions/143699/how-to-have-2-servers-different-paths-with-same-domain

[](https://stackoverflow.com/questions/3940909/configure-apache-to-listen-on-port-other-than-80)

correct enabled site listening port (be aware that it may be enabled in /etc/apache2/ports.conf)
```
 > vi /etc/apache2/sites-enabled/your_domain.conf

Listen 80
<VirtualHost *:80>
    ServerAdmin webmaster@email
    ServerName domain_name
    ServerAlias www.domain_name
    DocumentRoot /var/www/<domain_name>/html
    ErrorLog /var/www/<domain_name>/log/error.log
    CustomLog /var/www/<domain_name>/log/access.log combined
        
    ## proxy configuration redirect calls <domain_name:80>/search to <local_address:port>, e.g. streamlit
   ProxyPreserveHost On ## dont reveal local address
   ProxyPass /search http://<local_address:port>/search
   ProxyPassReverse /search http://<local_address:port>/search

   RewriteEngine On
   RewriteCond %{HTTP:Upgrade} =websocket
   RewriteRule /search/(.*) ws://<local_address:port>/search/$1 [P]
   RewriteCond %{HTTP:Upgrade} !=websocket
   RewriteRule ^/search/(.*) http://<local_address:port>/search/$1 [P]
</VirtualHost>

```

Finally restart server

> sudo service apache2 restart

Check journals that everything is up and running

# Redirect ips to domain name (#see apache_ssl.md)

> apache2ctl -S

```
 > curl -s -D - http://ip2:80 -o /dev/null | grep -E 'HTTP/|Location:'
 HTTP/1.1 301 Moved Permanently
 Location: https://<domain_name>/

 > curl -s -D - http://ip2/search -o /dev/null | grep -E 'HTTP/|Location:'
 HTTP/1.1 301 Moved Permanently
 Location: https://<domain_name>/search

```
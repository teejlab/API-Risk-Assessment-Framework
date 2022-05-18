# Current available fields

## api_endpoint_id

The unique identifier for the API endpoint.

Type: numeric

## api_id

The ID of the API.

Type: numeric

## api_vendor_id

The ID of the API vendor.

Type: numeric

## api_vendor

The vendor of the API, e.g "OneLook", "Victoria State Government Australia", "TeejLab"...

Type: string

## api

The name of the API, e.g "Datamuse Dictionary", "DepartmentAPI"...

Type: string

## category

The category of the API, e.g "Research & Education", "AI & Data Science"...

Type: string

## usage_base

Free or commercial API.

- Free: there are free limits, such as the number of calls that can be made for free. These limits are also available to hackers.
- Commercial: need registration. Additional layer of security

Type: string

## sample_response

A sample response from the API.

- "None": not safe at all
- "Path": risky
- "others not listed": okay
- "OAuth": strongest

-
Type: String

## tagset

List of keys in the sample response.

Type: list

## authentication

Authentication method, e.g "None", "OAuth 2.0", "Basic Authentication"...

The risk level can be found here: <https://owasp.org/www-project-api-security/>

Type: string

## security_test_category

The category of the security test, e.g Broken Authentication', 'Cross-Site Scripting', 'Insecure Deserialization', 'SQL Injection','XML External Entities', 'Buffer Overflow'....
Type: string

## security_test_result

The result of the security test, e.g (FALSE=Passed; TRUE=Failed)
Type: boolean

## server_location

The location of the API, e.g "Australia", "United States"...
Type: string

## hosting_isp

The hosting ISP of the API, e.g "Amazon", "Cloudflare", "Google"...
Type: string

## server_name

The server running the API, e.g "Apache/2.4.33", "Microsoft-IIS/8.5"...
Type: string

## hosting city

The city hosting the API, e.g "Melbourne", "New York"...
Type: string

## response_metadata

The response metadata of the API, e.g "X-Powered-By: PHP/5.6.31"...
Type: string

## risk_label

The risk label of the API, e.g "Low", "Medium", "High"...
Type: string

# Additional Suggested fields

## KSI

Known security issues of the API, e.g "XSS", "SQL Injection", "CSRF", "Insecure CORS"

## PII

Personally Identifiable Information; Any representation of information that permits the identity of an individual to whom the information applies to be reasonably inferred by either direct or indirect means.

## FII

Financial Information: Any representation of information that is reasonably considered to be financial in nature, such as a bank account number, credit card number, or other financial information.

## How many parameters sent: (Exploit Surface)

The number of parameters sent in the API, e.g "5"

# Response Metadata

## status

The status of the API, e.g "200", "404"...

## content_type

The content type of the API, e.g "application/json", "text/html"...

## content_length

The content length of the API, e.g "10", "100"...

## x-powered-by

The x-powered-by of the API, e.g "PHP/5.6.31", "Microsoft-IIS/8.5"...

## access-control-allow-origin

The access-control-allow-origin of the API, e.g "*", "https://www.victoriatax.gov.au"...

## access-control-allow-methods

The access-control-allow-methods of the API, e.g "GET, POST, PUT, DELETE"...

## access-control-allow-headers

The access-control-allow-headers of the API, e.g "Content-Type, Accept, Authorization"...

## access-control-max-age

The access-control-max-age of the API, e.g "3600"...

# Security Category

## Broken Authentication

Broken authentication attacks aim to take over one or more accounts giving the attacker the same privileges as the attacked user.

## Cross-Site Scripting

Cross-Site Scripting (XSS) attacks are a type of injection, in which malicious scripts are injected into otherwise benign and trusted websites.

## Insecure Deserialization

Insecure deserialization is when user-controllable data is deserialized by a website. This potentially enables an attacker to manipulate serialized objects in order to pass harmful data into the application code.

## SQL Injection

A SQL injection attack consists of insertion or “injection” of a SQL query via the input data from the client to the application

## XML External Entities

XML external entities are a type of custom XML entity whose defined values are loaded from outside of the DTD in which they are declared.

## Buffer Overflow

A buffer overflow condition exists when a program attempts to put more data in a buffer than it can hold or when a program attempts to put data in a memory area past a buffer

# HTTP Security Response Headers

The list of HTTP security response headers is cross-referenced with the OWASP HTTP Security Response Headers Guide.
<https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html>

## X-Content-Type-Options

The X-Content-Type header offers a countermeasure against MIME sniffing. It instructs the browser to follow the MIME types indicated in the header. Used as a feature to discover an asset’s file format, MIME sniffing can also be used to execute cross-site scripting attacks.

```
X-Content-Type-Options: nosniff
```

## X-Frame-Options

 In this technique, an attacker fools a user into clicking something that isn’t there. For example, a user might think that he’s on the official website, but something else is running in the background. A user may reveal his/her confidential information in the process.

X-Frame-Options help guard against these kinds of attacks. This is done by disabling the iframes present on the site. In other words, it doesn’t let others embed your content.

```
X-Frame-Options: DENY

X-Frame-Options: SAMEORIGIN

X-Frame-Options: ALLOW-FROM https://example.com/
```

## Cross Site Scripting Protection (X-XSS)

X-XSS header protects against Cross-Site Scripting attacks.

```
X-XSS-Protection: 0

X-XSS-Protection: 1

X-XSS-Protection: 1; mode=block

X-XSS-Protection: 1; report=<reporting-uri>
```

## HTTP Strict Transport Security (HSTS)

If a site is equipped with HTTPS, the server forces the browser to communicate over secure HTTPS. This way, the possibility of an HTTP connection is eliminated entirely.

```
Strict-Transport-Security: max-age=<expire-time>

Strict-Transport-Security: max-age=<expire-time>; includeSubDomains

Strict-Transport-Security: max-age=<expire-time>; preload
```

## X-XSS-Protection

The X-XSS-Protection header was introduced to protect against JavaScript injection attacks through cross-site scripting. The usual syntax was:

```
X-XSS-Protection: 1; mode=block
```

## Expect-CT

To prevent website certificate spoofing, the Expect-CT header can be used to indicate that only new certificates added to Certificate Transparency logs should be accepted. A typical header would be:

```
Expect-CT: max-age=86400, enforce, 
    report-uri="https://example.com/report"
```

## Referrer-Policy

Controls if and how much referrer information should be revealed to the web server. Typical usage would be:

```
Referrer-Policy: origin-when-cross-origin
```

## Content-Type

The Content-Type representation header is used to indicate the original media type of the resource (before any content encoding is applied for sending). NOTE: the charset attribute is necessary to prevent XSS in HTML pages

```
Content-Type: text/html; charset=UTF-8
```

## Set-Cookie

The Set-Cookie HTTP response header is used to send a cookie from the server to the user agent, so the user agent can send it back to the server later. To send multiple cookies, multiple Set-Cookie headers should be sent in the same response.

## Access-Control-Allow-Origin

The Access-Control-Allow-Origin response header indicates whether the response can be shared with requesting code from the given origin. Prefer using specific origin instead of *.

```
Access-Control-Allow-Origin: https://yoursite.com
```

## Server

The Server header describes the software used by the origin server that handled the request — that is, the server that generated the response. Remove this header or set non-informative values.

```
Server: webserver
```

## X-Powered-By

The X-Powered-By header describes the technologies used by the webserver. This information exposes the server to attackers. Using the information in this header, attackers can find vulnerabilities easier. Remove all X-Powered-By headers.

## X-AspNet-Version

Provides information about the .NET version. Disable sending this header.

```
MvcHandler.DisableMvcResponseHeader = true;
```

# Appendix A: Feature Engineering

Tags defined for PII and FII

| **Personally Identifiable Information (PII) tags**  | **Financially Identifiable Information (FII) tags** |
|--------|-----------------------|
| PERSON   | CREDIT_CARD                     |
| LOCATION | CRYPTO                   |
| NRP    | IBAN_CODE                   |
| EMAIL_ADDRESS  | US_BANK_NUMBER                |
| MEDICAL_LICENSE  | US_ITIN                 |
| IP_ADDRESS  | US_SSN                 |

Description of High Risk Security Headers
These descriptions are incorporated from Cheat Sheet (<https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html>)

| **High Risk Security Headers**  | **Description** |
|--------|-----------------------|
| x-frame-options   | It can be used to indicate whether or not a browser should be allowed to render a page in a `<frame>`, `<iframe>`, `<embed>` or `<object>`. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.                     |
| x-xss-protection | It is a feature of Internet Explorer, Chrome, and Safari that stops pages from loading when they detect reflected cross-site scripting (XSS) attacks. |
| strict-transport-security | It lets a website tell browsers that it should only be accessed using HTTPS, instead of using HTTP. |
| expect-ct | It lets sites opt-in to reporting of Certificate Transparency (CT) requirements. Given that mainstream clients now require CT qualification, the only remaining value is reporting such occurrences to the nominated report-uri value in the header. The header is now less about enforcement and more about detection/reporting. |
| referrer-policy | It controls how much referrer information (sent via the Referer header) should be included with requests. |
| content-type | It is used to indicate the original media type of the resource (before any content encoding is applied for sending). |
| set-cookie | It is used to send a cookie from the server to the user agent, so the user agent can send it back to the server later. To send multiple cookies, multiple Set-Cookie headers should be sent in the same response. |
| access-control-allow-origin | It indicates whether the response can be shared with requesting code from the given origin. |
| server | It describes the software used by the origin server that handled the request — that is, the server that generated the response. |
| x-powered-by | It describes the technologies used by the webserver. This information exposes the server to attackers. Using the information in this header, attackers can find vulnerabilities easier. |
| x-aspnet-version | It provides information about the .NET version. |
| x-ratelimit-limit | The maximum number of requests available in the current time frame. |

# Demo Vulnerable Application

⚠️ **WARNING: This application contains intentional security vulnerabilities for testing purposes only!**

## DO NOT use this code in production!

This is a demo application created to test the Aura backend testing agent's security scanning capabilities.

## Vulnerabilities Included

### 1. **SQL Injection** (Multiple instances)
- Direct string concatenation in queries
- f-string formatting in SQL
- No parameterized queries

### 2. **Hardcoded Secrets**
- API keys in source code
- Database passwords
- AWS credentials
- Stripe API keys

### 3. **Command Injection**
- Using `subprocess.run()` with `shell=True`
- No input validation

### 4. **Cross-Site Scripting (XSS)**
- Rendering user input without escaping
- `render_template_string()` with user data

### 5. **Path Traversal**
- No validation on file paths
- Arbitrary file read/write

### 6. **Insecure Deserialization**
- Using `pickle.loads()` on user data
- Unsafe YAML loading

### 7. **XML External Entity (XXE)**
- Unsafe XML parsing

### 8. **Server-Side Request Forgery (SSRF)**
- No URL validation
- Can access internal services

### 9. **Missing Authentication**
- Admin endpoints without auth checks
- No authorization validation

### 10. **Weak Cryptography**
- MD5 for password hashing
- XOR encryption
- Weak random number generation

### 11. **Information Disclosure**
- Debug endpoints exposing secrets
- Environment variables exposed

### 12. **Code Injection**
- Using `eval()` and `exec()` on user input

### 13. **Open Redirect**
- No validation on redirect URLs

### 14. **Insecure Direct Object Reference (IDOR)**
- No authorization checks on resource access

## How to Test

1. Create a ZIP file of this directory:
   ```bash
   cd d:\aura-main
   Compress-Archive -Path demo_vulnerable_app\* -DestinationPath demo_vulnerable_app.zip
   ```

2. Upload to Aura at http://localhost:3000

3. Run the analysis to see all vulnerabilities detected!

## Expected Results

The security agent should detect:
- 10+ SQL injection vulnerabilities
- 5+ hardcoded secrets
- Command injection issues
- XSS vulnerabilities
- Path traversal risks
- Insecure deserialization
- And many more!

# app.py
import os
import json
import base64
import hashlib
import uuid
import re
from datetime import datetime
from flask import Flask, request, redirect, render_template_string, session, jsonify, flash

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()  # Dynamic secret key for sessions

# ========================
# ENHANCED DATA STORAGE
# ========================
USER_DATA_FILE = "users.json"
CONTACT_DATA_FILE = "contacts.json"

def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {} if filename == USER_DATA_FILE else []

def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def get_current_user():
    return session.get('user')

# Password hashing for security
def hash_password(password):
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + key.hex()

def verify_password(stored_password, provided_password):
    salt = bytes.fromhex(stored_password[:32])
    stored_key = stored_password[32:]
    new_key = hashlib.pbkdf2_hmac(
        'sha256', 
        provided_password.encode(), 
        salt, 
        100000
    ).hex()
    return new_key == stored_key

# ========================
# ADVANCED UTILITIES
# ========================
def json_format(text):
    try:
        parsed = json.loads(text)
        return json.dumps(parsed, indent=2)
    except:
        return "Invalid JSON"

def markdown_to_html(text):
    # Simple Markdown conversion
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'^# (.*)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text.replace('\n', '<br>')

def html_to_markdown(text):
    # Simple HTML to Markdown conversion
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text)
    text = re.sub(r'<h1>(.*?)</h1>', r'# \1', text)
    text = re.sub(r'<h2>(.*?)</h2>', r'## \1', text)
    text = re.sub(r'<code>(.*?)</code>', r'`\1`', text)
    return text.replace('<br>', '\n')

# ========================
# EMBEDDED CSS (Enhanced)
# ========================
CSS = """
:root {
    --primary: #6366f1;
    --primary-light: #818cf8;
    --secondary: #10b981;
    --secondary-light: #34d399;
    --dark: #0f172a;
    --darker: #020617;
    --light: #f8fafc;
    --gray: #94a3b8;
    --danger: #ef4444;
    --warning: #f59e0b;
    --success: #22c55e;
    --glass: rgba(30, 41, 59, 0.7);
    --glass-light: rgba(148, 163, 184, 0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
}

body {
    background: radial-gradient(circle at top right, var(--darker), var(--dark));
    color: var(--light);
    min-height: 100vh;
    overflow-x: hidden;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 0;
}

/* Navigation */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 0;
    border-bottom: 1px solid var(--glass-light);
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(10px);
}

.logo {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.logo-icon {
    font-size: 2rem;
}

.nav-links {
    display: flex;
    gap: 2rem;
}

.nav-link {
    color: var(--gray);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    position: relative;
}

.nav-link:hover, .active {
    color: var(--light);
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    transition: width 0.3s ease;
}

.nav-link:hover::after, .active::after {
    width: 100%;
}

.btn {
    padding: 0.7rem 1.5rem;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    text-decoration: none;
    display: inline-block;
    background: transparent;
    position: relative;
    overflow: hidden;
    z-index: 1;
}

.btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 0%;
    height: 100%;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    transition: width 0.5s ease;
    z-index: -1;
}

.btn:hover::before {
    width: 100%;
}

.btn-primary {
    border: 2px solid var(--primary);
    color: var(--light);
}

.btn-primary:hover {
    color: var(--light);
    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
}

.btn-outline {
    border: 2px solid var(--primary);
    color: var(--primary);
}

.btn-outline:hover {
    color: var(--light);
    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
}

/* Hero Section */
.hero {
    padding: 8rem 0 5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
    z-index: -1;
}

.hero h1 {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    background: linear-gradient(90deg, var(--primary-light), var(--secondary-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeIn 1s ease-out;
    line-height: 1.2;
}

.hero p {
    font-size: 1.3rem;
    color: var(--gray);
    max-width: 800px;
    margin: 0 auto 3rem;
    animation: fadeIn 1.2s ease-out;
    line-height: 1.6;
}

/* Cards & Features */
.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2.5rem;
    margin: 5rem 0;
}

.card {
    background: var(--glass);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2.5rem;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
    border: 1px solid var(--glass-light);
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 0%;
    background: linear-gradient(180deg, var(--primary), var(--secondary));
    transition: height 0.5s ease;
    z-index: 0;
}

.card:hover::before {
    height: 100%;
}

.card:hover {
    transform: translateY(-15px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.card-content {
    position: relative;
    z-index: 1;
}

.card h3 {
    color: var(--primary-light);
    margin-bottom: 1.5rem;
    font-size: 1.6rem;
}

.card p {
    color: var(--gray);
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.card-icon {
    font-size: 3rem;
    margin-bottom: 1.5rem;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Dashboard */
.dashboard {
    padding: 3rem 0;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3rem;
}

.user-greeting {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.user-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    font-weight: bold;
    color: white;
}

.widget-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.widget {
    background: var(--glass);
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid var(--glass-light);
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease;
}

.widget:hover {
    transform: translateY(-5px);
}

.widget-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--glass-light);
    padding-bottom: 1rem;
}

.widget-title {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-size: 1.4rem;
}

.widget-icon {
    color: var(--primary-light);
    font-size: 1.8rem;
}

.tools-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.tool-card {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 15px;
    padding: 1.5rem;
    transition: transform 0.3s ease;
    border: 1px solid var(--glass-light);
}

.tool-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.tool-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.2rem;
}

.tool-icon {
    color: var(--secondary);
    font-size: 1.5rem;
}

textarea, input, select {
    width: 100%;
    padding: 1rem;
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid var(--glass-light);
    color: white;
    margin: 0.8rem 0;
    font-size: 1rem;
    transition: all 0.3s ease;
}

textarea:focus, input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
}

textarea {
    min-height: 150px;
    resize: vertical;
}

.result-box {
    background: rgba(15, 23, 42, 0.7);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid var(--glass-light);
    min-height: 150px;
    margin: 0.8rem 0;
    overflow: auto;
    white-space: pre-wrap;
}

.tool-actions {
    display: flex;
    gap: 0.8rem;
    margin-top: 1rem;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}

.animate-fade {
    animation: fadeIn 0.8s ease-out forwards;
}

.animate-float {
    animation: float 6s ease-in-out infinite;
}

.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }

/* Particles Background */
.particles {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -2;
    overflow: hidden;
}

.particle {
    position: absolute;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    opacity: 0.3;
    animation: float 15s infinite linear;
}

/* Notification */
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 2rem;
    border-radius: 10px;
    color: white;
    font-weight: 500;
    z-index: 1000;
    transform: translateX(150%);
    transition: transform 0.5s ease;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}

.notification.show {
    transform: translateX(0);
}

.notification.success {
    background: rgba(34, 197, 94, 0.2);
    border-left: 5px solid var(--success);
}

.notification.error {
    background: rgba(239, 68, 68, 0.2);
    border-left: 5px solid var(--danger);
}

/* Responsive */
@media (max-width: 768px) {
    .nav-links { 
        position: fixed;
        top: 80px;
        right: -100%;
        flex-direction: column;
        background: var(--glass);
        backdrop-filter: blur(10px);
        width: 70%;
        height: calc(100vh - 80px);
        padding: 2rem;
        transition: right 0.5s ease;
        z-index: 99;
    }
    
    .nav-links.show {
        right: 0;
    }
    
    .hero h1 { font-size: 2.8rem; }
    .tools-grid { grid-template-columns: 1fr; }
    .dashboard-header { flex-direction: column; gap: 1.5rem; align-items: flex-start; }
}

.mobile-menu-btn {
    display: none;
    background: transparent;
    border: none;
    color: var(--light);
    font-size: 1.8rem;
    cursor: pointer;
}

@media (max-width: 768px) {
    .mobile-menu-btn {
        display: block;
    }
}
"""

# ========================
# EMBEDDED JAVASCRIPT (Enhanced)
# ========================
JS = """
document.addEventListener('DOMContentLoaded', () => {
    // Create particles
    const particlesContainer = document.querySelector('.particles');
    if (particlesContainer) {
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            // Random properties
            const size = Math.random() * 10 + 5;
            const posX = Math.random() * 100;
            const posY = Math.random() * 100;
            const delay = Math.random() * 15;
            
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${posX}%`;
            particle.style.top = `${posY}%`;
            particle.style.animationDelay = `${delay}s`;
            particle.style.opacity = Math.random() * 0.3 + 0.1;
            
            particlesContainer.appendChild(particle);
        }
    }
    
    // Animation observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.card, .hero > *').forEach(el => {
        observer.observe(el);
    });

    // Dashboard tool functionality
    document.querySelectorAll('.tool-action').forEach(btn => {
        btn.addEventListener('click', function() {
            const toolId = this.dataset.tool;
            const input = document.querySelector(`#${toolId}-input`);
            const output = document.querySelector(`#${toolId}-output`);
            
            try {
                if(toolId === 'base64-encode') {
                    output.value = btoa(unescape(encodeURIComponent(input.value)));
                } else if(toolId === 'base64-decode') {
                    output.value = decodeURIComponent(escape(atob(input.value)));
                } else if(toolId === 'url-encode') {
                    output.value = encodeURIComponent(input.value);
                } else if(toolId === 'url-decode') {
                    output.value = decodeURIComponent(input.value);
                } else if(toolId === 'json-format') {
                    output.textContent = JSON.stringify(JSON.parse(input.value), null, 2);
                } else if(toolId === 'markdown-html') {
                    output.innerHTML = markdownToHtml(input.value);
                } else if(toolId === 'html-markdown') {
                    output.value = htmlToMarkdown(input.value);
                }
            } catch(e) {
                if(output.value !== undefined) output.value = "Error: Invalid input";
                else output.textContent = "Error: Invalid input";
            }
        });
    });

    // Format JSON on input
    document.querySelectorAll('.json-input').forEach(input => {
        input.addEventListener('input', function() {
            try {
                const obj = JSON.parse(this.value);
                this.nextElementSibling.textContent = JSON.stringify(obj, null, 2);
            } catch {
                this.nextElementSibling.textContent = "Invalid JSON";
            }
        });
    });

    // Mobile menu toggle
    document.querySelector('.mobile-menu-btn')?.addEventListener('click', () => {
        document.querySelector('.nav-links').classList.toggle('show');
    });

    // Show notifications
    const showNotification = (message, type) => {
        const notification = document.createElement('div');
        notification.classList.add('notification', type);
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 3000);
    };

    // Check for URL params to show notifications
    const urlParams = new URLSearchParams(window.location.search);
    if(urlParams.has('signup_success')) {
        showNotification('Account created successfully!', 'success');
    } else if(urlParams.has('login_success')) {
        showNotification('Login successful!', 'success');
    } else if(urlParams.has('contact_success')) {
        showNotification('Message sent successfully!', 'success');
    }

    // Markdown conversion functions
    function markdownToHtml(text) {
        // Simple Markdown to HTML conversion
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        text = text.replace(/^# (.*)$/gm, '<h1>$1</h1>');
        text = text.replace(/^## (.*)$/gm, '<h2>$1</h2>');
        text = text.replace(/`(.*?)`/g, '<code>$1</code>');
        text = text.replace(/\n/g, '<br>');
        return text;
    }

    function htmlToMarkdown(text) {
        // Simple HTML to Markdown conversion
        text = text.replace(/<strong>(.*?)<\/strong>/g, '**$1**');
        text = text.replace(/<em>(.*?)<\/em>/g, '*$1*');
        text = text.replace(/<h1>(.*?)<\/h1>/g, '# $1');
        text = text.replace(/<h2>(.*?)<\/h2>/g, '## $1');
        text = text.replace(/<code>(.*?)<\/code>/g, '`$1`');
        text = text.replace(/<br>/g, '\n');
        return text;
    }
});
"""

# ========================
# PAGE TEMPLATES (Enhanced)
# ========================
def base_template(content, title="AI Portfolio"):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>{CSS}</style>
    <script>{JS}</script>
</head>
<body>
    <div class="particles"></div>
    {content}
</body>
</html>
"""

def portfolio_template():
    return f"""
<section class="hero">
    <h1>AI-Powered Web Portfolio</h1>
    <p>Next-generation developer portfolio with integrated dashboard tools and secure authentication</p>
    <div class="cta">
        <a href="/login" class="btn btn-primary">Get Started</a>
        <a href="#features" class="btn btn-outline">Explore Features</a>
    </div>
</section>

<section id="features" class="features">
    <div class="card animate-fade delay-1">
        <div class="card-icon">
            <i class="fas fa-shield-alt"></i>
        </div>
        <div class="card-content">
            <h3>Secure Authentication</h3>
            <p>JSON-based user storage with password hashing and session management. Enterprise-grade security in a lightweight package.</p>
        </div>
    </div>
    
    <div class="card animate-fade delay-2">
        <div class="card-icon">
            <i class="fas fa-tools"></i>
        </div>
        <div class="card-content">
            <h3>Real-time Tools</h3>
            <p>Integrated encoding utilities, JSON formatting, and Markdown conversion accessible directly from your dashboard.</p>
        </div>
    </div>
    
    <div class="card animate-fade delay-3">
        <div class="card-icon">
            <i class="fas fa-mobile-alt"></i>
        </div>
        <div class="card-content">
            <h3>Responsive Design</h3>
            <p>Mobile-first layout with smooth animations and modern UI components that work flawlessly on all devices.</p>
        </div>
    </div>
</section>

<section class="contact" id="contact">
    <h2 class="section-title">Contact Me</h2>
    <form id="contact-form" action="/contact" method="POST">
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="message" placeholder="Your Message" rows="4" required></textarea>
        <button type="submit" class="btn btn-primary">Send Message</button>
    </form>
</section>
"""

def dashboard_template():
    user = get_current_user()
    first_letter = user['username'][0].upper() if user['username'] else 'U'
    return f"""
<section class="dashboard">
    <div class="dashboard-header">
        <div class="user-greeting">
            <div class="user-avatar">{first_letter}</div>
            <div>
                <h2>Welcome, {user['username']}</h2>
                <p>Member since: {user['joined']}</p>
            </div>
        </div>
        <a href="/logout" class="btn btn-outline">Logout</a>
    </div>

    <div class="widget-grid">
        <div class="widget">
            <div class="widget-header">
                <div class="widget-title">
                    <i class="fas fa-user widget-icon"></i>
                    <h3>User Profile</h3>
                </div>
            </div>
            <div class="profile-info">
                <p><i class="fas fa-envelope"></i> <strong>Email:</strong> {user['email']}</p>
                <p><i class="fas fa-calendar-alt"></i> <strong>Member since:</strong> {user['joined']}</p>
                <p><i class="fas fa-key"></i> <strong>Account Type:</strong> Premium</p>
            </div>
        </div>

        <div class="widget">
            <div class="widget-header">
                <div class="widget-title">
                    <i class="fas fa-tools widget-icon"></i>
                    <h3>Developer Tools</h3>
                </div>
            </div>
            <div class="tools-grid">
                <div class="tool-card">
                    <div class="tool-header">
                        <i class="fas fa-lock tool-icon"></i>
                        <h4>Base64 Encode</h4>
                    </div>
                    <textarea id="base64-encode-input" placeholder="Enter text to encode"></textarea>
                    <button class="btn btn-primary tool-action" data-tool="base64-encode">Encode</button>
                    <textarea id="base64-encode-output" placeholder="Encoded result" readonly></textarea>
                </div>
                
                <div class="tool-card">
                    <div class="tool-header">
                        <i class="fas fa-lock-open tool-icon"></i>
                        <h4>Base64 Decode</h4>
                    </div>
                    <textarea id="base64-decode-input" placeholder="Enter text to decode"></textarea>
                    <button class="btn btn-primary tool-action" data-tool="base64-decode">Decode</button>
                    <textarea id="base64-decode-output" placeholder="Decoded result" readonly></textarea>
                </div>
                
                <div class="tool-card">
                    <div class="tool-header">
                        <i class="fas fa-link tool-icon"></i>
                        <h4>URL Encode</h4>
                    </div>
                    <textarea id="url-encode-input" placeholder="Enter URL to encode"></textarea>
                    <button class="btn btn-primary tool-action" data-tool="url-encode">Encode</button>
                    <textarea id="url-encode-output" placeholder="Encoded result" readonly></textarea>
                </div>
                
                <div class="tool-card">
                    <div class="tool-header">
                        <i class="fas fa-unlink tool-icon"></i>
                        <h4>URL Decode</h4>
                    </div>
                    <textarea id="url-decode-input" placeholder="Enter URL to decode"></textarea>
                    <button class="btn btn-primary tool-action" data-tool="url-decode">Decode</button>
                    <textarea id="url-decode-output" placeholder="Decoded result" readonly></textarea>
                </div>
                
                <div class="tool-card">
                    <div class="tool-header">
                        <i class="fas fa-code tool-icon"></i>
                        <h4>JSON Formatter</h4>
                    </div>
                    <textarea id="json-format-input" class="json-input" placeholder='Enter JSON: {"key":"value"}'></textarea>
                    <div class="result-box" id="json-format-output">Formatted JSON will appear here</div>
                    <div class="tool-actions">
                        <button class="btn btn-primary tool-action" data-tool="json-format">Format JSON</button>
                    </div>
                </div>
                
                <div class="tool-card">
                    <div class="tool-header">
                        <i class="fas fa-file-alt tool-icon"></i>
                        <h4>Markdown to HTML</h4>
                    </div>
                    <textarea id="markdown-html-input" placeholder="Enter Markdown text"></textarea>
                    <button class="btn btn-primary tool-action" data-tool="markdown-html">Convert</button>
                    <div class="result-box" id="markdown-html-output">HTML output will appear here</div>
                </div>
            </div>
        </div>
    </div>
</section>
"""

def auth_template(form_type, error=None):
    error_html = f'<div class="error" style="color: var(--danger); margin-bottom: 1.5rem; text-align: center; padding: 1rem; background: rgba(239,68,68,0.1); border-radius: 10px;"><i class="fas fa-exclamation-circle"></i> {error}</div>' if error else ''
    return f"""
<section class="auth-form">
    <div class="card" style="max-width: 500px; margin: 5rem auto;">
        <div style="text-align: center; margin-bottom: 2rem;">
            <div class="logo" style="font-size: 2.5rem;">
                <i class="fas fa-cube logo-icon"></i>
                AI Portfolio
            </div>
            <p style="color: var(--gray); margin-top: 0.5rem;">{'Login to your account' if form_type == 'login' else 'Create a new account'}</p>
        </div>
        
        {error_html}
        
        <form id="auth-form" action="/{'login' if form_type == 'login' else 'signup'}" method="POST">
            <div style="margin-bottom: 1.5rem;">
                <label style="display: block; margin-bottom: 0.5rem; color: var(--gray);">Username</label>
                <input type="text" name="username" placeholder="Enter your username" required style="width: 100%;">
            </div>
            
            {'<div style="margin-bottom: 1.5rem;"><label style="display: block; margin-bottom: 0.5rem; color: var(--gray);">Email</label><input type="email" name="email" placeholder="Enter your email" required style="width: 100%;"></div>' if form_type == 'signup' else ''}
            
            <div style="margin-bottom: 2rem;">
                <label style="display: block; margin-bottom: 0.5rem; color: var(--gray);">Password</label>
                <input type="password" name="password" placeholder="Enter your password" required style="width: 100%;">
            </div>
            
            <button type="submit" class="btn btn-primary" style="width: 100%; padding: 1rem; font-size: 1.1rem;">
                {'Login' if form_type == 'login' else 'Sign Up'}
            </button>
        </form>
        
        <p style="margin-top: 2rem; text-align: center; color: var(--gray);">
            {'Need an account? <a href="/signup" style="color: var(--primary);">Sign Up</a>' if form_type == 'login' else 'Already have an account? <a href="/login" style="color: var(--primary);">Login</a>'}
        </p>
    </div>
</section>
"""

# ========================
# FLASK ROUTES (Enhanced)
# ========================
@app.route('/')
def home():
    navbar = """
    <nav class="navbar">
        <div class="logo">
            <i class="fas fa-cube logo-icon"></i>
            AI Portfolio
        </div>
        <div class="nav-links">
            <a href="/" class="nav-link active">Home</a>
            <a href="#features" class="nav-link">Features</a>
            <a href="#contact" class="nav-link">Contact</a>
            <a href="/login" class="nav-link">Dashboard</a>
        </div>
        <button class="mobile-menu-btn">☰</button>
    </nav>
    """
    content = navbar + portfolio_template()
    return render_template_string(base_template(content))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if get_current_user():
        return redirect('/dashboard')
        
    if request.method == 'POST':
        users = load_data(USER_DATA_FILE)
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Basic validation
        if not username or not email or not password:
            content = auth_template('signup', error="All fields are required")
            return render_template_string(base_template(content, title="Sign Up"))
            
        if username in users:
            content = auth_template('signup', error="Username already exists")
            return render_template_string(base_template(content, title="Sign Up"))
            
        # Simple email validation
        if '@' not in email or '.' not in email:
            content = auth_template('signup', error="Invalid email address")
            return render_template_string(base_template(content, title="Sign Up"))
            
        users[username] = {
            'password': hash_password(password),
            'email': email,
            'joined': datetime.now().strftime("%Y-%m-%d")
        }
        save_data(users, USER_DATA_FILE)
        session['user'] = {'username': username, **users[username]}
        return redirect('/dashboard?login_success=true')
    
    content = auth_template('signup')
    return render_template_string(base_template(content, title="Sign Up"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if get_current_user():
        return redirect('/dashboard')
        
    if request.method == 'POST':
        users = load_data(USER_DATA_FILE)
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            content = auth_template('login', error="Username and password are required")
            return render_template_string(base_template(content, title="Login"))
            
        if username not in users or not verify_password(users[username]['password'], password):
            content = auth_template('login', error="Invalid username or password")
            return render_template_string(base_template(content, title="Login"))
        
        session['user'] = {'username': username, **users[username]}
        return redirect('/dashboard?login_success=true')
    
    content = auth_template('login')
    return render_template_string(base_template(content, title="Login"))

@app.route('/dashboard')
def dashboard():
    if not get_current_user():
        return redirect('/login')
    
    navbar = f"""
    <nav class="navbar">
        <div class="logo">
            <i class="fas fa-cube logo-icon"></i>
            Dashboard
        </div>
        <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/dashboard" class="nav-link active">Dashboard</a>
            <a href="#contact" class="nav-link">Contact</a>
            <a href="/logout" class="nav-link">Logout</a>
        </div>
        <button class="mobile-menu-btn">☰</button>
    </nav>
    """
    content = navbar + dashboard_template()
    return render_template_string(base_template(content, title="Dashboard"))

@app.route('/contact', methods=['POST'])
def contact():
    contacts = load_data(CONTACT_DATA_FILE)
    contact_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'message': request.form['message'],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    contacts.append(contact_data)
    save_data(contacts, CONTACT_DATA_FILE)
    return redirect('/?contact_success=true')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# ========================
# RUN APPLICATION
# ========================
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
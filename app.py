from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

# ============================================
# PAGE ROUTES
# ============================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services.html')
def services():
    return render_template('services.html')

@app.route('/projects.html')
def projects():
    return render_template('projects.html')

@app.route('/courses.html')
def courses():
    return render_template('courses.html')

@app.route('/careers.html')
def careers():
    return render_template('careers.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# ============================================
# EMAIL API ROUTES
# ============================================

@app.route('/api/contact', methods=['POST'])
def api_contact():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', '')
        message = data.get('message')
        
        msg_body = f"""
New message from website:

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
"""
        
        msg = Message(
            subject=f"Contact from {name}",
            recipients=[os.environ.get('MAIL_USERNAME')],
            body=msg_body,
            reply_to=email
        )
        mail.send(msg)
        
        return jsonify({'message': 'Message sent!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscribe', methods=['POST'])
def api_subscribe():
    try:
        data = request.get_json()
        email = data.get('email')
        
        msg = Message(
            subject="New Subscriber",
            recipients=[os.environ.get('MAIL_USERNAME')],
            body=f"New subscriber: {email}"
        )
        mail.send(msg)
        
        return jsonify({'message': 'Subscribed!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
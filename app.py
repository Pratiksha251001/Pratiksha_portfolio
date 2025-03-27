from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your-app-password')
mail = Mail(app)

# Ensure directories exist
for dir_name in ['messages', 'applications']:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # Validate required fields
        if not all([name, email, subject, message]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400

        # Create message object
        message_obj = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }

        # Save message to file
        filename = f"messages/message_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(message_obj, f, indent=4)

        # Send email notification
        try:
            msg = Message(
                subject=f"New Contact Form Message: {subject}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']]  # Send to yourself
            )
            msg.body = f"""
            New message from your portfolio website:
            
            From: {name} ({email})
            Subject: {subject}
            
            Message:
            {message}
            """
            mail.send(msg)
        except Exception as e:
            print(f"Email notification failed: {str(e)}")

        return jsonify({
            'success': True,
            'message': 'Message sent successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500

@app.route('/api/apply', methods=['POST'])
def apply():
    try:
        # Get form data
        course_type = request.form.get('courseType')
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        previous_education = request.form.get('previousEducation')
        percentage = request.form.get('percentage')
        
        # Handle file upload
        documents = request.files.get('documents')
        
        if not all([course_type, full_name, email, phone, previous_education, percentage, documents]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400

        # Create application object
        application = {
            'courseType': course_type,
            'fullName': full_name,
            'email': email,
            'phone': phone,
            'previousEducation': previous_education,
            'percentage': percentage,
            'timestamp': datetime.now().isoformat()
        }

        # Save application data
        app_filename = f"applications/application_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(app_filename, 'w') as f:
            json.dump(application, f, indent=4)

        # Save uploaded document
        if documents:
            doc_filename = f"applications/documents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            documents.save(doc_filename)

        # Send email notification
        try:
            msg = Message(
                subject=f"New Course Application: {course_type.upper()}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']]
            )
            msg.body = f"""
            New course application received:
            
            Course: {course_type.upper()}
            Name: {full_name}
            Email: {email}
            Phone: {phone}
            Previous Education: {previous_education}
            Percentage: {percentage}%
            
            Please check the applications folder for attached documents.
            """
            mail.send(msg)
        except Exception as e:
            print(f"Email notification failed: {str(e)}")

        return jsonify({
            'success': True,
            'message': 'Application submitted successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
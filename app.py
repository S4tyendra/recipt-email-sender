from flask import Flask, request, jsonify
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Email configuration
sender_email = "2022kucp1033@iiitkota.ac.in"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "2022kucp1033@iiitkota.ac.in"
smtp_password = os.getenv("PASS")

@app.route('/')
def hello_world():
    return 'Hello, World!'


html_ = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Entry Pass</title>
</head>

<body style="font-family: Arial, sans-serif;">

  <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
    <h1 style="text-align: center;">Invitation pass!</h1>
    <p>Dear [_name_],</p>
    <p>This is to inform you that your invitation pass is ready. Please find the details below:</p>

    <img src="https://freshers-iiitk.devh.in/api/innvoice/[_id_]" alt="Invoice Image" style="max-width: 100%; height: 70%; width: 70%; margin: 20px 0;">
  
    <p style="text-align: center;">
      <a href="https://freshers-iiitk.devh.in/approved/[_id_]" target="_blank" style="text-decoration: none; background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 5px; margin: 20px 0; display: inline-block;">
        View in Browser / Download
      </a>
    </p>

    <p style="text-align: left;">Regards,<br>Satyendra<br>2022KUCP1033<br><a href="https://www.linkedin.com/in/s4tyendra/">Linkedin</a> · <a href="https://satyendra.in/">Website</a></p>

  </div>

</body>

</html>

"""



@app.route('/send_email', methods=['GET'])
def send_email():
    try:
        name = request.args.get('name')
        id_ = request.args.get('id')

        if not name or not id_:
            return jsonify({'error': 'Missing parameters'}), 400

        subject = f"Invitation Pass for {name}"
        body = html_.replace("[_id_]",id_).replace("[_name_]",name)
        receiver_email = f"{id_.lower()}@iiitkota.ac.in"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return jsonify({'message': 'Email sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

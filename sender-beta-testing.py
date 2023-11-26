import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_sender_details():
    sender_email = input("Enter the sender's email address: ")
    password = input("Enter the sender's password: ")
    return sender_email, password

def get_receiver_details():
    receiver_email = input("Enter the recipient's email address: ")
    return receiver_email

def get_email_content():
    subject = input("Enter the subject of the email: ")
    body = input("Enter the body of the email: ")
    return subject, body

def main():
    # Get user input for sender details
    sender_email, password = get_sender_details()

    # Get user input for recipients, body, and message
    receiver_email = get_receiver_details()
    subject, body = get_email_content()

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add body to the email
    message.attach(MIMEText(body, 'plain'))

    # SMTP server configuration
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    # Create a secure connection with the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login to your Outlook account
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Close the connection
    server.quit()

    # Display a message after sending the email
    print("Email sent!")

if __name__ == '__main__':
    main()
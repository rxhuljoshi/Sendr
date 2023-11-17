#!/usr/bin/env python3
# FILEPATH: /C:/Users/joshi/Code/Sendr/sendr.py
import speech_recognition as sr
import pyttsx3
import sqlite3
import smtplib, ssl
from email.message import EmailMessage
import getpass
import os
import sys
import keyboard

number_names = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
}

def name_number(name):
    words = name.split()
    number = 0
    for word in words:
        if word not in number_names:
            return None
        if number_names[word] >= 1000:
            number += number_names[word]
            number *= number_names[word]
        else:
            number += number_names[word]
    return number

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    attempts = 0
    while attempts < 3:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            speak(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand your command.")
            speak("Sorry, I could not understand your command.")
            attempts += 1
    print("Sorry, I could not understand your command. Please type your input:")
    speak("Sorry, I could not understand your command. Please type your input:")
    text = input()
    return text

def send_email(to, subject, body):
    msg = EmailMessage()
    msg['From'] = os.environ.get('rjdeep0301@gmail.com')
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(os.environ.get('rjdeep0301@gmail.com'), os.environ.get('Rxhul@321'))
        server.send_message(msg)

def add_contact(name, email):
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS contacts (name TEXT, email TEXT)')
        cursor.execute('INSERT INTO contacts (name, email) VALUES (?, ?)', (name, email))
        conn.commit()

def delete_contact(name):
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE name = ?', (name,))
        conn.commit()

def remove_all_contacts():
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts')
        conn.commit()

def get_email(name):
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM contacts WHERE name = ?', (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

def show_contacts():
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        results = cursor.fetchall()
        if len(results) == 0:
            print("No contacts found.")
            speak("No contacts found.")
        else:
            for i, row in enumerate(results):
                print(f"{i+1}. {row[0]}: {row[1]}")

def exit():
    print("Exiting...")
    speak("Bye Bye!")
    sys.exit()

def greet():
    print("Hi! I am Sendr, your virtual Email BOT.")
    speak("Hi! I am Sendr, your virtual Email BOT.")
    speak("What should I call you?")
    name=input("Enter your name: ")
    speak(f"Hello {name}! How can I help you?")
    print(f"Hello {name}! How can I help you?")
        
def main():
    greet()
    print("Here are the available commands:")
    speak("Here are the available commands:")
    print('''1. Write email
2. Send email
3. Add contact
4. Delete contact
5. Remove all contacts
6. Show contacts
7. Exit''')
    print("Press the spacebar to continue or escape to exit.")
    speak("Press the spacebar to continue or escape to exit.")
    while True:
        event = keyboard.read_event()
        if event.name == 'space':
            break
        elif event.name == 'esc':
            exit()

    while True:
        command = listen().lower()

        if "write email" in command:
            print("To whom do you want to send the email?")
            speak("To whom do you want to send the email?")
            to = listen()
            email = get_email(to)

            if email is None:
                print("Email address not found. Please enter the email address:")
                speak("Email address not found. Please enter the email address:")
                email = input()
                add_contact(to, email)
            print("What is the subject of the email?")
            speak("What is the subject of the email?")
            subject = listen()
            choice = input("Do you want to manually enter the body of the email?")
            if choice == "yes":
                print("Please enter the body of the email:")
                speak("Please enter the body of the email:")
                body = input()
            else:
                print("What is the body of the email?")
                speak("What is the body of the email?")
                body = listen()
            print("Email written successfully!")
            speak("Email written successfully!")
            print("Do you want to send the email?")
            speak("Do you want to send the email?")
            choice = listen()
            if choice == "yes":
                send_email(email, subject, body)
                print("Email sent successfully!")
                speak("Email sent successfully!")
            else:
                print("Are you sure you don't want to send the email?")
                speak("Are you sure you don't want to send the email?")
                choice = listen()
                if choice == "yes":
                    print("Email not sent.")
                    speak("Email not sent.")
                        
        elif "add contact" in command:
            print("What is the name of the contact?")
            speak("What is the name of the contact?")
            name = listen()
            print("What is the email of the contact?")
            speak("What is the email of the contact?")
            email = input()
            add_contact(name, email)
        
        elif "delete contact" in command:
            show_contacts()
            print("Enter the number of the contact you want to delete:")
            speak("Enter the number of the contact you want to delete:")
            x = listen()
            num = name_number(x)
            with sqlite3.connect('contacts.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT name FROM contacts')
                results = cursor.fetchall()
                if len(results) == 0:
                    print("No contacts found.")
                    speak("No contacts found.")
                elif num < 1 or num > len(results):
                    print("Invalid number.")
                    speak("Invalid number.")
                else:
                    name = results[num-1][0]
                    delete_contact(name)
                    print(f"{name} Deleted successfully!")
                    speak(f"{name} Deleted successfully!")
        
        elif "remove all contacts" in command:
            remove_all_contacts()
            print("All contacts removed successfully!")
            speak("All contacts removed successfully!")        
        
        elif "show contacts" in command:
            show_contacts()
        
        elif "exit" in command:
            exit()
        
        else:
            print("Invalid command. Please try again.")
            speak("Invalid command. Please try again.")
            print("Press Space to continue or Escape to exit.")
            speak("Press Space to continue or Escape to exit.")
            while True:
                event = keyboard.read_event()
                if event.name == 'space':
                    break
                elif event.name == 'esc':
                    exit()

if __name__ == '__main__':
    main()
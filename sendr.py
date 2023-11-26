#!/usr/bin/env python3
# FILEPATH: /C:/Users/joshi/Code/Sendr/sendr.py
import speech_recognition as sr
import pyttsx3
import sqlite3
import smtplib, ssl
from email.message import EmailMessage
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
        server.login(os.environ.get('rjdeep0301@gmail.com'), os.environ.get('Rjdeep@0301')) #let's just write this as my password for now
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
2. Send email (Use Drafts)
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

        if "write email" in command or "right email" in command or "white email" in command:
            print("You said: Write Email")
            speak("You said: Write Email")
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
            if choice == "yes" or "Yes" or "YES":
                send_email(email, subject, body)
                print("Email sent successfully!")
                speak("Email sent successfully!")
            else:
                print("Are you sure you don't want to send the email?")
                speak("Are you sure you don't want to send the email?")
                choice = listen()
                if choice == "yes" or "Yes" or "YES":
                    print("Email not sent.")
                    speak("Email not sent.")
                else:
                    print("Do you want to save the email as a draft?")
                    speak("Do you want to save the email as a draft?")
                    choice = listen()
                    if choice == "yes" or "Yes" or "YES":
                        # Save the email as a draft
                        with open("draft.txt", "w") as file:
                            file.write(f"To: {to}\n")
                            file.write(f"Subject: {subject}\n")
                            file.write(f"Body: {body}\n")
                        print("Email saved as draft!")
                        speak("Email saved as draft!")
        
        elif "send email" in command:
            print("You said: Send Email")
            speak("You said: Send Email")
            drafts = os.listdir()
            draft_files = [file for file in drafts if file.endswith(".txt")]
            if len(draft_files) == 0:
                print("No drafts found.")
                speak("No drafts found.")
            else:
                print("Here are the available drafts:")
                speak("Here are the available drafts:")
                for i, file in enumerate(draft_files):
                    print(f"{i+1}. {file}")
                print("Please enter the number of the draft you want to send:")
                speak("Please enter the number of the draft you want to send:")
                choice = listen()
                num = name_number(choice)
                if num is None or num < 1 or num > len(draft_files):
                    print("Invalid number.")
                    speak("Invalid number.")
                else:
                    draft_file = draft_files[num-1]
                    with open(draft_file, "r") as file:
                        draft_content = file.read()
                    print("Do you want to send this draft?")
                    speak("Do you want to send this draft?")
                    choice = listen()
                    if choice == "yes":
                        # Extract the email details from the draft content
                        lines = draft_content.split("\n")
                        to = lines[0].replace("To: ", "")
                        subject = lines[1].replace("Subject: ", "")
                        body = lines[2].replace("Body: ", "")
                        send_email(to, subject, body)
                        print("Email sent successfully!")
                        speak("Email sent successfully!")
                    else:
                        print("Email not sent.")
                        speak("Email not sent.")
        
        elif "add contact" in command:
            print("You said: Add Contact")
            speak("You said: Add Contact")
            print("What is the name of the contact?")
            speak("What is the name of the contact?")
            name = listen()
            print("What is the email of the contact?")
            speak("What is the email of the contact?")
            email = input()
            add_contact(name, email)
        
        elif "delete contact" in command:
            print("You said: Delete Contact")
            speak("You said: Delete Contact")
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
            print("You said: Remove all contacts")
            speak("You said: Remove all contacts")
            remove_all_contacts()
            print("All contacts removed successfully!")
            speak("All contacts removed successfully!")        
        
        elif "show contacts" in command:
            print("You said: Show Contacts")
            speak("You said: Show Contacts")
            print("Here are your contacts:")
            speak("Here are your contacts:")
            show_contacts()
        
        elif "exit" in command:
            print("You said: Exit")
            speak("You said: Exit")
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
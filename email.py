import hashlib  
import json  
import os  
import datetime

class User:  
    def __init__(self, username, password, is_admin=False):  
        self.username = username
        self.password = password 
        self.is_admin = is_admin  
        self.inbox = []  
        self.sent_emails = []  


    def add_email(self, email):  
        self.inbox.append(email)  

    def add_sent_email(self, email):  
        self.sent_emails.append(email)  

    def view_sent_emails(self):  
        if self.sent_emails:  
            print(f"Sent emails from {self.username}:")  
            for email in self.sent_emails:  
                print(email)  
        else:  
            print(f"No sent emails from {self.username}.")  


class Email:  
    def __init__(self, sender, receiver, text):  
        self.sender = sender  
        self.receiver = receiver  
        self.text = text  

    def __str__(self):  
        return f"From: {self.sender}, To: {self.receiver}, Text: {self.text}"  

class EmailSystem:  
    def __init__(self):  
        self.users = {}  
        self.emails = []  
        self.load_users_and_emails_from_file('email.json')  
        self.create_admin_if_not_exists()  

    def load_users_and_emails_from_file(self, filename):  
        if os.path.exists(filename):  
            try:  
                with open(filename, 'r') as f:  
                    data = json.load(f)  
                    self.users = {item['username']: User(item['username'], item['password'], item['is_admin'])  
                                  for item in data['users']}  
                    self.emails = data.get('emails', [])  
            except json.JSONDecodeError:  
                print(f"Error decoding JSON from {filename}. Creating a new file.")  
                self.save_users_and_emails_to_file(filename)  
        else:  
            print(f"{filename} does not exist. Creating a new file.")  
            self.save_users_and_emails_to_file(filename)  

    def save_users_and_emails_to_file(self, filename):  
        data = {  
            'users': [{'username': user.username, 'password': user.password, 'is_admin': user.is_admin}  
                      for user in self.users.values()],  
            'emails': self.emails,  
        }  
        with open(filename, 'w') as f:  
            json.dump(data, f)  

    def register(self, username, password):  
        if username in self.users:  
            print("Username already exists.")  
            return  
        is_admin = len(self.users) == 0  
        new_user = User(username, hashlib.sha256(password.encode()).hexdigest(), is_admin)  
        self.users[username] = new_user  
        print(f"User {username} registered successfully.")  

    def is_admin(self, user):  
        return user.is_admin  

    def create_admin_if_not_exists(self):  
        if 'admin' not in self.users:  
            admin_user = User(username='admin', password='admin', is_admin=True)  
            self.users[admin_user.username] = admin_user  
            print("Admin user created.")  

            self.save_users_and_emails_to_file('email.json')  

    def login(self, username, password):  
        user = self.users.get(username) 
        passwords =  hashlib.sha256(password.encode()).hexdigest()
        if user and user.password == passwords:  
            print(f"User {username} logged in successfully.")  
            return user  
        else:  
            print("Invalid username or password.")  
            return None  

    def send_email(self, sender, receiver_username, text):  
        receiver = self.users.get(receiver_username)  
        if receiver:  
            email = Email(sender.username, receiver_username, text)  
            receiver.add_email(email)  
            sender.add_sent_email(email)  
            self.emails.append({'sender': sender.username, 'receiver': receiver_username, 'text': text,'time':datetime.datetime.now()})  
            print(f"Email successfully sent to {receiver_username}.")  
        else:  
            print("Receiver not found.")  

    def view_inbox(self, user):  
        if user.inbox:  
            print(f"Inbox for {user.username}:")  
            for email in user.inbox:  
                print(email)  
        else:  
            print(f"Inbox for {user.username} is empty.")  

    def change_password(self, username, current_password, new_password):  
        user = self.users.get(username)  
        hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()  
        if user and user.password == hashed_current_password:  
            user.password = hashlib.sha256(new_password.encode()).hexdigest()  
            print("Password changed successfully.")  
        else:  
            print("Current password is incorrect or user does not exist.")  


def main():  
    email_system = EmailSystem()  

    while True:  
        username = input('Enter username: ')  
        password = input('Enter password: ')  
        user = email_system.login(username, password)  
        if not user:  
            continue

        
        if email_system.is_admin(user):  
            while True:  
                print("\nAdmin Menu:")  
                print("1. Register a new user")  
                print("2. Logout")  
                print("3. Exit")  
                
                choice = input("Choose an option: ")  

                if choice == '1':  
                    new_username = input('Enter username to register: ')  
                    new_password = input('Enter password to register: ')  
                    email_system.register(new_username, new_password)  
                elif choice == '2':  
                    print("Logged out.")  
                    break  
                elif choice == '3':  
                    print("Exiting the program.")  
                    email_system.save_users_and_emails_to_file('email.json') 
                    return  
                else:  
                    print("Invalid choice. Please try again.")  
        else:  
            while True:  
                print("\nUser Menu:")  
                print("1. Send Email")  
                print("2. View Inbox")  
                print("3. View Sent Emails")  
                print("4. Logout")  
                print("5. Exit")  
                print("6.change password")

                user_choice = input("Choose an option: ")  

                if user_choice == '1':  
                    receiver_username = input('Send to: ')  
                    text = input('Text: ')  
                    email_system.send_email(user, receiver_username, text)  

                elif user_choice == '2':  
                    email_system.view_inbox(user)  

                elif user_choice == '3':  
                    user.view_sent_emails()  

                elif user_choice == '4':  
                    print("Logged out.")  
                    break  
                elif user_choice == '5':  
                    print("Exiting the program.")  
                    email_system.save_users_and_emails_to_file('email.json') 
                    return  
                elif user_choice == '6':  
                    current_password = input("Enter current password: ")  
                    new_password = input('Enter new password: ')  
                    email_system.change_password(user.username, current_password, new_password)  
                
                else:  
                    print("Invalid choice. Please try again.")  

if __name__ == "__main__":  
    main()
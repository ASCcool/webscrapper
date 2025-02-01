import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class NotificationManager:
    def __init__(self, send_email=False):
        """
        Initialize notification settings
        """
        self.send_email = send_email
        self.sender_email = os.getenv("GMAIL_SENDER")
        self.app_password = os.getenv("GMAIL_APP_PASSWORD")
        self.receiver_email = os.getenv("NOTIFICATION_EMAIL")

    def send_notification(self, scraped_count, pages):
        """
        Notify about scraping results
        """
        message = f"Scraping Completed: {scraped_count} products scraped across {pages} pages and updated the DB"
        self.__print_to_console__(message)

        # Send Email if enabled
        if self.send_email:
            self.__send_email__(message)

    def __print_to_console__(self, message):
        """
        Print to Console
        """
        print(message)

    def __send_email__(self, message):
        """
        Send email notification via Gmail SMTP
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email
            msg["Subject"] = "Scraping Notification"

            msg.attach(MIMEText(message, "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            server.quit()

            print(f"Email sent to {self.receiver_email}")
        except Exception as e:
            print(f"Email notification failed: {e}")

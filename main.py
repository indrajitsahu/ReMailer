# Automated Subscription Renewal Email System

import pyodbc
import config
import smtplib
import requests
import asyncio
from email.message import EmailMessage
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AutomatedEmailSubscriptionModel")

@mcp.prompt()
def build_connection_string():
    return (
        f"DRIVER={config.DB_DRIVER};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_NAME};"
        f"UID={config.DB_USERNAME};"
        f"PWD={config.DB_PASSWORD};"
    )

@mcp.tool()
def send_email(email_string, subject, body):
    """Sends an email to a email addresse which is string parameter with the specified subject and body."""
    """:param email_string: email addresses which is a string is passed here to send the email to
        :param subject: Subject of the email
        :param body: Body of the email"""
    msg = EmailMessage()
    msg['From'] = config.FROM_EMAIL
    msg['To'] = email_string
    msg['Subject'] = subject
    msg.set_content(body)
    
    # Mark as important
    msg['X-Priority'] = '1'
    msg['X-MSMail-Priority'] = 'High'
    msg['Importance'] = 'High'

    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"Email sent to {email_string}")

@mcp.tool()
def send_email(email_tuple, subject, body):
    """Sends an email to a list of email addresses which are enclosed in tuple with the specified subject and body."""
    """:param email_tuple: Tuple of email addresses to send the email to
        :param su   bject: Subject of the email
        :param body: Body of the email"""
    for email in email_tuple:
        msg = EmailMessage()
        msg['From'] = config.FROM_EMAIL
        msg['To'] = email
        msg['Subject'] = subject
        msg.set_content(body)
        
        # Mark as important
        msg['X-Priority'] = '1'
        msg['X-MSMail-Priority'] = 'High'
        msg['Importance'] = 'High'

        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Email sent to {email}")

@mcp.tool()
def get_expired_users() :
    """Users with expired subscriptions, send them renewal email"""
    try:
        with pyodbc.connect(build_connection_string()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT u.Name, u.Email FROM Users u JOIN Subscription s ON u.Id = s.UserId WHERE s.ExpiryDate < GETDATE() AND u.IsActive = 1 AND s.IsActive = 0")
                return cursor.fetchall()
    except Exception as e:
        print(f"Connection or query failed: {e}")

@mcp.tool()
async def get_all_users() :
    """Send mail to all users with global message"""
    try:
        with pyodbc.connect(build_connection_string()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT Name, Email FROM Users")
                return cursor.fetchall()
    except Exception as e:
        print(f"Connection or query failed: {e}")

@mcp.tool()
def get_inactive_users_with_due() :
    """Users who haven't logged in in 30+ days and still owe money"""
    try:
        with pyodbc.connect(build_connection_string()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT u.Name, u.Email FROM Users u WHERE DATEDIFF(DAY, u.LastLoginDate, GETDATE()) > 30 AND u.DueAmount > 0 AND u.IsActive = 1")
                return cursor.fetchall()
    except Exception as e:
        print(f"Connection or query failed: {e}")

@mcp.tool()
def get_active_users_with_due() :
    """Users with active subscriptions but payment due"""
    try:
        with pyodbc.connect(build_connection_string()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT u.Name, u.Email, s.PlanName, s.AmountPaid FROM Users u JOIN Subscription s ON u.Id = s.UserId WHERE s.IsActive = 1 AND u.DueAmount > s.AmountPaid AND u.IsActive = 1")
                return cursor.fetchall()
    except Exception as e:
        print(f"Connection or query failed: {e}")

@mcp.tool()
def get_new_users_with_no_subscription() :
    """New users with no subscription yet and No entries in Subscription for these users"""
    try:
        with pyodbc.connect(build_connection_string()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT u.Name, u.Email FROM Users u LEFT JOIN Subscription s ON u.Id = s.UserId WHERE s.UserId IS NULL")
                return cursor.fetchall()
    except Exception as e:
        print(f"Connection or query failed: {e}")

@mcp.tool()
def get_all_users_with_due() :
    """all users with due amount and amount greater than 0"""
    try:
        with pyodbc.connect(build_connection_string()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT u.Name, u.Email FROM Users u WHERE u.ConditionField = 'due' AND u.DueAmount > 0")
                return cursor.fetchall()
    except Exception as e:
        print(f"Connection or query failed: {e}")

@mcp.tool()
def get_all_upcoming_expiry_users() :
    """Users with subscriptions expiring in next 7 days"""
    try:
        with pyodbc.connect(build_connection_string()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT u.Name, u.Email, s.ExpiryDate FROM Users u JOIN Subscription s ON u.Id = s.UserId WHERE s.ExpiryDate BETWEEN GETDATE() AND DATEADD(DAY, 7, GETDATE()) AND s.IsActive = 1")
                return cursor.fetchall()
    except Exception as e:
        print(f"Connection or query failed: {e}")

@mcp.tool()
def get_premium_users() :
    """Users on 'Premium' plan who are still active"""
    try:
        with pyodbc.connect(build_connection_string()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT u.Name, u.Email, s.PlanName FROM Users u JOIN Subscription s ON u.Id = s.UserId WHERE s.PlanName = 'Premium' AND u.IsActive = 1 AND s.IsActive = 1")
                return cursor.fetchall()
    except Exception as e:
        print(f"Connection or query failed: {e}")

if __name__ == "__main__":
    print("Email Sender MCP Server is running...")
    mcp.run()

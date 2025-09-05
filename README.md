# Remailer – Automated Subscription Renewal Emailer  

## About  
Automated Subscription Renewal Emailer built with **Python**, **SMTP**, and **Azure SQL DB**.  
It securely sends **personalized, high-priority emails** to single or multiple recipients.  
Easily configurable through `.env` and `config.py` for quick deployment.  

## Features  
- 📧 Automated email delivery with **SMTP**  
- 🔑 Configurable authentication via `.env` & `config.py`  
- 🗄️ **Azure SQL Database** integration for dynamic queries  
- ⚡ **MCP Server integration** with Claude Desktop via `uv`  
- 🎯 Multiple targeting tools:  
  - Expired subscriptions  
  - Upcoming renewals  
  - Inactive users with dues  
  - Premium plan users  
  - New users without subscriptions  
- 🚨 Emails marked as **High Priority**  
- ✅ Supports both **single** and **bulk recipients**  

## Tech Stack  
- **Python 3.13+**  
- **uv** – package & MCP manager  
- **pypyodbc** – SQL Server connector  
- **smtplib** – SMTP mail sender  
- **mcp.server.fastmcp** – MCP server integration  
- **Azure SQL Database**  

## Setup  

### 1. Clone repository  
```bash
git clone https://github.com/your-username/repo-name.git
cd repo-name
```

### 2. Configure environment

#### Create a .env file in the root directory:
```
DB_SERVER=your-sql-server
DB_NAME=your-database
DB_USERNAME=your-username
DB_PASSWORD=your-password

SMTP_SERVER=smtp.example.com
SMTP_PORT=587
EMAIL_USERNAME=your@email.com
EMAIL_PASSWORD=yourpassword
```

### 3. Install MCP server with uv
```bash
uv run mcp install main.py
```

### 4. Run MCP server
```bash
uv run main.py
```


You should see:

```bash
Email Sender MCP Server is running...
```

#### Usage

Once installed, connect it to Claude Desktop client.
You can then issue natural language prompts like:

Send renewal emails to expired users
List users with upcoming subscription expiry
Notify inactive users with pending dues

#### Roadmap

- Add retry logic & logging for failed emails
- Enhance async database queries
- UI dashboard for tracking email history
- Docker container support

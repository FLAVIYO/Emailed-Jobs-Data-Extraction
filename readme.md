# Emailed Jobs Data Extraction Script

This Python script connects to your email server, searches both the **Inbox** and **Spam** folders for job-related emails, extracts key details, and displays them in a neatly formatted table using Pandas. This can help you keep track of job opportunities by consolidating all relevant emails into one structured view.

## Features

- Connects securely to an IMAP-compatible email server.
- Searches for job-related keywords (e.g., "job," "opportunity," "position") in both **Inbox** and **Spam** folders.
- Extracts key details from each job-related email:
  - **Job Title**
  - **Application Link**
  - **Sender (Source)**
  - **Subject Line**
  - **Date**
- Displays extracted information in a neatly formatted table using Pandas.

## Prerequisites

- **Python 3.x**
- **Pandas library** (for table formatting)
- **IMAP access** enabled for your email account
- **An .env file** containing your email credentials (see Setup)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/FLAVIYO/Emailed-Jobs-Data-Extraction.git
   cd Emailed-Jobs-Data-Extraction
   ```
2. Install the required libraries:
   ```bash
   pip install pandas python-dotenv
   ```
3. Create a .env file in the root directory to store your email credentials:
   ```bash
   EMAIL =
   PASSWORD = #this is the "app password" from gmail account setting
   ```   
## Usage

```bash
python main.py
 ```

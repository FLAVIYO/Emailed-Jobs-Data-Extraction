import email
from email.policy import default
import imaplib
import os
import pandas as pd
from dotenv import load_dotenv

#laod .env file
load_dotenv()

def load_credentails():
    '''get credentials from .env file'''
    my_email = os.getenv("EMAIL")
    my_password = os.getenv("PASSWORD")

    if not my_email or not my_password:
        raise ValueError("you tryna be smart huhh, get out of here")
    print(my_email)
    return my_email, my_password

load_credentails()

def connect_to_meail_server():
    '''Establish a connection to the gmail server'''
    my_email ,my_password = load_credentails()
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(my_email,my_password)
        print('successfully connected to gmail server')
        return mail
    except imaplib  .IMAP4.error as e:
        print('Failed to connect to the server', e)
        return None

connect_to_meail_server()

def access_folder(mail,folder_name):
    '''select the  fonder'''
    try:
        status ,messages = mail.select(folder_name)
        if status == "OK":
            print( f"successfully accessed {folder_name} folder")
            print(messages)
            return messages
        else:
            print( f"failded to access the {folder_name} folder")
    except Exception as e:
        print(f"errer accessing {folder_name} folder",e)  
        return None

def search_job_emails(mail):
    '''seach for job-related emails in the folders'''
    job_keywords = ['job', 'opportunity', 'position','career']

    for keyword in job_keywords:
        status, data = mail.search(None, f'(BODY "{keyword}")')
        if status == "OK":
            email_ids = data[0].split()
            if email_ids:
                print(f"found {len(email_ids)} job-related emails with keyword '{keyword}' ")
            else:
                print(f"No job-related emails found with keyword '{keyword}'")  
    return list(set(email_ids))             

def fetch_email_details(mail, email_id):
    '''fetch an d parse email content to extract job details'''
    status , data = mail.fetch(email_id, '(RFC822)')
    if status != 'OK':
        print(f"failed to fetch email with ID {email_id}")
        return None
    
    #parse email content
    msg = email.message_from_bytes(data[0][1], policy=default)
    email_details = {
        "subject": msg["subject"],
        "from": msg["from"],
        "date": msg["date"],
        "job_title": None,
        "link": None,
    }


    # Extract job title and link from the email content
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                content = part.get_content().strip()
                email_details.update(extract_job_info(content))
    else:
        content = msg.get_content().strip()
        email_details.update(extract_job_info(content))

    return email_details

def extract_job_info(content):
    """Extract job title and link from email content based on keywords and patterns."""
    job_info = {"Job Title": None, "Link": None}

    # Basic pattern matching for job title
    title_keywords = ["Position:", "Job Title:", "Opportunity:", "Role:"]
    for line in content.splitlines():
        for keyword in title_keywords:
            if keyword in line:
                job_info["Job Title"] = line.replace(keyword, "").strip()

    # Basic pattern matching for links, excluding irrelevant links
    if "http" in content:
        link_start = content.find("http")
        link_end = content.find(" ", link_start)
        link = content[link_start:link_end].strip()

        # Exclude unwanted links like the XHTML DTD reference
        if "w3.org" not in link:
            job_info["Link"] = link

    return job_info


def close_connection(mail):
    '''logout and close the connectoing to the mail server'''
    if mail :
        try:
            mail.logout()
            print("Disconnected to the server")
        except Exception as e :
            print("error during logout")    

# Main script execution
if __name__ == "__main__":
    mail = connect_to_meail_server()
    if mail:
        # Access the inbox and junk folders
        access_folder(mail, "INBOX")
        job_emails_inbox = search_job_emails(mail)
        access_folder(mail, "[Gmail]/Spam")  # Adjust folder name as needed
        job_emails_junk = search_job_emails(mail)

        # Collect email details for job-related emails
        all_job_emails = job_emails_inbox + job_emails_junk
        email_details_list = []
        for email_id in all_job_emails:
            details = fetch_email_details(mail, email_id)
            if details:
               email_details_list.append(details)

        # Use Pandas to create a DataFrame and display the details
        df = pd.DataFrame(email_details_list)
        print("\nJob-Related Emails:\n")
        print(df)

        close_connection(mail)
                










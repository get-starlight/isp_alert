import requests
from bs4 import BeautifulSoup
import hashlib
from email.message import EmailMessage
import ssl
import smtplib
from passwords import my_password


isps = ["optimum", "verizon", "spectrum", "xFinity"]

isp_url = {
    "verizon": 'https://www.verizon.com/home/acp/',
    "optimum": "https://www.optimum.com/affordable-connectivity-program",
    "spectrum": "https://www.spectrum.com/cp/broadband-get-qualified",
    "xFinity": "https://www.xfinity.com/learn/internet-service/acp/free-internet#gbb"
}

isp_identifier = {
    "verizon": ["div", "fios-home"], # tag, class
    "optimum": ["div", "compare-plan-scale"],
    "spectrum": ["div", "imageSuperHero"],
    "xFinity": ["div", "xds-gbb-cards__main-wrapper"]
}


def siteChanged(isp):
    url = isp_url[isp]
    # https://stackoverflow.com/questions/51154114/python-request-get-fails-to-get-an-answer-for-a-url-i-can-open-on-my-browser
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e: # if website doesn't respond, treat as if content changed
        return True
        
    soup = BeautifulSoup(response.content, 'html.parser')

    content = soup.find_all(isp_identifier[isp][0],class_=isp_identifier[isp][1])
    content = "".join([str(tag) for tag in content])
    
        
        
        # Check if the content has changed
    previous_content = ''

    try:
        with open(f"{isp}.txt", 'r', encoding='utf-8') as f:
            previous_content = f.read()
        
    except FileNotFoundError:
        pass

    # using hash function to check if html has changed, instead of dealing with whitespace discrepancies in strings
    # https://stackoverflow.com/questions/65693836/how-to-detect-changes-on-website-python-web-scraping
    # content might be None if class name has been changed
    new_content=hashlib.sha256(content.encode('utf-8')).hexdigest() if content else hashlib.sha256(soup.encode('utf-8')).hexdigest()
    

    if new_content != previous_content:
            # Save the new content
        with open(f"{isp}.txt", 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"{isp} changed")
        
    else:
        print(f"{isp} same")
    
    return new_content != previous_content





    # Send email notification
        # Tutorial:
            # https://www.youtube.com/watch?v=zxFXnLEmnb4&ab_channel=CodeWithTomi

email_list = []

for isp in isps:
    if siteChanged(isp):
        email_list.append(isp)



if email_list:
    email_sender = "your_email@gmail.com" # Replace with your email address
    email_password = my_password # Replace with app password, NOT email password
                                        # more details in tutorial above
    email_receiver = "recipient_email@example.com" # # Replace with the recipient email address
    
    sites = "\n"
    for isp in email_list:
        sites += isp_url[isp]
        sites += "\n"
    
    subject = f"The contents of {', '.join(email_list)} changed"
    body = f"Please check the webpages: {sites}"
      
    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        
        
    
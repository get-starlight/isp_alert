# Isp_alert

This Python script uses BeautifulSoup to scrape the HTML contents of four ISP websites - Verizon, Optimum, Spectrum, and xFinity. It then reads from a file that contains the contents from a previous scraping and compares them to see if the websites have been modified. If any updates were made, the script makes a list of the sites that have changed and sends an email to a receiver to notify them of which sites have been updated.

## Installation
1. Clone or download this repository to your local machine.
2. Make sure you have Python 3.x installed.
3. Install the required packages by running pip install -r requirements.txt in your terminal or command prompt.

## Usage
1. To run the script, navigate to the directory where the script is saved.
2. Open the alert.py file in your preferred code editor.
3. Replace the email_sender, email_password, and email_receiver fields with your own email credentials and recipient email address. The email_password uses an app password, which is NOT the same as your gmail password. Follow the steps of "Setting up passwords.py" to learn how to generate an app password through gmail.
4. Run the script by typing "python alert.py" in your terminal or command prompt.


## Setting up passwords.py
1. Create a new file named passwords.py in the same directory as the main script.
2. Follow [this](https://www.youtube.com/watch?v=zxFXnLEmnb4&ab_channel=CodeWithTomi) tutorial to generate an app password.
3. In the passwords.py file, create the variable "my_password" that holds your password as a string (e.g. my_password = "my_secret_password").


## Configuration
The script is configured to scrape the HTML contents of four different websites - Verizon, Optimum, Spectrum, and xFinity. If you want to add more websites to the script, you can do so by adding an entry to the isp_url and isp_identifier dictionaries.

The isp_url dictionary contains the URLs for the websites you want to scrape. The key is a string that identifies the website, and the value is the website's URL.

The isp_identifier dictionary contains the tag and class that identifies the content you want to monitor. The key is the same string identifier used in the isp_url dictionary, and the value is a list containing the tag and class.

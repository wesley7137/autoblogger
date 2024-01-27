import requests
from bs4 import BeautifulSoup

# Paste the scraping functions here

import smtplib
from email.message import EmailMessage
import requests
from bs4 import BeautifulSoup
import os
from email.message import EmailMessage
import smtplib
from bs4 import BeautifulSoup
import csv
all_articles = []



def write_results_to_file(scraped_article_results, filename='scraped_results.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["", "Number", "Title", "Link", "Summary"])  # Write the header
        for i, article in enumerate(scraped_article_results, start=1):
            writer.writerow(["", i, article['title'], article['link'], article.get('summary', 'No summary available')])
    return filename


def send_email(subject, body, recipient, attachment_path, reply_to):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'weslagarde@gmail.com'  # Your sending email
    msg['To'] = recipient
    msg['Reply-To'] = reply_to  # Set the Reply-To header

    # Set the email body
    msg.set_content(body)

    # Attach the file if attachment_path is not None
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  # Gmail's SMTP server
        smtp.login('weslagarde@gmail.com', 'sayy iefr pqqk mvay')  # Replace with your email and app password
        smtp.send_message(msg)
        


def scrape_kdnuggets():
    url = "https://www.kdnuggets.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    count = 0
    max_articles = 5

    for li in soup.find_all("li", class_="li-has-thumb"):
        if count >= max_articles:
            break

        title_tag = li.find("a")
        title = title_tag.get_text(strip=True) if title_tag else "No title"
        link = title_tag['href'] if title_tag else "No link"
        summary_tag = li.find("p")
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

        articles.append({"title": title, "link": link, "summary": summary})
        count += 1

    return articles


def scrape_ai_news():
    url = "https://www.artificialintelligence-news.com/categories/ai-deep-reinforcement-learning/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    count = 0
    max_articles = 5

    for article in soup.find_all("div", class_="cb-post-title"):
        if count >= max_articles:
            break

        title = article.find("h2")
        link = title.find("a")["href"] if title else None

        if title and link:
            articles.append({"title": title.text.strip(), "link": link})
            count += 1

    return articles

def scrape_techcrunch_ai():
    url = "https://techcrunch.com/category/artificial-intelligence/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    count = 0
    max_articles = 5

    for article in soup.find_all("div", class_="post-block"):
        if count >= max_articles:
            break

        title = article.find("a", class_="post-block__title__link")
        link = title.get("href", None) if title else None
        summary = article.find("div", class_="post-block__content").text.strip() if article.find("div", class_="post-block__content") else ""

        if title and link:
            articles.append({"title": title.text.strip(), "link": link, "summary": summary})
            count += 1

    return articles


def scrape_medium_ai_articles():
    # Define the URL of the site
    url = "https://medium.com/tag/artificial-intelligence/recommended"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all article entries - adjust the class as needed
    articles = soup.find_all('a', {'rel': 'noopener follow'})
    
    # Initialize a list to store scraped data
    scraped_articles = []
    
    # Loop through all found article entries
    for article in articles:
        title = article.find('h2')
        subtitle = article.find('h3')
        link = article['href']
        if title and subtitle and link:
            scraped_articles.append({
                'title': title.text.strip(),
                'subtitle': subtitle.text.strip(),
                'link': f"https://medium.com{link}"
            })
    
    return scraped_articles

# Function to write article mapping to a CSV file
def save_article_mapping(article_mappings, filename='article_mapping.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Number', 'Title', 'Link', 'Summary'])  # Header row
        for article in article_mappings:
            writer.writerow([article['number'], article['title'], article['link'], article.get('summary', 'No summary available')])
            print("Saved article mapping to CSV file.")
# Your existing function to aggregate articles


def aggregate_articles():
    all_articles = []
    # Call each scraping function and extend the all_articles list
    all_articles.extend(scrape_kdnuggets())
    all_articles.extend(scrape_techcrunch_ai())
    all_articles.extend(scrape_medium_ai_articles())
    all_articles.extend(scrape_ai_news())
    # Assign a unique number to each article
    for i, article in enumerate(all_articles, start=1):
        article['number'] = i
    print(f"Found {len(all_articles)} articles.")
    return all_articles


# Main execution
# Main execution
def article_scraper():
    print("[START] Running Article Fetch and Summarize")
    all_articles = aggregate_articles()
    
    if not all_articles:
        print("No articles found. Exiting application.")
        exit()
        
    # Save the article mapping to a CSV file; no need to capture a return value as it doesn't return anything
    save_article_mapping(all_articles, filename='article_mapping.csv')
    
    # Write the results to a file and capture the filename to send as an attachment
    file_to_send = write_results_to_file(all_articles)

    subject = "Daily AI Articles Scraping Results: ATTENTION!!!!"
    body = "Attached is the daily report of AI articles scraped from various sources."
    recipient = 'weslagarde@gmail.com'  # Replace with the recipient's email address
    reply_to_address = 'weslagarde@gmail.com'  # Your Zapier email parser address
    
    # Call send_email with the corrected arguments
    send_email(subject, body, recipient, file_to_send, reply_to_address)
    print("Email sent successfully.")
    return all_articles

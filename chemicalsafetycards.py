import requests
import random
import time
from bs4 import BeautifulSoup

def extract_links_and_names(url):
    """
    Extracts chemical names and their corresponding links from a table on a webpage.
    
    Parameters:
        url (str): The URL of the webpage containing the table.
    
    Returns:
        list of tuples: A list where each tuple contains (ID, URL, Chemical Name).
    """
    # Send a GET request to fetch the HTML content from the provided URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        html_content = response.text  # Get the HTML content from the response
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all rows in the table (excluding the first empty row)
        rows = soup.find_all('tr', valign="top")
        
        # List to hold the extracted data (ID, URL, Chemical Name)
        link_data = []
        
        # Iterate over each row to extract the ID, link, and name
        for row in rows:
            cells = row.find_all('td')
            
            if len(cells) > 1:  # Make sure there are at least two cells in the row
                # Extract the link (ID) and URL from the first cell
                link = cells[0].find('a')
                if link:
                    link_id = link.get_text()  # Text inside the <a> tag (the ID)
                    link_url = link.get('href')  # href attribute of the <a> tag (the URL)
                    
                    # Extract the chemical name from the second cell
                    chemical_name = cells[1]
                    index_of_br = str(chemical_name).find('<br/>')
                    index_of_td = str(chemical_name).find('</td>')
                    if index_of_br == -1:
                        chemical_name = chemical_name.get_text(strip=True)
                    else:
                        chemical_name = str(chemical_name)[4:index_of_br]
            
                    # Handle the case where there is additional text inside a <span> element
                    #span = cells[1].find('span')
                    #if span:
                    #    additional_names = span.get_text(strip=True)
                    #    chemical_name += "; " + additional_names
                    
                    # Append the extracted data as a tuple (ID, URL, Chemical Name)
                    link_data.append((link_id, link_url, chemical_name))
        
        return link_data  # Return the list of extracted link data
    
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []  # Return an empty list in case of failure



if __name__ == "__main__":
    url = "https://chemicalsafety.ilo.org/dyn/icsc/showcard.listcards3?p_lang=enp"  # Replace with the actual URL
    data = extract_links_and_names(url)
    root = "https://chemicalsafety.ilo.org"
    # Print the extracted data
    if data:
        for link_id, link_url, chemical_name in data:
            try:
                time.sleep(random.randint(2,5))
                response = requests.get(root+link_url)
                if response.status_code == 200:
                    html_content = response.text
                    f = open("chemicals/"+str(chemical_name).title(), "a")
                    f.write(html_content)
                    f.close()
                else:
                    print("Failed to fetch the webpage.")
            except Exception as e:
                    # Handle the exception
                    print(f"An error occurred: {e}")
    else:
        print("No data extracted.")

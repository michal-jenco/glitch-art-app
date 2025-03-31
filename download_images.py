import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time


def download_images(search_query, num_images=50, folder_name="images"):
    # Create a folder to store images
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Format search query for the URL
    search_query = urllib.parse.quote_plus(search_query)

    # Construct the Google Image search URL
    base_url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_query}"

    # Set user-agent to avoid being blocked by Google
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    image_count = 0
    page_num = 0  # Start from the first page

    while image_count < num_images:
        # Construct the URL for the next page (start=20 for page 2, start=40 for page 3, etc.)
        url = base_url + f"&start={page_num * 20}"

        # Send a GET request to Google Images
        response = requests.get(url, headers=headers)

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the image tags
        img_tags = soup.find_all("img")

        # Loop through the image tags and download the images
        for img_tag in img_tags[1:]:  # Skip the first image (it's a small placeholder image)
            try:
                # Get the image URL
                img_url = img_tag.get("src")

                if img_url:
                    # Download the image content
                    img_data = requests.get(img_url).content

                    # Create a file path to save the image
                    img_filename = os.path.join(folder_name, f"{search_query}_{image_count + 1}.jpg")

                    # Save the image to the folder
                    with open(img_filename, 'wb') as f:
                        f.write(img_data)

                    print(f"Downloaded {img_filename}")
                    image_count += 1

                    # Stop once we have downloaded the desired number of images
                    if image_count >= num_images:
                        break

            except Exception as e:
                print(f"Error downloading image: {e}")

        # Increment the page number to load the next set of results
        page_num += 1

        # To avoid being blocked, add a small delay between requests
        time.sleep(2)

    print(f"Downloaded {image_count} images.")

prompt = "osaka azumanga daioh"
# Example usage
download_images(prompt, num_images=50, folder_name=prompt)
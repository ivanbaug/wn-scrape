import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}


def get_page_txt(site_url):
    """Uses requests library to get text from the url
    It also catches the most common errors and stores them in an error list to check which likns failed later"""
    try:
        response = requests.get(site_url, headers=headers)
        response.raise_for_status()
        # print(f"statuscode:{response.status_code}")
        return response.text
    except requests.exceptions.ConnectionError:
        # wrong_links.append(site_url)
        print(f"Failed to load the following link: {site_url}")
    except requests.exceptions.HTTPError:
        # wrong_links.append(site_url)
        print(f"Failed to load the following link: {site_url}")
    return None

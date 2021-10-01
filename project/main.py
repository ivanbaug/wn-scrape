import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from dotenv import load_dotenv

out_folder = "output/"
load_dotenv()
main_url = os.getenv("SITE_URL")
print(main_url)
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}


wrong_links = []


def get_page_txt(site_url):
    """Uses requests library to get text from the url
    It also catches the most common errors and stores them in an error list to check which likns failed later"""
    try:
        response = requests.get(site_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.ConnectionError:
        wrong_links.append(site_url)
        print(f"Failed to load the following link: {site_url}")
    except requests.exceptions.HTTPError:
        wrong_links.append(site_url)
        print(f"Failed to load the following link: {site_url}")
    return None


def save_ch_txt(ch_num: int):
    # get entire page
    site_url = f"{main_url}{ch_num}"
    wn_webpage = get_page_txt(site_url)
    soup = BeautifulSoup(wn_webpage, "html.parser")

    # get chapter data
    ch_title = soup.find("p", class_="novel_subtitle")
    novel_honbun = soup.find(id="novel_honbun")
    novel_afterword = soup.find(id="novel_a")

    with open(
        f"output/CH{ch_num:03d}-{dt.now().strftime('%Y%m%d-%H%M%S')}.txt",
        "w",
        encoding="utf8",
    ) as myfile:
        # Write title
        myfile.write(f"CHAPTER {ch_num}: {ch_title.text}\n")

        # Write paragraphs
        keep_trying = 3
        paragraph_id = 1
        while keep_trying:
            paragraph = novel_honbun.find(id=f"L{paragraph_id}")
            if paragraph == None:
                keep_trying -= 1
            else:
                myfile.write(paragraph.text + "\n")
            paragraph_id += 1
        # Write paragraphs
        keep_trying = 3
        afterword_id = 1
        myfile.write("----------\n")
        while keep_trying:
            aw = novel_afterword.find(id=f"La{afterword_id}")
            if aw == None:
                keep_trying -= 1
            else:
                myfile.write(aw.text + "\n")
            afterword_id += 1


save_ch_txt(1)


# soup = BeautifulSoup(wn_webpage, "html.parser")
# test_line = soup.find(id="L0")
# print(test_line)
# print(test_line == None)
# print(test_line.text)

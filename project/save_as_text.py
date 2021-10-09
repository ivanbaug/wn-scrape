import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime as dt
from shared_funcs import get_page_txt

out_folder = "output/"

load_dotenv()
main_url = os.getenv("SITE_URL")
print(main_url)


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
        # Write afterwords
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


if __name__ == "__main__":
    # Save raw chapters
    # for i in range(1, 678):
    for i in range(1, 3):
        save_ch_txt(i)

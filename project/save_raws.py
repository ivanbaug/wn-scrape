import os
from dotenv import load_dotenv
from datetime import datetime as dt
from shared_funcs import get_page_txt

load_dotenv()
main_url = os.getenv("SITE_URL")
print(main_url)

out_folder = "wn_jp_html/"


def save_ch_html(ch_num: int):
    # get entire page
    site_url = f"{main_url}{ch_num}"
    wn_webpage = get_page_txt(site_url)

    with open(
        f"{out_folder}CH{ch_num:03d}-{dt.now().strftime('%Y%m%d-%H%M%S')}.html",
        "w",
        encoding="utf8",
    ) as myfile:
        # Write title
        myfile.write(wn_webpage)


if __name__ == "__main__":
    # Save raw chapters
    for i in range(1, 678):
        # for i in range(1, 3):
        save_ch_html(i)

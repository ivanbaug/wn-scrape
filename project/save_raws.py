import os
from dotenv import load_dotenv
from datetime import datetime as dt
from shared_funcs import get_page_txt

load_dotenv()


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
    main_url = os.getenv("SITE_URL")
    out_folder = "wn_jp_html/"
    ch_start = 1
    ch_end = 128

    for i in range(ch_start, ch_end):
        # for i in range(1, 3):
        save_ch_html(i)

import os
from datetime import datetime as dt
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import string
import json
import re


def validate_payload(payload):
    """
    validate the target text to translate
    @param payload: text to translate
    @return: bool
    """
    # check if is string, is not empty string or contains only numbers
    if (
        not payload
        or not isinstance(payload, str)
        or not payload.strip()
        or payload.isdigit()
    ):
        return False

    # check if payload contains only symbols
    payload = payload.strip()
    if all(i in string.punctuation for i in payload):
        return False

    return True


def file_top(title):
    return f"""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
</head>
<body>
"""


def file_bottom():
    return "\n</body></html>"


def make_title(title):
    return f'<h1 class="chapter">{title}</h1>\n'


def make_paragraph(content):
    return f"<p>{content}</p>\n"


def make_afterword(chapter_id):
    return f"<h2>{chapter_id} Afterword:</h2>\n"


def replace_words_jp(text, word_dict):
    for entry in word_dict:
        if entry["active"]:
            text = text.replace(entry["repA"], entry["repB"])
    return text


def replace_words_en(text, word_dict):
    for entry in word_dict:
        if entry["active"]:
            insensitive_word = re.compile(re.escape(entry["repA"]), re.IGNORECASE)
            text = insensitive_word.sub(entry["repB"], text)
    return text


def paragraphs_to_list(soup_item, identifier):
    attempts = 3
    paragraph_id = 1
    p_list = []
    while attempts:
        paragraph = soup_item.find(id=f"{identifier}{paragraph_id}")
        if paragraph == None:
            attempts -= 1
        else:
            # Drop empty paragraphs and special character only paragraphs
            if validate_payload(paragraph.text):
                p_list.append(paragraph.text)
        paragraph_id += 1
    return p_list


def translate_list(p_list, en_dict, ja_dict):
    # Replace known japanese words
    for i, sentence in enumerate(p_list):
        p_list[i] = replace_words_jp(sentence, ja_dict)

    # Translate using translator services
    translated = GoogleTranslator(source="ja", target="en").translate_batch(p_list)

    # Correct known translation misspells
    en_list = []
    for sentence in translated:
        en_list.append(replace_words_en(sentence, en_dict))

    return en_list


def translate_multiple_ch(bk_name: str, ch_start=1, ch_end=2, raws_dir="wn_jp_html/"):
    # Get list of all files in the raws dir
    f = []
    for (dirpath, dirnames, filenames) in os.walk(raws_dir):
        f.extend(filenames)
        break

    # Open word dictionaries for replacements
    with open("project/dicts/jap_dict.json", "r", encoding="utf8") as d:
        ja_dict = json.load(d)["replacements"]
    with open("project/dicts/word_dict.json", "r", encoding="utf8") as d:
        en_dict = json.load(d)["replacements"]

    # Open and create output file
    with open(
        f"output/BOOK-{dt.now().strftime('%Y%m%d-%H%M%S')}.html",
        "w",
        encoding="utf8",
    ) as myfile:
        # Write html headers
        myfile.write(file_top(bk_name))
        # Iterate over desired chapters (remember lists start in 0)
        f_list = f[(ch_start - 1) : ch_end]
        for file_name in f_list:
            # Load raw file
            print(file_name)
            with open(f"{raws_dir}{file_name}", encoding="utf8") as fp:
                soup = BeautifulSoup(fp.read(), features="lxml")

            # Get chapter data
            ch_title = soup.find("p", class_="novel_subtitle")
            novel_honbun = soup.find(id="novel_honbun")
            novel_afterword = soup.find(id="novel_a")

            # Translate and write chapter title to file
            if validate_payload(ch_title.text):
                title_l = translate_list(
                    [ch_title.text], en_dict=en_dict, ja_dict=ja_dict
                )
                title = f"{file_name.split('-')[0]}: {title_l[0]}"
            else:
                title = f"{file_name.split('-')[0]}"
            myfile.write(make_title(title))

            # Write chapter content to file
            par_list = paragraphs_to_list(novel_honbun, "L")
            print(f"WN Sentences to translate: {len(par_list)}")
            if par_list:
                en_list = translate_list(par_list, en_dict=en_dict, ja_dict=ja_dict)
            for sentence in en_list:
                myfile.write(make_paragraph(sentence))

            # Write afterwords
            myfile.write(make_afterword(file_name.split("-")[0]))
            par_list = paragraphs_to_list(novel_afterword, "La")
            print(f"Afterword Sentences to translate: {len(par_list)}")
            if par_list:
                en_list = translate_list(par_list, en_dict=en_dict, ja_dict=ja_dict)
            for sentence in en_list:
                myfile.write(make_paragraph(sentence))

        # Write html file closing tags
        myfile.write(file_bottom())


if __name__ == "__main__":
    # Run translation - html crsation function
    # The resulting html is compatible with Calibre ebook indentation
    book_title = "Booklet 5.12"

    translate_multiple_ch(book_title, ch_start=42, ch_end=52)
    # 5.11 649-665
    # 5.12 666-677

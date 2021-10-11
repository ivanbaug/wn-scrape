import os
from datetime import datetime as dt
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import string
import json
import re

# translated = GoogleTranslator(source="ja", target="en").translate_batch(["...."])

# print(translated)


def validate_payload(payload):
    """
    validate the target text to translate
    @param payload: text to translate
    @return: bool
    """
    # check if is string, is not empry string or contains only numbers
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
    return f"""
<!DOCTYPE html>
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


def translate_list(p_list):
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


# Get list of all files in the raws dir
raws_dir = "wn_jp_html/"
f = []
for (dirpath, dirnames, filenames) in os.walk(raws_dir):
    f.extend(filenames)
    break

# Open word dictionaries to replace
with open("project/dicts/jap_dict.json", "r", encoding="utf8") as d:
    ja_dict = json.load(d)["replacements"]
with open("project/dicts/word_dict.json", "r", encoding="utf8") as d:
    en_dict = json.load(d)["replacements"]


with open(
    f"output/test_html-{dt.now().strftime('%Y%m%d-%H%M%S')}.html",
    "w",
    encoding="utf8",
) as myfile:
    # Write html headers
    myfile.write(file_top("Booklet 1"))
    # Iterate over desired chapters (temember lists start in 0)
    myef = [f[559]]
    for file_name in myef:
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
            title_l = translate_list([ch_title.text])
            title = f"{file_name.split('-')[0]}: {title_l[0]}"
        else:
            title = f"{file_name.split('-')[0]}"
        myfile.write(make_title(title))

        # Write chapter content to file
        par_list = paragraphs_to_list(novel_honbun)
        en_list = translate_list(par_list)

        for sentence in en_list:
            myfile.write(make_paragraph(sentence))
        # keep_trying = 3
        # paragraph_id = 1
        # while keep_trying:
        #     paragraph = novel_honbun.find(id=f"L{paragraph_id}")
        #     if paragraph == None:
        #         keep_trying -= 1
        #     else:
        #         if validate_payload(paragraph.text):
        #             # Replace known japanese words
        #             ja_paragr = replace_words_jp(paragraph.text, ja_dict)
        #             paragr = ja_paragr
        #         else:
        #             paragr = paragraph.text
        #         myfile.write(make_paragraph(paragr))
        #     paragraph_id += 1

        # Write afterwords
        myfile.write(make_afterword(file_name.split("-")[0]))
        par_list = paragraphs_to_list(novel_afterword)
        en_list = translate_list(par_list)

        for sentence in en_list:
            myfile.write(make_paragraph(sentence))
        # keep_trying = 3
        # afterword_id = 1
        # myfile.write(make_afterword(file_name.split("-")[0]))
        # while keep_trying:
        #     aw = novel_afterword.find(id=f"La{afterword_id}")
        #     if aw == None:
        #         keep_trying -= 1
        #     else:
        #         if validate_payload(aw.text):
        #             # Replace known japanese words
        #             ja_paragr = replace_words_jp(aw.text, ja_dict)
        #             afterword = ja_paragr
        #         else:
        #             afterword = aw.text
        #         myfile.write(make_paragraph(afterword))
        #     afterword_id += 1

    # Write html file closing tags
    myfile.write(file_bottom())

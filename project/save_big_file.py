import os
from bs4 import BeautifulSoup
from datetime import datetime as dt

out_folder = "output/"


# Get list of all files in the raws dir
raws_dir = "wn_jp_html/"
f = []
for (dirpath, dirnames, filenames) in os.walk(raws_dir):
    f.extend(filenames)
    break

# open a file and turn it into soup
with open(f"{raws_dir}{f[1]}", encoding="utf8") as fp:
    print(f[1])
    soup = BeautifulSoup(fp.read(), features="lxml")
    # soup = BeautifulSoup(fp, 'html.parser')
ch_title = soup.find("p", class_="novel_subtitle")
print(ch_title)


with open(
    f"output/BIGFILE-JP-{dt.now().strftime('%Y%m%d-%H%M%S')}.txt",
    "w",
    encoding="utf8",
) as myfile:
    # file_name = f[0]
    for file_name in f[:4]:
        # Load raw file
        with open(f"{raws_dir}{file_name}", encoding="utf8") as fp:
            soup = BeautifulSoup(fp.read(), features="lxml")

        # Get chapter data
        ch_title = soup.find("p", class_="novel_subtitle")
        novel_honbun = soup.find(id="novel_honbun")
        novel_afterword = soup.find(id="novel_a")

        # Write chapter title to file
        myfile.write(f"{file_name.split('-')[0]}: {ch_title.text}\n")

        # Write chapter content to file
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
        myfile.write("\n\n")

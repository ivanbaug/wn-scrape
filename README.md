# wn-scrape

Web Novel Scrape, is the result of the wish to keep reading a japanese webnovel that is not released in english yet, but it's available for free in japanese.

## How it works
### Save raws
In order to request the html from the site only once instead of spamming it multiple times i created a script to save the raws to then proccess them.

First save the raw html of the chapters of the WN using `save_raws.py`.

You'll have to edit a bit the code to set the following variables:
```python
    main_url = "site url"
    out_folder = "wn_jp_html/"
    ch_start = 1 #First chapter to save
    ch_end = 128 #Last chapter to save
```

When the script is run, it will save the WN in japanese to the folder `wn_jp_html/`. 

### Translate and save
Once we have the raws we can use the `main.py` script we will have to again edit a bit the script to personalize the name of the book and select chapters:
```python
if __name__ == "__main__":
    # Run translation - html crsation function
    # The resulting html is compatible with Calibre ebook indentation
    book_title = 'book name or set of chapters name'

    translate_multiple_ch(book_title, ch_start=42, ch_end=52)
```

**note:** I usually separate the books in batches of 10 chapters because the translation library has a delay of a couple of seconds per paragraph as to not spam the google servers.

**note2:** Translating 10 chapters takes around 20 to 40 minutes depending on the lenght.

**note3:** The resulting html is compatible with Calibre ebook indentation so we can use that software to convert it to an ebook format.

## Word dicts
Since japanese machine translators are not very accurate there maybe names or words that you may want to replace personally if you know the context, to do that in the project folder you'll have to create a `dicts` folder with the following files:

```
wnscrape
│
└──output
└──project
│   │
│   └──dicts
│      │jap_dict.json
│      │en_dict.json
└──wn_jp_html
```
In `jap_dict.json` and `en_dict.json` you can add custom words to replace during translation, being them in japanese or english, for example:

```json
{
  "version": "2.0.10",
  "replacements": [{
      "active": true,
      "case": "Override",
      "repA": "麗乃",
      "repB": "Urano",
      "type": "Simple"
    },
    {
      "active": true,
      "case": "Override",
      "repA": "本須",
      "repB": "Motosu",
      "type": "Simple"
    }
  ]
}
```

Enjoy your books!


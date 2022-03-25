import requests
import json
from ast import literal_eval
import time
from pymongo import MongoClient
import statistics

words_to_ignore = {
    "avyze",
    "awdls",
    "azygy",
    "boygs",
    "byked",
    "byrls",
    "daych",
    "dorbs",
    "dsobo",
    "dsomo",
    "durgy",
    "dzhos",
    "eevns",
    "egmas",
    "ennog",
    "erevs",
    "euked",
    "evhoe",
    "ewked",
    "gowfs",
    "humfs",
    "hwyls",
    "hiois",
    "jarps",
    "jokol",
    "kerky",
    "khafs",
    "koaps",
    "kophs",
    "kuzus",
    "mausy",
    "omovs",
    "odyls",
    "nabks",
    "peeoy",
    "peghs",
    "phpht",
    "poupt",
    "pebas",
    "ryked",
    "pyins",
    "qapik",
    "qophs",
    "sdayn",
    "snebs",
    "sohur",
    "skyfs",
    "skyrs",
    "sowfs",
    "syped",
    "takky",
    "tiyns",
    "ylkes",
    "ylems",
    "yesks",
    "yarko",
    "yaffs",
    "xysts",
    "wudus",
    "whyda",
    "wembs",
    "vutty",
    "voips",
    "voema",
    "viffs",
    "uraos",
    "yarco",
}


def populate_ngrams(ngrams_collection) -> None:
    start_year = 2000
    ny_list_file = "/home/utpal/wordle/nytimes_list.txt"
    with open(ny_list_file) as words_file:
        for line in words_file:
            line = line.strip().lower()
            if line in words_to_ignore:
                continue
            else:
                find_result = ngrams_collection.find_one({"word": line})
                if find_result:
                    continue
                else:
                    print(f"processing word:{line}")
                    url = f"https://books.google.com/ngrams/json?content={line}&year_start={start_year}&year_end=2022&corpus=26&smoothing=3"
                    r = requests.get(url)
                    if r.status_code == 200:
                        data = literal_eval(r.text)
                        if len(data) > 0:
                            ngrams_collection.insert_one(
                                {"word": line, "ngramsum": sum(data[0]["timeseries"])}
                            )
                        else:
                            print(url)
                            print("ngram did not return data.")
                    else:
                        print(r.status_code, r.text)
                        time.sleep(30)


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client.ngramsdb
    # populate_ngrams(db.ngrams)
    ngrams_list = []
    for item in db.ngrams.find():
        ngrams_list.append({"word": item["word"], "ngramsum": item["ngramsum"]})

    median = statistics.median((item["ngramsum"] for item in ngrams_list))
    print(median)
    words_less_than_median = [item for item in ngrams_list if item["ngramsum"] < median]
    words_less_than_median.sort(key=lambda t: t["ngramsum"], reverse=True)
    print(words_less_than_median)
    # outfile = open("ngram_words.json", "wt")
    # outfile.write(json.dumps(ngrams_list, indent=2))
    # outfile.close()

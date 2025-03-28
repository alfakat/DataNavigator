import re
import spacy
from spacy.matcher import Matcher
import pandas as pd

inventors = [
    "Ada-Lovelace-Computer-Programming-1843-No-UK",
    "Thomas-Edison-USA-1879-No-Light-Bulb",
    "Telephone-Alexander-Bell-1876-Scotland-Telephone-No",
    "Marie-Curie-Yes-Poland-Radioactivity-1898-Yes",
    "Guglielmo-Marconi-Radio-Italy-Yes-1895",
    "James-Watt-1769-No-Scotland-Steam-Engine",
    "Italy-Various-1490-No-Leonardo-da-Vinci",
    "Germany-Johannes-Gutenberg-Printing-Press-1440-No",
    "Tim-Berners-Lee-UK-World-Wide-Web-1989-No",
    "Computer-Science-Alan-Turing-UK-1936-No",
    "1976-No-Steve-Jobs-USA-Personal-Computer",
    "Lamarr-Hedy-No-Austria-Wireless-Communication-1942",
    "Sweden-Dynamite-Alfred-Nobel-1867-No",
    "No-Wright-Brothers-USA-Airplane-1903",
]

df = pd.DataFrame(inventors, columns=["Inventor"])


def preprocess_string(string: str):
    """I found out that splitting into small tokens is more efficients then one long input"""
    parts = string.replace('-', ' ').replace('_', ' ').split()
    return parts


def detect_objects_from_parts(parts: str):
    objects = {'NobelPrize': False}
    for part in parts:
        if part == 'Yes':
            objects['NobelPrize'] = 'Yes'
        elif part == 'No':
            objects['NobelPrize'] = 'No'

    return objects


def process_nobel_prize(nobel_prize: str):
    parts = preprocess_string(nobel_prize)
    return pd.Series(detect_objects_from_parts(parts))


df[['NobelPrize']] = df["Inventor"].apply(lambda x: process_nobel_prize(str(x)))


def extract_year(string: str):
    """Extracts a 4-digit year from the string"""
    parts = preprocess_string(string)
    for part in parts:
        if re.match(r"^\d{4}$", part):
            return int(part)
    return None


df["Year"] = df["Inventor"].apply(extract_year)

def clean_inventor_column(df, column_name):

    df["Inventor"] = df.apply(
        lambda row: "-".join(
            [part for part in preprocess_string(row["Inventor"]) if part not in [str(row[column_name])]]), axis=1)
    return df

trf = spacy.load('en_core_web_trf')

def extract_human_names(string: str):
    parts = preprocess_string(string)

    human_names = []
    for part in parts:
        doc = trf(part)
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                human_names.append(ent.text)

    return ', '.join(human_names)


df["inventor_names"] = df["Inventor"].apply(lambda x: extract_human_names(str(x)))

df[["Name", "Surname"]] = df["inventor_names"].apply(lambda x: pd.Series(x.split(", ")[:2] if x else ["", ""]))
df.drop(columns=["inventor_names"], inplace=True)


nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)
pattern_country = [{"POS": "PROPN"}]
matcher.add("COUNTRY", [pattern_country])

def extract_country(video_id):
    """Extracts the country name from the inventor's video_id"""
    parts = video_id.split("-")
    doc = nlp(" ".join(parts))

    matches = matcher(doc)
    for match_id, start, end in matches:
        return doc[start:end].text

    return ""


def extract_field(inventor_string):
    """Extracts the field of invention from the cleaned Inventor column."""
    parts = preprocess_string(inventor_string)
    return " ".join(parts[1:])


df["Country"] = df["Inventor"].apply(extract_country)
clean_inventor_column(df, "Country")

df["Field"] = df["Inventor"].apply(extract_field)
print(df)

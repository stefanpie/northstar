from collections import OrderedDict
import datetime
import io
import json
from pathlib import Path
import re
from joblib import Parallel, delayed
import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup
import gzip
import shutil
import tqdm


DATA_DIR = Path("./data")


def download_bouy(data_dir: Path):
    data_dir.mkdir(exist_ok=True)

    bouy_dir = data_dir / "bouy"
    bouy_dir.mkdir(exist_ok=True)

    bouy_dir_raw = bouy_dir / "raw"
    bouy_dir_raw.mkdir(exist_ok=True)

    r = requests.get("https://www.ndbc.noaa.gov/historical_data.shtml", timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")
    ul = soup.find("b", text="Standard Meterological").find_next_sibling("ul")
    links = ul.find_all("a")
    herfs = [link.get("href") for link in links]

    def download_single(href):
        data_page_link = "https://www.ndbc.noaa.gov" + href
        r = requests.get(data_page_link, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        data_url = "https://www.ndbc.noaa.gov" + soup.find("a", text=re.compile("\w+\.txt\.gz")).get("href")
        data_name = data_url.split("/")[-1]
        data_path = bouy_dir_raw / data_name
        r = requests.get(data_url, allow_redirects=True, timeout=10)
        with open(data_path, "wb") as f:
            f.write(r.content)
        with gzip.open(data_path, "rb") as f_in:
            with open(data_path.with_suffix(""), "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        data_path.unlink()

    # Parallel(n_jobs=-1)(delayed(download_single)(href) for href in tqdm.tqdm(herfs))
    # use multiprocessing 
    Parallel(n_jobs=12, backend="loky")(delayed(download_single)(href) for href in tqdm.tqdm(herfs))


if __name__ == "__main__":
    download_bouy(DATA_DIR)

from collections import OrderedDict
import datetime
import io
import json
from pathlib import Path
from joblib import Parallel, delayed
import numpy as np
import requests
import pandas as pd
from pyproj import Geod


DATA_DIR = Path("./data")


def download_hurdat(data_dir=DATA_DIR):
    hurdat_dir = data_dir / "hurdat"
    hurdat_dir.mkdir(exist_ok=True)
    url = "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2021-100522.txt"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}")
    with open(hurdat_dir / "hurdat2.txt", "w", encoding="utf8") as f:
        f.write(response.text)


def process_hurdat(data_dir=DATA_DIR):
    hurdat_dir = data_dir / "hurdat"
    hurdat_fp = hurdat_dir / "hurdat2.txt"

    # check if file exists
    if not hurdat_fp.exists():
        raise FileNotFoundError(f"File {hurdat_fp} does not exist")

    hurdat = []
    data_file_lines = []


    with open(hurdat_fp, encoding="utf-8") as f:
        data_file_lines = f.readlines()

 
    current_atcf_code = None
    current_storm_name = None
    current_storm_num_of_entries = None

    for line in data_file_lines[:]:
        line_data = line.rstrip("\n")
        line_data = line_data.split(",")[:-1]
        line_data = list(map(str.strip, line_data))
        if len(line_data) == 3:
            current_atcf_code = line_data[0]
            current_storm_name = line_data[1]
            current_storm_num_of_entries = line_data[2]
            # print(line_data)
        else:
            data = OrderedDict()
            data["atcf_code"] = current_atcf_code
            data["storm_name"] = current_storm_name
            data["year"] = int(line_data[0][:4])
            data["month"] = int(line_data[0][4:6])
            data["day"] = int(line_data[0][6:])
            data["hour"] = int(line_data[1][:2])
            data["minute"] = int(line_data[1][2:])
            data["record_id"] = line_data[2]
            data["system_status"] = line_data[3]
            lat = float(line_data[4][:-1])
            if line_data[4][-1] == "S":
                lat *= -1.0
            data["latitude"] = lat
            lon = float(line_data[5][:-1])
            if line_data[5][-1] == "W":
                lon *= -1.0
            data["longitude"] = lon
            data["max_sus_wind"] = float(line_data[6])
            data["min_pressure"] = float(line_data[7])

            data["wind_radii_34_NE"] = float(line_data[8])
            data["wind_radii_34_SE"] = float(line_data[9])
            data["wind_radii_34_SW"] = float(line_data[10])
            data["wind_radii_34_NW"] = float(line_data[11])

            data["wind_radii_50_NE"] = float(line_data[12])
            data["wind_radii_50_SE"] = float(line_data[13])
            data["wind_radii_50_SW"] = float(line_data[14])
            data["wind_radii_50_NW"] = float(line_data[15])

            data["wind_radii_64_NE"] = float(line_data[16])
            data["wind_radii_64_SE"] = float(line_data[17])
            data["wind_radii_64_SW"] = float(line_data[18])
            data["wind_radii_64_NW"] = float(line_data[19])

            hurdat.append(data)
    
    source_df = pd.DataFrame(hurdat)
    hurricane_df_list = []

    for atcf_code, hurrican_df in source_df.groupby("atcf_code"):
        hurricane_df_list.append(hurrican_df)

    def hurricane_missing_values_filter(x):
        flag = True
        if -999 in x["max_sus_wind"].values:
            flag = False
        if -999 in x["min_pressure"].values:
            flag = False
        return flag

    def odd_time_row_filter(x):
        x_filtered = x[((x["hour"] % 6) == 0) & (x["minute"] == 0)]
        return x_filtered

    def calculate_delta_distance_and_azimuth(x):
        x["latitude-6"] = x["latitude"].shift(1)
        x["longitude-6"] = x["longitude"].shift(1)
        x.dropna(inplace=True)

        wgs84_geod = Geod(ellps="WGS84")

        def delta_distance_azimuth(lat1, lon1, lat2, lon2):
            az12, az21, dist = wgs84_geod.inv(lon1, lat1, lon2, lat2)
            dist = [x / 1000.0 for x in dist]
            return dist, az12

        x["delta_distance"], x["azimuth"] = delta_distance_azimuth(
            x["latitude-6"].tolist(), x["longitude-6"].tolist(), x["latitude"].tolist(), x["longitude"].tolist()
        )

        del x["latitude-6"]
        del x["longitude-6"]
        return x

    def calculate_x_y(x):
        x["x"] = np.sin(x["latitude"]) * np.cos(x["longitude"])
        x["y"] = np.sin(x["latitude"]) * np.sin(x["longitude"])
        return x

    def calculate_new_dt_info(x):
        def extract_dt_info(y):
            y["day_of_year"] = datetime.datetime(y["year"], y["month"], y["day"]).timetuple().tm_yday
            y["minute_of_day"] = y["hour"] * 60 + y["minute"]
            return y

        x = x.apply(extract_dt_info, axis=1)
        return x

    def calculate_aday(x):
        x["aday"] = np.exp(np.square(x["day_of_year"] - 253) / 900)
        return x

    def calculate_vpre(x):
        x["vpre"] = x["max_sus_wind"] * x["min_pressure"]
        return x

    def calculate_landfall(x):
        x["landfall"] = x.apply(lambda x: 1 if x["record_id"] == "L" else 0, axis=1)
        return x

    def calculate_time_shifted_features(x):
        shifts = [1, 2, 3, 4, 5, 6, 7, 8, -1, -4]
        d_t = 6
        features = [
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "record_id",
            "system_status",
            "latitude",
            "longitude",
            "max_sus_wind",
            "min_pressure",
            "delta_distance",
            "azimuth",
            "day_of_year",
            "minute_of_day",
            "aday",
            "x",
            "y",
            "vpre",
            "landfall",
        ]
        for s in shifts:
            shift_label = ""
            if s > 0:
                shift_label = str(-1 * d_t * s)
            else:
                shift_label = "+" + str(-1 * d_t * s)

            f_p = [f + shift_label for f in features]
            x[f_p] = x[features].shift(s)

        x.dropna(inplace=True)
        return x

    print("#### Cleaning and Feature Extraction ####")

    print("Filtering missing values...")
    hurricane_df_list = list(filter(hurricane_missing_values_filter, hurricane_df_list))

    print("Filtering each hurricane for off interval times...")
    hurricane_df_list = list(map(odd_time_row_filter, hurricane_df_list))

    # input("test")

    print("Calculating azimuth and delta distance features...")
    # hurricane_df_list = list(map(calculate_delta_distance_and_azimuth, hurricane_df_list))
    hurricane_df_list = Parallel(n_jobs=-1, verbose=0)(
        delayed(calculate_delta_distance_and_azimuth)(h_df) for h_df in hurricane_df_list
    )

    print("Calculating x and y features...")
    # hurricane_df_list = list(map(calculate_x_y, hurricane_df_list))
    hurricane_df_list = Parallel(n_jobs=-1, verbose=0)(delayed(calculate_x_y)(h_df) for h_df in hurricane_df_list)

    print("Calculating new datetime features...")
    # hurricane_df_list = list(map(calculate_new_dt_info, hurricane_df_list))
    hurricane_df_list = Parallel(n_jobs=-1, verbose=0)(
        delayed(calculate_new_dt_info)(h_df) for h_df in hurricane_df_list
    )

    print("Calculating aday feature...")
    # hurricane_df_list = list(map(calculate_aday, hurricane_df_list))
    hurricane_df_list = Parallel(n_jobs=-1, verbose=0)(delayed(calculate_aday)(h_df) for h_df in hurricane_df_list)

    print("Calculating vpre feature...")
    # hurricane_df_list = list(map(calculate_vpre, hurricane_df_list))
    hurricane_df_list = Parallel(n_jobs=-1, verbose=0)(delayed(calculate_vpre)(h_df) for h_df in hurricane_df_list)

    print("Calculating landfall feature...")
    # hurricane_df_list = list(map(calculate_landfall, hurricane_df_list))
    hurricane_df_list = Parallel(n_jobs=-1, verbose=0)(delayed(calculate_landfall)(h_df) for h_df in hurricane_df_list)

    # print("Calculating time shifted feature...")
    # hurricane_df_list = list(map(calculate_time_shifted_features, hurricane_df_list))
    # hurricane_df_list = Parallel(n_jobs=-1,verbose=0)(delayed(calculate_time_shifted_features)(h_df) for h_df in hurricane_df_list)

    print("Done")

    hurricane_df_list = [h_df for h_df in hurricane_df_list if not h_df.empty]

    final_df = pd.concat(hurricane_df_list)
    final_df = final_df.sort_values(by=["year", "atcf_code", "month", "day", "hour"])
    final_df = final_df[final_df["year"] >= 1980]


    print("#### Saving processed data to file ####")
    hurdat_processed_csv_fp = hurdat_dir / "hurdat2_processed.csv"
    final_df.to_csv(hurdat_processed_csv_fp, index=False)
    print("Done")

    data_for_web = {}
    for group_id, group in final_df.groupby("atcf_code"):
        data_for_web[group_id] = group.to_dict("records")

    # replace nan with None
    for group_id, group in data_for_web.items():
        for datum in group:
            for key, value in datum.items():
                if isinstance(value, float) and np.isnan(value):
                    datum[key] = None

    hurdat_processed_json_fp = hurdat_dir / "hurdat2_processed.json"
    with open(hurdat_processed_json_fp, "w", encoding="utf8") as f:
        json.dump(data_for_web, f, indent=4)


if __name__ == "__main__":
    download_hurdat()
    process_hurdat()

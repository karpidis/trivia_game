import os
import requests

# Create a directory for the flags
output_folder = "UN_Flags"
os.makedirs(output_folder, exist_ok=True)

# List of country codes in ISO format
country_codes = [
    "af", "al", "dz", "ad", "ao", "ag", "ar", "am", "au", "at", "az", "bs", "bh", "bd", "bb", "by", "be", "bz", "bj", "bt", "bo", "ba", "bw", "br", "bn", "bg", "bf", "bi", "cv", "kh", "cm", "ca", "cf", "td", "cl", "cn", "co", "km", "cg", "cd", "cr", "ci", "hr", "cu", "cy", "cz", "dk", "dj", "dm", "do", "ec", "eg", "sv", "gq", "er", "ee", "sz", "et", "fj", "fi", "fr", "ga", "gm", "ge", "de", "gh", "gr", "gd", "gt", "gn", "gw", "gy", "ht", "hn", "hu", "is", "in", "id", "ir", "iq", "ie", "il", "it", "jm", "jp", "jo", "kz", "ke", "ki", "kp", "kr", "kw", "kg", "la", "lv", "lb", "ls", "lr", "ly", "li", "lt", "lu", "mg", "mw", "my", "mv", "ml", "mt", "mh", "mr", "mu", "mx", "fm", "md", "mc", "mn", "me", "ma", "mz", "mm", "na", "nr", "np", "nl", "nz", "ni", "ne", "ng", "mk", "no", "om", "pk", "pw", "pa", "pg", "py", "pe", "ph", "pl", "pt", "qa", "ro", "ru", "rw", "kn", "lc", "vc", "ws", "sm", "st", "sa", "sn", "rs", "sc", "sl", "sg", "sk", "si", "sb", "so", "za", "ss", "es", "lk", "sd", "sr", "se", "ch", "sy", "tj", "tz", "th", "tl", "tg", "to", "tt", "tn", "tr", "tm", "tv", "ug", "ua", "ae", "gb", "us", "uy", "uz", "vu", "va", "ve", "vn", "ye", "zm", "zw"
]

# Base URL for downloading flags from FlagCDN
base_url = "https://flagcdn.com/256x192/{}.png"

# Download all flags
for code in country_codes:
    flag_url = base_url.format(code)
    flag_path = os.path.join(output_folder, f"{code}.png")

    try:
        response = requests.get(flag_url, stream=True)
        if response.status_code == 200:
            with open(flag_path, "wb") as file:
                file.write(response.content)
            print(f"✅ Downloaded: {code}.png")
        else:
            print(f"❌ Failed: {code}.png (Status: {response.status_code})")
    except Exception as e:
        print(f"⚠️ Error downloading {code}.png: {e}")

print("🎉 All flags downloaded successfully!")


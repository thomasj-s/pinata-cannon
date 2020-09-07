"""Main module."""
import sweetviz as sv
import requests
import pandas as pd
from sklearn.model_selection import train_test_split


# class
class SetKeys:
    # Required api keys
    # constructor
    def __init__(self, pinata_api_key, pinata_secret_api_key):
        self.pinata_api_key = pinata_api_key
        self.pinata_secret_api_key = pinata_secret_api_key


class GetRequests(SetKeys):
    # inherits keys
    def __init__(self, pinata_api_key, pinata_secret_api_key):
        super().__init__(pinata_api_key=pinata_api_key,
                         pinata_secret_api_key=pinata_secret_api_key)

    # method
    def get_all(self):
        url = 'https://api.pinata.cloud/data/userPinnedDataTotal'

        headers = {'pinata_api_key': self.pinata_api_key,
                   'pinata_secret_api_key': self.pinata_secret_api_key}

        r = requests.get(url, headers=headers)

        print(r.status_code)

        return r.text

    def get_list(self):
        url = 'https://api.pinata.cloud/data/pinList'

        headers = {'pinata_api_key': self.pinata_api_key,
                   'pinata_secret_api_key': self.pinata_secret_api_key}

        r = requests.get(url, headers=headers)

        print(r.status_code)

        return r.text


class PostRequests(SetKeys):
    def __init__(self, pinata_api_key, pinata_secret_api_key, file):
        super().__init__(pinata_api_key=pinata_api_key,
                         pinata_secret_api_key=pinata_secret_api_key)
        self.file = file

    def pin_file(self):

        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

        # payload = {'pinataMetadata': '{"name":"MyExampleDocument",
        # "keyvalues":{"company": "Pinatas"}}'}
        files = [
            ('file', open('test.txt', 'rb'))
        ]
        headers = {
            'pinata_api_key': self.pinata_api_key,
            'pinata_secret_api_key': self.pinata_secret_api_key
        }

        response = requests.request("POST", url, headers=headers, files=files)

        print(response.text.encode('utf8'))


def sweet_make_report(csv):
    df = pd.read_csv(csv)
    my_report = sv.analyze(df)
    my_report.show_html()
    print("report made")


def test_train_split(csv):
    df = pd.read_csv(csv)
    # feature_config = sv.FeatureConfig(skip="PassengerId", force_text=["Age"])
    train, test = train_test_split(df, test_size=0.20, random_state=42)
    my_report = sv.compare([test, "Training Data"], [train, "Test Data"])
    my_report.show_html("splitreport.html")


def sweet_test_train_report(csv):
    df = pd.read_csv(csv)
    my_report = sv.analyze(df)
    my_report.show_html()
    print("report made")
    pass


class Sweetviz2Pinata(SetKeys):
    def __init__(self, pinata_api_key, pinata_secret_api_key, file):
        super().__init__(pinata_api_key=pinata_api_key,
                         pinata_secret_api_key=pinata_secret_api_key)
        self.file = file

    def pin_report(self):
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

        # payload = {'pinataMetadata':
        # '{"name":"MyExampleDocument","keyvalues":{"company": "Pinatas"}}'}
        files = [
            ('file', open('splitreport.html', 'rb'))
        ]
        headers = {
            'pinata_api_key': self.pinata_api_key,
            'pinata_secret_api_key': self.pinata_secret_api_key
        }

        response = requests.request("POST", url, headers=headers, files=files)

        print(response.text.encode('utf8'))


if __name__ == "__main__":
    print("Hello Pinata")

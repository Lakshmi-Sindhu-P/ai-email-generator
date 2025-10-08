import kagglehub

def download_email_dataset():
    path = kagglehub.dataset_download("bofulee/kevin-hillstrom-minetdata-emailanalytics")
    print("Dataset downloaded at:", path)

if __name__ == "__main__":
    download_email_dataset()

import requests
import time
import json

def analyze_url(url_to_analyze, api_key):
    """
    Analyzes the given URL using the VirusTotal API and writes the analysis report to a file.

    Parameters:
    url_to_analyze (str): The URL to be analyzed.
    api_key (str): Your VirusTotal API key.

    Returns:
    None
    """
    url = "https://www.virustotal.com/api/v3/urls"
    payload = {"url": url_to_analyze}
    headers = {
        "accept": "application/json",
        "x-apikey": api_key,
        "content-type": "application/x-www-form-urlencoded"
    }

    # Send POST request
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        # 解析 JSON data
        response_data = response.json()
        analysis_id = response_data["data"]["id"]
        print(f"URL submitted successfully. Analysis ID: {analysis_id}")

        time.sleep(3)

        # 分析报告的 URL
        report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        report_response = requests.get(report_url, headers=headers)

        if report_response.status_code == 200:
            report = report_response.json()

            # 寫入 TXT 
            with open("analysis_URL.txt", "w") as file:
                file.write(json.dumps(report, indent=4))
            print("Report has been written to analysis_URL.txt")
        else:
            print(f"Failed to retrieve report: {report_response.status_code}")
            with open("error_log.txt", "w") as file:
                file.write(f"Failed to retrieve report: {report_response.status_code}\n")
                file.write(report_response.text)
    else:
        print(f"Failed to submit URL: {response.status_code}")
        with open("error_log.txt", "w") as file:
            file.write(f"Failed to submit URL: {response.status_code}\n")
            file.write(response.text)

def upload_file_to_virustotal(api_key, file_path):
    """
    Uploads a file to VirusTotal for analysis and writes the analysis report to a file.

    Parameters:
    api_key (str): Your VirusTotal API key.
    file_path (str): The path to the file to be uploaded.

    Returns:
    None
    """
    upload_url = "https://www.virustotal.com/api/v3/files"

    try:
        # Read file
        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {
                "accept": "application/json",
                "x-apikey": api_key
            }

            # Upload file
            response = requests.post(upload_url, files=files, headers=headers)
            response.raise_for_status()  # Check if the request was successful

            # Parse JSON data
            response_data = response.json()
            analysis_id = response_data["data"]["id"]
            print(f"File uploaded successfully. Analysis ID: {analysis_id}")

            # Give some time for the analysis to be done
            time.sleep(3)

            # Get analysis report URL
            report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
            report_response = requests.get(report_url, headers=headers)
            report_response.raise_for_status()  # Check if the request was successful

            report = report_response.json()

            # Write report to a TXT file
            with open("analysis_report.txt", "w") as file:
                file.write(json.dumps(report, indent=4))
            print("Report has been written to analysis_report.txt")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        with open("error_log.txt", "w") as file:
            file.write(f"An error occurred: {e}\n")
            if response is not None:
                file.write(response.text)
            if report_response is not None:
                file.write(report_response.text)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        with open("error_log.txt", "w") as file:
            file.write(f"An unexpected error occurred: {e}\n")



### Usage
API_KEY = "API-KEY"
FILE_PATH = "test_file.pdf"
upload_file_to_virustotal(API_KEY, FILE_PATH)

URL_TO_ANALYZE = "https://ais3.org/Home/Course"
analyze_url(URL_TO_ANALYZE, API_KEY)
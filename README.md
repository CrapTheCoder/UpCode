# UpCode
A software for uploading all your accepted solutions from CodeChef, CodeForces, and Atcoder to Github with no hassles, and fully automated using Python.

## How to use:
* Generate an API key (Github access token) from https://github.com/settings/tokens. Make sure the repo section is checked.
* Download the project and extract the zip file. Navigate to the extracted folder and run the following command in terminal:

  ```
  pip install -r requirements.txt
  ```
  or you can try:
  ```
  py -m pip install -r requirements.txt
  ```
  
* To start using the project, run the following command in terminal:

  ```
  python main.py
  ```
* After this Put your Codeforces, CodeChef, and Atcoder username along with the GitHub access token (which you already generated at the start of the process)
  after this give the repository name and you are good to go!, Yaayyy : )


### Modules used:
* `requests` and `grequests` to get the html
* BeautifulSoup4 (`bs4`) to parse the html
* `selenium` to make CodeForces scraper more reliable
* `webdriver_manager` to automatically create the chromium executable
* `PyGithub` to access the GitHub API
* `json` to parse CodeForces API
* `multiprocessing` to parallelize CodeForces and CodeChef uploads
* Misc: `time`, `logging`, `dotenv`, `inspect`

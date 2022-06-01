# UpCode
A software for uploading all your accepted solutions from CodeChef and CodeForces to Github with no hassles, and fully automated using Python.

## How to use:
* Generate an API key from https://github.com/settings/tokens. Make sure the repo section is checked.
* Download the project and extract the file. Then open terminal and run the following command:

  ```
  pip install -r C:\path\to\requirements.txt
  ```
* In terminal, run the following command to start using the project:

  ```
  python3 C:\path\to\main.py
  ```

### Modules used:
* `requests` and `grequests` to get the html
* BeautifulSoup4 (`bs4`) to parse the html
* `PyGithub` to access the GitHub API
* `json` to parse CodeForces API
* Misc: `time`, `logging`, `dotenv`

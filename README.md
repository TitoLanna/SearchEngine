# Search Engine
## Description

This project is a search engine that can be used to search for words from text files and json objects. The search engine will return the top 10 most relevant documents based on the search query. The search engine uses the tf-idf algorithm to determine the relevance of a document to a search query.

## How to run the project

### creating and activating the virtual environment
1. `python -m venv venv`
2. `source venv/bin/activate`

### install the required packages
3. `pip --quiet install -r requirements.txt`

### project related commands
4. if you want to confirm that the script works, run `python prepare_data.py` or else the data is already prepared
5. In `main.ipynb` run all the cells to see the results of the search engine

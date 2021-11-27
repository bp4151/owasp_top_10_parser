# OWASP Web Top 10 Parser

## What
This python script will parse the OWASP Web Top 10 pages and pull out the top level, reference, and CWE links into a JSON format file. 

## Why
This was developed out of a need for OWASP Top 10 links in a json format to be included in automation. 

## How

To run (assumes PipEnv is installed):
1. Clone to your desired location
2. Create your .env file, setting the FILE and DEBUG values
```
    URL=https://owasp.org/Top10/
    FILE=web_2021.json
    DEBUG=True
```
3. From the command line, run 
```
pipenv shell
pipenv install
pipenv run python main.py
pipenv --rm
```
4. Your file containing the output should be in the root folder. 

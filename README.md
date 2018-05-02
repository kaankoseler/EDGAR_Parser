# Quovo Coding Challenge

### Challenge
- Write code in Python that parses fund holdings pulled from EDGAR, given a ticker or CIK. 

### Requirements
- Requires Python 3
- To install dependencies, cd into the directory and use:
```sh
$ pip install -r requirements.txt
```

### Example Usage
- Let's try and grab the latest 13F for *Goldman Sachs*
- cd into the directory, then do:
```sh
$ python parser.py GS
```
- The parser accepts both CIK and Ticker, so you can also do the following (for *The Bill and Melinda Gates Foundation*):
```sh
$ python parser.py 0001166559
```
- The output is a tab-delimited .txt file with headers. Conveniently labeled based on user input! 

### Goals
##### Let us know your thoughts on how to deal with different formats.  
This parser is quite robust to different formats. For example, *Goldman Sachs* has extra columns like "Put/Call" or "otherManager" that *The Bill and Melinda Gates Foundation* does not have. Even within *Goldman Sachs*'s 13F, not all entries have the same number of fields. The parser handles both cases. First, it builds a list of the maximum amount of headers used within the file. Then, it looks through each entry and adds an "N/A" if that entry does not, for example, have a "Put/Call" column. 

### Caveats
- It can take a while to parse when we're dealing with a larger 13F file. For example, parsing the latest Goldman Sachs 13F takes a few seconds. 



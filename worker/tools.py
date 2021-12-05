import requests, json, urllib 

def get_patent_numbers_from_list(patent_list):
    numlist = []
    if patent_list != None:
        for patent in patent_list:
            numlist.append( patent['patent_number'] )
    return numlist

def get_patent_title_from_number(patent_num):
    #print("TODO")
    url = "https://api.patentsview.org/patents/query?q={%22_eq%22:{%22patent_number%22:%22" + patent_num + "%22}}&f=[%22patent_title%22]"
    result = requests.get(url)
    json_dict = json.loads(result.text)
    patents = json_dict["patents"]
    if patents == None:
        return
    title = patents[0]["patent_title"]
    print(f"Title: {title}")
    return title

def get_continuation_by_title(title_to_search):
    if title_to_search == None or title_to_search == "":
        return
    # for getting cited patents given patent_id
    #url = "https://api.patentsview.org/patents/query?q={%22_eq%22:{%22patent_number%22:%22" + patent_number_input + "%22}}&f=[%22patent_number%22,%22cited_patent_number%22]"
    title_to_search_url_encoded = urllib.parse.quote(title_to_search)
    url = "https://api.patentsview.org/patents/query?q={%22_eq%22:{%22patent_title%22:%22" + title_to_search_url_encoded + "%22}}&f=[%22assignee_organization%22,%20%22patent_number%22,%20%22patent_title%22,%20%22patent_date%22,%22app_number%22,%22assignee_first_name%22,%22assignee_last_name%22,%22examiner_id%22,%22examiner_first_name%22,%22examiner_last_name%22,%22inventor_first_name%22,%22inventor_last_name%22]"
    print(f"URL: {url}")
    result = requests.get(url)
    json_dict = json.loads(result.text)
    patents = json_dict["patents"]
    return patents

def get_continuation_from_number( patent_id ):
    title = get_patent_title_from_number( patent_id )
    result = get_continuation_by_title( title )
    return result



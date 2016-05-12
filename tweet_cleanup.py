import re

def remove_usernames(string):
    #regex = r"@[A-Za-z0-9]+"
    regex = r"@\S+[\s\Z]"
    string = re.sub(regex, "", string)
    return string

def remove_hashtags(string):
    return re.sub(r"#\S+[\s\Z]", "", string)

def remove_url(string):
    regex = (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]'
             '|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return re.sub(regex, "", string)

try:
    # Wide UCS-4 build
    emoji = re.compile(u'['
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\U0001F910-\U0001F9C0'
        u'\u2600-\u26FF\u2700-\u27BF]',
        re.UNICODE)
except re.error:
    # Narrow UCS-2 build
    emoji = re.compile(u'('
        u'\ud83c[\udf00-\udfff]|'
        u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
        u'[\u2600-\u26FF\u2700-\u27BF])',
        re.UNICODE)

def get_emojis(string):
    return emoji.findall(string)

def cleanup(string):

    string = remove_usernames(string)
    string = remove_hashtags(string)
    string = remove_url(string)
    emojis = get_emojis(string)
    string = re.findall(r"[A-Za-z']+", string)
    return string, emojis

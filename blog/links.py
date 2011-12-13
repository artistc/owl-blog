''' Link Expander
  wraps key words in a document with <a></a> tags.
'''

def loadLinksFromDatabase():
    from models import Link
    #return dict( (link.keyword.upper(), link.url) for link in Link.objects.all() )
    # older version of python doesn't support the () generator syntax
    return dict( [(link.keyword.upper(), link.url) for link in Link.objects.all()] )

def makeLinkExpander(linkDictionary):
    ''' The keys of linkDictionary should be all uppercase.
    Returns a function that wraps each key with an HTML link to its value.
    The replacement is case-insensitive.  '''

    import re
    # regex will match any key in the dictionary
    regex = re.compile(
	    r'\s(?:(%s)([\)\-\'".,;:\s]))' % '|'.join(linkDictionary.keys()),
	    re.IGNORECASE | re.MULTILINE
	)

    def replaceMatch(match):
        word = match.group(1)
        punct = match.group(2)
        return ' <a href="%s">%s</a>%s' % (linkDictionary[word.upper()], word, punct)
    
    def linkExpander(string):
        return regex.sub(replaceMatch, string)
    return linkExpander

def getLinkExpander():
    try:
        return makeLinkExpander(loadLinksFromDatabase())
    except:
        return lambda x:x
    

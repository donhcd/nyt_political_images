from json import JSONDecoder, JSONEncoder
import sys

decoder = JSONDecoder()
encoder = JSONEncoder()

with open('nytimgurls.log','a') as f, open('nytfinal.json','a') as u:
    for line in sys.stdin.readline():
        jsonobj = decoder.decode(line)
        jsonobj['imgUrl'] = 'http://static.nytimes.com/' + jsonobj['imgUrl']
        f.write(jsonobj['imgUrl'])

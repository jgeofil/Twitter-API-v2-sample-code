import json

with open('tweets.json') as f:
    data = json.load(f)
general = ['author_id', 'conversation_id', 'created_at', 'id', 'lang', 'reply_settings', 'source', 'text']
tweets = []
metrics = []
refs = []
domain = []
subdomain = []
entities = {}
for tweet in data['data']:
	cleaned = {key: tweet[key] for key in tweet.keys() if key in general}
	met = tweet['public_metrics']
	met['id'] = tweet['id']
	if 'referenced_tweets' in tweet:
		for ref in tweet['referenced_tweets']:
			ref['from'] = tweet['id']
			refs.append(ref)
	metrics.append(met)
	tweets.append(cleaned)

	if 'entities' in tweet:
		for key in tweet['entities'].keys():
			if key not in entities:
				entities[key] = []
			for e in tweet['entities'][key]:
				e['id'] = tweet['id']
				entities[key].append(e)
	if 'context_annotations' in tweet:
		for ann in tweet['context_annotations']:
			dom = ann['domain']
			domain.append(dom)
			en = ann['entity']
			en['id'] = tweet['id']
			en['domain'] = dom['id']
			subdomain.append(en)
			

def linejson(js):
    
	js = [json.dumps(record) for record in js] 
	return '\n'.join(js)


with open('tweets_clean.json', 'w') as f:
    f.write(linejson(tweets))

with open('metrics.json', 'w') as f:
    f.write(linejson(metrics))

with open('refs.json', 'w') as f:
	f.write(linejson(refs))

for key in entities.keys():
    with open(f'{key}.json', 'w') as f:
        f.write(linejson(entities[key]))

with open('domain.json', 'w') as f:
	f.write(linejson(domain))

with open('subdomain.json', 'w') as f:
	f.write(linejson(subdomain))
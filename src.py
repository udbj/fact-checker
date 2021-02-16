import sys
import spacy
import lucene
from lupyne import engine
from transformers import pipeline
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from transformers import AutoTokenizer, AutoModelForSequenceClassification

lucene.initVM()
INDEXDIR = 'index'

src = sys.argv[1]

nlp = spacy.load("en_core_web_sm")

chklabs = set()
chklabs.add('CONTRADICTION')
chklabs.add('ENTAILMENT')

evidc_ls = []

tokenizer = AutoTokenizer.from_pretrained("roberta-large-mnli", do_lower_case = False)
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")
entailment = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# Extract named entities from query
doc = nlp(src)
names = ' '.join([ent.text for ent in doc.ents])

analyzer = EnglishAnalyzer()
indexer = engine.Indexer(INDEXDIR, analyzer = analyzer)

qry = QueryParser('titleTxt', analyzer).parse(names)

# Search for named entities in title texts
hits = indexer.search(qry, field = 'titleTxt', count = 3)

mx = hits.maxscore
hls = hits.highlights(qry, text = 1)


for hit in hits:
	if hit.score/mx > 0.5:
		for line in hit['text'].rstrip().split('\n'):

			l_num, l_txt = line.split(' ', 1)
			resl = entailment(l_txt + src)[0]
			
			# Add to results if the line contradicts or supports the query
			# with high confidence
			if resl['label'] in chklabs and resl['score'] > 0.95:
				pkg = (hit['title'], hit['file'], resl['label'], resl['score'], line)
				evidc_ls.append(pkg)



if len(evidc_ls) == 0:
	# If no evidence was found, search for whole sentence in article bodies
	qry = QueryParser('text', analyzer).parse(src)

	hits = indexer.search(qry, field = 'text', count = 3)

	mx = hits.maxscore
	hls = hits.highlights(qry, text = 1)


	for hit in hits:
		if hit.score/mx > 0.5:
			for line in hit['text'].rstrip().split('\n'):
				
				l_num, l_txt = line.split(' ', 1)
				resl = entailment(l_txt + src)[0]
				
				if resl['label'] in chklabs and resl['score'] > 0.95:
					pkg = (hit['title'], hit['file'], resl['label'], resl['score'], line)
					evidc_ls.append(pkg)

if len(evidc_ls) == 0:
	print('Not enough evidence.')
else:
	# Print results
	for idx, evidc in enumerate(evidc_ls):
		print('---------------------------------------------------')
		print('Article: ',evidc[0], ' ; File: ', evidc[1], ' ; Verdict: ', evidc[2], ' ', evidc[3])
		print()
		print(evidc[4])
		print('---------------------------------------------------')

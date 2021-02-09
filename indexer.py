import lucene
from lupyne import engine
import os
from org.apache.lucene.analysis.cjk import CJKAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer

INDEXDIR = 'index'
FILESDIR = 'wiki'

lucene.initVM()

analyzer = CJKAnalyzer()
analyzer = EnglishAnalyzer()

indexer = engine.Indexer(INDEXDIR, analyzer = analyzer)

indexer.set('file', engine.Field.Text, stored = True)
indexer.set('text', engine.Field.Text, stored = True)
indexer.set('title', engine.Field.Text, stored = True)
indexer.set('titleTxt', engine.Field.Text, stored = True)

for filename in os.listdir(FILESDIR):
	
	print('processing',filename)
	filepath = os.path.join(FILESDIR, filename)
	lines = open(filepath, 'r').readlines()
	
	prev = set()
	prev.add('DUMMY')
	content = ''
	for line in lines:
		title,text = line.split(' ', 1)
		if title not in prev:
			prev_title = list(prev)[0]
			tixt = prev_title.replace('_', ' ')
			indexer.add(text = content, file = filename, title = prev_title, titleTxt = tixt)
			prev = set()
			prev.add(title)
			content = text
		else:
			content = content + text

	indexer.add(text = content, file = filename, title = title)
	
	indexer.commit()

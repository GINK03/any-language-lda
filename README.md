# LDA example

## LDAについて

--- 数式 -- 

## gensimのLDAで使うコーパスのフォーマットについて  

DoW(Document Of Word)で表現する必要があり  
まず、あるドキュメントに関して、このようにする必要がある  

```console

```

かつ、単語にユニークな数値のIDを割り当てる必要があり、ListのListの形式でDocumentを生成する　　
```console

```

## gensimによる学習

```python
model = LdaMulticore(gensim_corpus, workers={8}, num_topics={TOPICN})
```

TOPICNはトピック数、workersはCPUの数

## トピックの分布を表示する

LDAはストップワードは頻出する単語を、コーパスから取り除くことで、うまく表現することである 

今回は、Wikipediaから構築したtf-idf辞書から、重要度が高い単語のみの残す  

```python
  model = pickle.loads( open('tmp/pickles/model.pkl', 'rb').read() )
  for topic in range(TOPICN):
    topn =  model.print_topic(topic, topn=100) 
    pairs = {}
    for pair in topn.split(' + '):
      weight, term = pair.split('*')
      term = term.replace('"', '')
      pairs[ index_term[int(term)] ] = float( weight )
    print( topic, sorted(pairs.items(), key=lambda x:x[1]*-1) )
```

## 推して参る（予想)

```python
def infer():
  model = pickle.loads( open('tmp/pickles/model.pkl', 'rb').read() )
  words = pickle.loads( open('tmp/words.pkl', 'rb').read() )
  term_index = pickle.loads( open('tmp/pickles/term_index.pkl', 'rb').read() )
  documents = []
  for name in glob.glob('tmp/wakati/*'):
    terms = dict( Counter( [term_index[term] for term in open(name).read().split() if term in words] ) )
    document = [ (t, f) for t,f in terms.items() ]
    documents.append( document )
  for document in documents:
    print( model[document] )
```

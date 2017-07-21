# LDA example

## LDAについて

--- 数式 -- 

## gensimのLDAで使うコーパスのフォーマットについて  

DoW(Document Of Word)で表現する必要があり  
まず、あるドキュメントに関して、このようにする必要がある  

```console
[('アドバンテッジパートナーズ', 1), ('ホームプロダクツ', 1), ('居住まい', 1), ('ユニゾン・キャピタル', 1), ('のたうち回っ', 1), ('たとえれ', 1), ('元の木阿弥', 1)]
[('おぉ', 1), ('ぁぁぁ', 1), ('ボロッと', 1), ('摘み食い', 1), ('ドンピシャ', 1), ('こう着', 1), ('曲る', 1), ('ねじ込ん', 1), ('カッポン', 1), ('神々し', 1), ('かせげ', 1)]
[('辰典', 1), ('すごかっ', 1), ('石田秀範', 1), ('武田玲奈', 1), ('ヤダ', 1), ('真鈴', 1), ('BuzzFeed', 1), ('寝れ', 1), ('マリエッティ', 1), ('今年5月', 1), ('引き締まる', 1), ('楽しいっ', 1)]
[('帝都自動車交通', 1), ('コネクテッド', 2)]
```

かつ、単語にユニークな数値のIDを割り当てる必要があり、ListのListの形式でDocumentを生成する　　
```console
[(36399, 1), (2532, 1), (25, 1), (36400, 1)]
[(1581, 1), (1583, 1), (1587, 1), (1582, 1), (1586, 1), (1585, 1), (1584, 1)]
[(5750, 1), (5754, 1), (5753, 1), (5746, 1), (5747, 1), (5752, 1), (5751, 1), (3748, 1), (5749, 1), (5755, 1), (5748, 1)]
[(1030, 1), (1263, 1), (3366, 1), (3362, 1), (3364, 1), (3363, 1), (15, 1), (3368, 1), (3365, 1), (999, 1), (712, 1), (3367, 1)]
[(15248, 1), (5861, 2)]
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

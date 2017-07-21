import os 
import sys

import math
import gensim

import gzip
import glob
import pickle
from collections import Counter

import MeCab
import concurrent.futures

from gensim.models import LdaMulticore


TOPICN = 10

def _wakati(name):
  m = MeCab.Tagger('-Owakati')
  savename = 'tmp/wakati/{}.txt'.format( name.split('/').pop() )
  text = gzip.open(name, 'rt').read()
  wakati = m.parse(text).strip()
  open(savename, 'w').write( wakati )
  print('end', name)
  
def wakati():
  names = [ name for name in glob.glob('tmp/each/*.gz') ]
 
  with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
    executor.map( _wakati, names )

def multicore():
  # tfidfで重みが大きいもののセット
  words = pickle.loads( open('tmp/words.pkl', 'rb').read() )

  documents = []
  for name in glob.glob('tmp/wakati/*'):
    terms = open(name).read().split()
    terms = [ term for term in terms if term in words ] 
    documents.append( terms )

  term_index = {}
  for terms in documents:
    for term in terms:
      # wordsに入っていない単語は見ない
      if term not in words:
         continue
      if term_index.get( term ) is None:
         term_index[term] = len( term_index )

  open('tmp/pickles/term_index.pkl', 'wb').write( pickle.dumps( term_index ) )
  gensim_corpus = []

  for document in documents:
    tf = dict( Counter( document ) )
    doc = [ (term_index[t], f) for t, f in tf.items() ]
    gensim_corpus.append( doc )
  print('start to fit lda distribute...')
  model = LdaMulticore(gensim_corpus, workers=8, num_topics=TOPICN)
  open('tmp/pickles/model.pkl', 'wb').write( pickle.dumps( model ) )

  print('finish to learn')

def topics():
  term_index = pickle.loads( open('tmp/pickles/term_index.pkl', 'rb').read() )
  index_term = { index:term for term, index in term_index.items() }
  print( index_term[1] )
  model = pickle.loads( open('tmp/pickles/model.pkl', 'rb').read() )
  for topic in range(TOPICN):
    topn =  model.print_topic(topic, topn=100) 

    pairs = {}
    for pair in topn.split(' + '):
      weight, term = pair.split('*')
      term = term.replace('"', '')
      pairs[ index_term[int(term)] ] = float( weight )
    print( topic, sorted(pairs.items(), key=lambda x:x[1]*-1) )

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
    #print( document )
    print( model[document] )

if __name__ == '__main__':
  if '--step1' in sys.argv:
     wakati()

  if '--step2' in sys.argv:
    multicore()

  if '--step3' in sys.argv:
    topics()

  if '--step4' in sys.argv:
    infer()

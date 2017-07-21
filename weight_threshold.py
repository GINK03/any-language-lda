import os
import glob


import json
import pickle

# 全体のTFIDFの重み、トップ50％を利用
words_idf = json.loads( open('tmp/words_idf.json?dl=0').read() )

words = set()
for word, idf in sorted( words_idf.items(), key=lambda x:x[1]*-1)[:len(words_idf)//100*50]: 
  words.add( word ) 

open('tmp/words.pkl', 'wb').write( pickle.dumps( words ) )


import graphlab as gl
gl.canvas.set_target('ipynb')
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient

gl_cat_tfidf = gl.SFrame('../data/items_categories_tifidf_need2reduce.gl')
train_set_2 = gl.SFrame("../data/train_set_2.gl")
test_set_2 = gl.SFrame("../data/test_set_2.gl")
orig_res = gl.SFrame("../data/orig_results.gl")

client = MongoClient()
# Access/Initiate Database
db = client['Podcast']
# Access/Initiate Table
Features = db['Features_noCategories']
print Features.count()

precision = []
prec_num  = []
recall    = []
recall_num= []

for col in gl_cat_tfidf.column_names()[:-1]:
    cols = ['Title']
    if col == 'Title':
        continue
    cols.append(col)
    item_model = gl.item_similarity_recommender.create(train_set_2, user_id="user_id", 
                                                       item_id="Title", item_data=gl_cat_tfidf[cols],
                                                       verbose=False)
    new_res = item_model.evaluate_precision_recall(test_set_2, cutoffs=[1,2,3,4,5], verbose=False)
    new_res = new_res['precision_recall_overall']
    compare_p = sum(orig_res['precision']<new_res['precision'])
    compare_r = sum(orig_res['recall']<new_res['recall'])
    if compare_p>0 or compare_r>0:
        p_max = np.array(orig_res['precision']- new_res['precision']).max()
        r_max = np.array(orig_res['recall']- new_res['recall']).max()
        Features.insert_one( {'Feature': col, 'Precision': compare_p, 
                      'Recall': compare_r, 'Precision_max': p_max, 
                      'Recall_max':r_max})
        print "Precision: " + str(col)
        print "Recall: " + str(col)
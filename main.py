import time
from typing import Union
from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import uuid


app = FastAPI()

url = 'Coursera.csv'
df = pd.read_csv(url)
df['uid'] = [uuid.uuid4().__str__() for _ in range(df.shape[0])]

uc = ['Course URL', 'Course Rating', 'Skills', 'University','Difficulty Level']  
df = df.drop(columns=uc)
print('\n', df.shape, '\n')
print(df.head())

df = df.rename(columns={'Course Name': 'course_title',
               'Course Description': 'course_desc'})
cv = TfidfVectorizer()
tfidf_matrix = cv.fit_transform(df['course_title']+'  '+df['course_desc'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df.index, index=df['course_title'])
titles = df['course_title']


def recommendations(course_title):
    test = {n.lower(): n for n in titles}
    find_close_match = []
    # find_close_match=[test[r] for r in  test.keys() if course_title.lower() in r]
    for r in test.keys():
        if course_title.lower() in r:
            find_close_match = [test[r]]
            break

    if len(find_close_match) != 0:
        close_match = find_close_match[0]
        index_of_movie = df[df['course_title'] == close_match].index.values[0]
        sim_scores = list(enumerate(cosine_sim[index_of_movie]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        course_indices = {df['uid'][i[0]]: titles.iloc[i[0]]
                          for i in sim_scores}
        return course_indices
    return {'result': 'No Results'}


@app.get("/url/")
def read_root(q: Union[str, None] = None):
    try:
        start_time = time.time()
        data = recommendations(q)
        return {"data": data, "timeTaken": time.time()-start_time, 'Count': len(data)}
    except Exception as e:
        return {'eee': str(e)}

# print(df[df['course_title'].str.contains(sys.argv[1],case=False)].course_title.to_list())

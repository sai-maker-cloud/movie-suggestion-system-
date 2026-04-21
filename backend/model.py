import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df=pd.read_csv("https://raw.githubusercontent.com/rashida048/Some-NLP-Projects/master/movie_dataset.csv")

features=['keywords','cast','genres','director']

for feature in features:
    df[feature]=df[feature].fillna('')

def combine_features(row):
    return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']
df['combined_features']=df.apply(combine_features,axis=1)
vectorizer=CountVectorizer()
count_matrix=vectorizer.fit_transform(df['combined_features'])
cosine_sim=cosine_similarity(count_matrix)
def get_recommendations(movie_name):
    try:
        movie_name = movie_name.lower().strip()

        matching_movies = df[df.title.str.lower().str.contains(movie_name)]

        if matching_movies.empty:
            return []

        movie_index = matching_movies.index[0]

        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        results = []

        for movie in sorted_movies[1:11]:
            index = movie[0]
            score = round(movie[1], 3)
            title = df.iloc[index]["title"]

            results.append({
                "title": title,
                "score": score
            })

        return results

    except Exception as e:
        print("ERROR in model:", e)
        return []
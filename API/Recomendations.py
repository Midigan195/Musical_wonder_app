import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(query, connection, anime_id, num_items):

    music_df = pd.read_sql(query, connection)

    if anime_id not in music_df['Anime_id'].values:
        return None

    # Combine selected columns into a single column for text processing (excluding 'Anime_id' and 'Image')
    music_df['combined_text'] = music_df[['Name', 'Description', 'Writer', 'Genre', 'Year']].apply(lambda x: ' '.join(x.astype(str)), axis=1)

    # Create a document-term matrix using CountVectorizer
    vectorizer = CountVectorizer()
    dtm = vectorizer.fit_transform(music_df['combined_text'])

    # Calculate cosine similarity between music items
    cosine_sim = cosine_similarity(dtm, dtm)

    # Find the index of the anime with the given name
    idx = music_df[music_df['Anime_id'] == anime_id].index[0]

    # Calculate cosine similarity scores for the given anime
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    total_items = len(sim_scores) - 1  # Exclude the item itself
    num_items = min(num_items, total_items)

    # Get top recommendations (excluding itself)
    sim_scores = sim_scores[1:(num_items + 1)]
    anime_indices = [i[0] for i in sim_scores]

    # Return only the 'Name', 'Anime_id', and 'Image' columns for each recommended anime
    return music_df[['Name', 'Anime_id', 'Image']].iloc[anime_indices]

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from models import Product

class RecommendationEngine:
    def __init__(self, products: List[Product]):
        self.products = products
        self.df = self._prepare_data(products)
        self.tfidf_matrix = None
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self._fit()

    def _prepare_data(self, products: List[Product]):
        data = []
        for p in products:
            data.append({
                'id': p.id or str(hash(p.name)),
                'content': f"{p.name} {p.description} {' '.join(p.tags)} {p.category}"
            })
        return pd.DataFrame(data)

    def _fit(self):
        if not self.df.empty:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.df['content'])

    def get_similar_products(self, product_id: str, top_n: int = 5):
        if self.tfidf_matrix is None or self.df.empty:
            return []
        
        try:
            idx = self.df.index[self.df['id'] == product_id].tolist()[0]
        except IndexError:
            return []

        cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        
        product_indices = [i[0] for i in sim_scores]
        return [self.products[i] for i in product_indices]

    def get_user_recommendations(self, user_interactions: List[dict], top_n: int = 5):
        # A simple hybrid approach: find products similar to those the user interacted with
        if not user_interactions or self.df.empty:
            return self.products[:top_n] # Fallback to featured
        
        # Aggregate user interests based on interacted products
        interacted_indices = []
        for interaction in user_interactions:
            pid = interaction['product_id']
            idx_list = self.df.index[self.df['id'] == pid].tolist()
            if idx_list:
                interacted_indices.append(idx_list[0])
        
        if not interacted_indices:
            return self.products[:top_n]

        # Calculate average similarity to all interacted products
        cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        user_scores = cosine_sim[interacted_indices].mean(axis=0)
        
        sim_scores = list(enumerate(user_scores))
        # Filter out already seen products
        sim_scores = [s for i, s in enumerate(sim_scores) if i not in interacted_indices]
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[:top_n]
        
        product_indices = [i[0] for i in sim_scores]
        return [self.products[i] for i in product_indices]

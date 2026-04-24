import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from schemas.schemas import ClusterGroup

def get_cluster_label(titles: list[str]) -> str:
    if not titles:
        return "General"
    sorted_titles = sorted(titles, key=lambda x: len(x))
    return sorted_titles[0][:40]

def cluster_titles(titles: list[str], n_clusters: int = 5) -> list[ClusterGroup]:
    if not titles:
        return []

    n_clusters = min(n_clusters, len(titles))

    try:
        print(f"[clustering] Vectorizing {len(titles)} titles with TF-IDF...")

        # ── Step 1: TF-IDF vectorization ──
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=500,
            ngram_range=(1, 2)
        )
        embeddings = vectorizer.fit_transform(titles).toarray()
        embeddings = normalize(embeddings)

        # ── Step 2: KMeans clustering ──
        print(f"[clustering] Running KMeans with {n_clusters} clusters...")
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10
        )
        labels = kmeans.fit_predict(embeddings)

        # ── Step 3: Group titles by cluster ──
        clusters: dict[int, list[str]] = {}
        for idx, label in enumerate(labels):
            clusters.setdefault(int(label), []).append(titles[idx])

        # ── Step 4: Get top TF-IDF keywords as cluster label ──
        feature_names = vectorizer.get_feature_names_out()
        result = []

        for cluster_id, cluster_titles_list in clusters.items():
            # get keyword from cluster center
            center = kmeans.cluster_centers_[cluster_id]
            top_indices = center.argsort()[-3:][::-1]
            keywords = [feature_names[i] for i in top_indices]
            label = " | ".join(keywords)

            result.append(ClusterGroup(
                cluster_id=cluster_id,
                label=label,
                topics=cluster_titles_list
            ))

        result.sort(key=lambda x: len(x.topics), reverse=True)
        print(f"[clustering] Created {len(result)} clusters ✅")
        return result

    except Exception as e:
        print(f"[clustering] Error: {e}")
        return []
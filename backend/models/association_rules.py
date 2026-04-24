from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
from schemas.schemas import AssociationRule

def extract_keywords(title: str) -> list[str]:
    """Extract meaningful keywords from a title"""
    import re
    # Remove special chars, lowercase
    title = re.sub(r'[^a-zA-Z\s]', '', title.lower())
    
    # Common stopwords to remove
    stopwords = {
        "the", "a", "an", "is", "it", "in", "on", "at", "to", "for",
        "of", "and", "or", "but", "with", "this", "that", "are", "was",
        "be", "as", "by", "from", "will", "not", "have", "has", "do",
        "its", "i", "my", "we", "our", "you", "your", "they", "their",
        "he", "she", "his", "her", "what", "how", "why", "when", "who",
        "so", "if", "me", "us", "about", "up", "out", "can", "get",
        "im", "more", "than", "been", "would", "could", "should", "now"
    }
    
    words = [w for w in title.split() if w not in stopwords and len(w) > 3]
    return list(set(words))  # unique keywords per title

def build_association_rules(titles: list[str]) -> list[AssociationRule]:
    """
    Runs Apriori algorithm on post titles to find
    keyword association rules like: AI → jobs, AI → future
    """
    if len(titles) < 5:
        return []

    try:
        print(f"[association_rules] Building rules from {len(titles)} titles...")

        # ── Step 1: Build transactions (each title = basket of keywords) ──
        transactions = [extract_keywords(title) for title in titles]
        transactions = [t for t in transactions if len(t) > 1]  # need 2+ keywords

        if len(transactions) < 3:
            print("[association_rules] Not enough transactions")
            return []

        # ── Step 2: Encode transactions ──
        te = TransactionEncoder()
        te_array = te.fit_transform(transactions)
        df = pd.DataFrame(te_array, columns=te.columns_)

        # ── Step 3: Find frequent itemsets ──
        print("[association_rules] Running Apriori...")
        frequent_itemsets = apriori(
            df,
            min_support=0.05,       # appears in 5% of posts
            use_colnames=True,
            max_len=2               # pairs only
        )

        if frequent_itemsets.empty:
            print("[association_rules] No frequent itemsets found, lowering support...")
            frequent_itemsets = apriori(
                df,
                min_support=0.02,   # lower threshold fallback
                use_colnames=True,
                max_len=2
            )

        if frequent_itemsets.empty:
            print("[association_rules] Still no itemsets found")
            return []

        # ── Step 4: Generate association rules ──
        rules = association_rules(
            frequent_itemsets,
            metric="confidence",
            min_threshold=0.3
        )

        if rules.empty:
            print("[association_rules] No rules generated")
            return []

        # ── Step 5: Sort by confidence and return top rules ──
        rules = rules.sort_values("confidence", ascending=False)

        result = []
        for _, row in rules.head(15).iterrows():
            antecedents = list(row["antecedents"])
            consequents = list(row["consequents"])

            if not antecedents or not consequents:
                continue

            result.append(AssociationRule(
                antecedent=" + ".join(antecedents),
                consequent=" + ".join(consequents),
                confidence=round(float(row["confidence"]), 3),
                support=round(float(row["support"]), 3)
            ))

        print(f"[association_rules] Generated {len(result)} rules ✅")
        return result

    except Exception as e:
        print(f"[association_rules] Error: {e}")
        return []
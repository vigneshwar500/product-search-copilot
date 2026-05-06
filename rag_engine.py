from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import pandas as pd
import re

# Load CSV data
df = pd.read_csv("products.csv")

products = (
    df["name"] + " - " +
    df["description"] + " - " +
    df["price"].astype(str)
).tolist()

# Split documents
splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)
docs = splitter.create_documents(products)

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector DB
db = FAISS.from_documents(docs, embeddings)


# 🔍 Search function
def search_product(query):
    query = query.lower()

    # ✅ FAQ SUPPORT
    if "return policy" in query:
        return ["You can return products within 7 days."]
    if "delivery time" in query:
        return ["Delivery usually takes 3-5 days."]
    if "refund" in query:
        return ["Refund will be processed within 5 working days."]

    # Semantic search
    results = db.similarity_search(query, k=5)

    # ✅ PRICE FILTER (cheap / low)
    if "cheap" in query or "low" in query:
        results = sorted(results, key=lambda x: int(x.page_content.split("-")[-1]))

    # ✅ PRICE RANGE FILTER (e.g. under 20000)
    price_limit = re.search(r'\d+', query)
    if price_limit:
        limit = int(price_limit.group())
        results = [
            r for r in results
            if int(r.page_content.split("-")[-1]) <= limit
        ]

    # ✅ CATEGORY FILTER
    if "phone" in query:
        results = [r for r in results if "phone" in r.page_content.lower()]
    if "shoes" in query:
        results = [r for r in results if "shoes" in r.page_content.lower()]
    if "tv" in query:
        results = [r for r in results if "tv" in r.page_content.lower()]

    # Return top 3 results
    return [r.page_content for r in results[:3]] if results else ["No matching product found."]

from haystack.retriever.dense import EmbeddingRetriever
import pandas as pd


from haystack.document_store.elasticsearch import ElasticsearchDocumentStore

document_store = ElasticsearchDocumentStore(host="localhost", username="", password="",
                                            index="document",
                                            embedding_field="question_emb",
                                            embedding_dim=768,
                                            excluded_meta_data=["question_emb"])


retriever = EmbeddingRetriever(document_store=document_store, embedding_model="deepset/sentence_bert", use_gpu=True)

# Download

# Get dataframe with columns "question", "answer" and some custom metadata
df = pd.read_csv("atlassian_qna_v1.csv")
# Minimal cleaning
df.fillna(value="", inplace=True)
df["Question"] = df["Question"].apply(lambda x: x.strip())
print(df.head())

# Get embeddings for our questions from the FAQs
questions = list(df["Question"].values)
df["question_emb"] = retriever.embed_queries(texts=questions)
df = df.rename(columns={"answer": "text"})

# Convert Dataframe to list of dicts and index them in our DocumentStore
docs_to_index = df.to_dict(orient="records")
document_store.write_documents(docs_to_index)

# docs_to_indexfinder = Finder(reader=None, retriever=retriever)
# prediction = finder.get_answers_via_similar_questions(question="I need a developer license for a test instance. How do I get one?", top_k_retriever=10)
# print_answers(prediction, details="all")

print("Indexing completed")

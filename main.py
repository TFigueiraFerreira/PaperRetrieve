from Bio import Entrez
Entrez.email = "tfigueiraferreira@gmail.com"

def retrieving_papers(subject):
    handle = Entrez.esearch(db="pubmed", term=subject, retmax=5)
    results = Entrez.read(handle)
    handle.close()
    return results["IdList"]


def subject_overview(id_list):
    handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml")
    papers = Entrez.read(handle)
    handle.close()
    overviews = []

    for article in papers["PubmedArticle"]:
        title = article["MedlineCitation"]["Article"]["ArticleTitle"]

        if "Abstract" in article["MedlineCitation"]["Article"]:
            overview = article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]
        else:
            overview = "No abstract available"

        overviews.append((title, overview))

    return overviews

from transformers import pipeline

overviewer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def overview_text(text):
    overview = overviewer(text, max_length=500, min_length=30, do_sample=False)
    return overview[0]['summary_text']

def search_and_overview(subject):
    ids = retrieving_papers(subject)
    articles = subject_overview(ids)
    overviews = [(title, overview_text(overview)) for title, overview in articles]
    return overviews

subject = "diabetes"
results = search_and_overview(subject)
for title, summary in results:
    print(f"Title: {title}\nSummary: {summary}\n")
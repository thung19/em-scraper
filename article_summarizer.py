from transformers import pipeline
import torch


def summarize(article_attributes):
    summarizer = pipeline('summarization',model="facebook/bart-large-cnn")
    text =""
    
    #print(summarizer(text, max_length=250, min_length = 80, do_sample = False))
     
    
    
    for item in article_attributes:
        title = item.get("title", "")
        date = item.get("date", "")
        url = item.get("url", "")
        content = item.get("content","")

        content = (content or "").strip()
        if not content:
            combined_summary = ""
        elif len(content) <=120:
            combined_summary = content
        #If content length is greater than 3000, will split into 3000 char chunks and store in list
        elif len(content) > 3000:
            chunks = [content[i:i+3000] for i in range(0, len(content), 3000)]
            summaries = [summarizer(c, max_length=200, min_length=80, do_sample=False)[0]['summary_text'] for c in chunks]
            combined_summary = summarizer(" ".join(summaries), max_length=250, min_length=100, do_sample=False)[0]['summary_text']
        else:
            combined_summary = summarizer(content, max_length=200, min_length=80, do_sample=False)[0]['summary_text']

        '''
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Date: {date}")
        print()
        print("Summary")
        print(f"{combined_summary}\n")
        '''

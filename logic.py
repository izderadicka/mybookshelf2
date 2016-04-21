from sqlalchemy.sql import text,desc,func
import model

def preprocess_search_query(text):
    tokens=text.split()
    return ' & '.join(['%s:*'%t for t in tokens])

def search_query(q, search):
    search=preprocess_search_query(search)
    
    q.filter(model.Ebook.full_text.match(search))\
    .order_by(desc(func.ts_rank_cd(model.Ebook.full_text, func.to_tsquery(text("'custom'"), search))))
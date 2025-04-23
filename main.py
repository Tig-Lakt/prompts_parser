from fastapi import FastAPI, HTTPException
from typing import List, Dict
from fastapi.responses import HTMLResponse

from parsing import open_page
from constants import ALLOWED_CATEGORIES_LIST


app = FastAPI()


@app.get("/prompts/{category}")
async def get_prompts(category: str) -> List[Dict]:
    
    if category.capitalize() not in ALLOWED_CATEGORIES_LIST:
        raise HTTPException(status_code=400, detail="Недопустимая категория.  Допустимые категории: " + ", ".join(ALLOWED_CATEGORIES_LIST))

    links_prompt = await open_page(category)
    
    if links_prompt is None:
        prompts_text = "Не удалось получить промпты.  Возможно, проблема с парсингом сайта."

    else:
        prompts_text = f"Список ссылок на бесплатные промпты категории {category}<br><br>"
        for link in links_prompt:
            prompts_text = prompts_text + link + '<br>'
        
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Free prompts</title>
    </head>
    <body>
        <h3>{prompts_text}</h3>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
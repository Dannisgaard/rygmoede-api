import uvicorn
from app import app


@app.get("/")
async def read_root():
    return {"title": "Rygmøde app, husker de øl vi smager på til møderene."}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
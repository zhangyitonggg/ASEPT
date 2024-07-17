from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import backend.conf as conf

conf.init()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

from backend.routers import problem_file_upload, create_user, security, admin, user_group, news, problems

app.include_router(problem_file_upload.router)
app.include_router(create_user.router)
app.include_router(security.router)
app.include_router(admin.router)
app.include_router(user_group.router)
app.include_router(news.router)
app.include_router(problems.router)

@app.get("/print/{info}")
async def print_(info: str):
    print(info)
    return {"info": info}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='run_backend:app', host="localhost", port=8000, reload=True)
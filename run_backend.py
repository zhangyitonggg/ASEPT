from fastapi import FastAPI
import backend.conf as conf

conf.init()
app = FastAPI()

from backend.routers import problem_file_upload, create_user, security, admin

app.include_router(problem_file_upload.router)
app.include_router(create_user.router)
app.include_router(security.router)
app.include_router(admin.router)

@app.get("/print/{info}")
async def print_(info: str):
    print(info)
    return {"info": info}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='run_backend:app', host="0.0.0.0", port=8000, reload=True)
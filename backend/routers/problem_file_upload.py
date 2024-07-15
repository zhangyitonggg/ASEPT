from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query
import shutil

import backend.utils.convert as convert
import backend.conf as conf
import backend.routers.security as security

router = APIRouter(
    prefix='/problem_file_upload',
)

@router.post("/")
def problem_file_upload(
    file: UploadFile = File(...),
    user: str = Depends(security.get_current_user),
):
    file_path = conf.UPLOAD_DIRECTORY / convert.md5_filename(file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    res = convert.convert2text(file_path)
    if res == None:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and IMAGE files are allowed."
        )
    else:
        return {"text": res}
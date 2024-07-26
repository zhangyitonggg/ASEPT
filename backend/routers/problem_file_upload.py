from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query
import shutil

import backend.utils.convert as convert
import backend.conf as conf
import backend.routers.security as security
from backend.data.User import Permissions, User

router = APIRouter(
    prefix='/problem_file_upload',
)

@router.post("/")
def problem_file_upload(
    file: UploadFile = File(...),
    user: User = Depends(security.get_user),
):
    if file.size > conf.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size too large."
        )
    if user.permissions.get("UPLOAD_FILE") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied."
        )
    # file_path = conf.UPLOAD_DIRECTORY / convert.md5_filename(file.filename)
    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)
    # res = convert.convert2text(file_path)
    # if res == None:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Only PDF and IMAGE files are allowed."
    #     )
    # else:
    #     return {"text": res}
    return {"text": "hhhhhhhh"}
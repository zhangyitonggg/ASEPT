# 后端说明

开发版本：

- python 3.12.2

运行前，先执行 `pip install fastapi uvicorn` （fastapi 开发用）

依赖项目：

- MariaDB

```
pip install pymysql
pip install yaml
pip install pyyaml
pip install hashlib
```

- Redis

```
pip install redis
pip install yaml
pip install jwt
pip install datetime
```

- PDF/image 转文字

```
pip install pytesseract
pip install hashlib
pip install PIL
pip install pdf2image
pip install tempfile
pip install shutil
```

通过 `py run_backend.py` 运行后端。

运行后端后，可以通过访问 `http://0.0.0.0:8000/docs` 查看 API 说明文档。

# 前端说明

<font color="red">前端要是先写了 API 接口在 README 里写一下。</font>
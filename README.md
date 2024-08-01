# BUAA 2024 Python大作业
## ASEPT

## **后端：** 

Python版本：3.12.2

在项目目录下打开终端，执行：pip install -r requirements.txt

此外，对于运行Windows系统的电脑，需要从 https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine 下载 tesseract 并确保安装有chi_sim.traineddata，从 https://github.com/oschwartz10612/poppler-windows/releases 下载 poppler，并把路径填写在/backend/utils/convert.py里；对于运行Linux系统的电脑，需要安装tesseract-ocr和poppler-utils（对于使用apt包管理器的系统，对应的命令为sudo apt install tesseract-ocr poppler-utils），并从https://github.com/tesseract-ocr/tessdata/blob/main/chi_sim.traineddata 下载chi_sim.traineddata到/usr/share/tesseract-ocr/5/tessdata下。

安装好以上依赖后，执行：python run_backend.py启动后端。如果后端监听的端口不 8000，则可能需要重置网络以正常运行。

## **前端：**

打开终端执行：npm install vue-cli -g

在admin_frontend和frontend目录下打开终端，分别执行npm install安装所需的依赖包。

如果在安装过程中出现网络问题，请设置代理。

在安装完依赖包之后，在admin_frontend和frontend目录下打开终端，分别执行npm run serve运行前端，根据提示在浏览器里打开页面即可。

 
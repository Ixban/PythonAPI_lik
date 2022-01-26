pip install pyinstaller
pyinstaller --clean  --noupx --add-data "templates;templates" --add-data "static;static"  main.py
powershell Compress-Archive dist\main\.  dist\distribucion_servicio.zip -Force
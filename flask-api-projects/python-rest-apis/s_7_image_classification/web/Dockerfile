FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# we can also install the spacy pakage using online methods by executing below commands
# python -m spacy download en_core_web_sm
EXPOSE 5000
# CMD [ "python", "app.py" ]
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "app.py"]

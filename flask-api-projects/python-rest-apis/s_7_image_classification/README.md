#build an image
docker-compose build

#run the image
docker-compose up

# - this combines the commands

docker-compose up --build

The model is present in below path - download it
https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz

O/P - http://localhost:5000/

//for live reload in docker compose

if **name** == "**main**":
app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)

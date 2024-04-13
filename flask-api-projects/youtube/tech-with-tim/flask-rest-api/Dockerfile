FROM python:3
# inside the machine(container) working directory should be /usr/src/app
WORKDIR /usr/src/app
# copy the requirements
COPY requirements.txt .
# run pip install with no cache recursively
RUN pip install --no-cache-dir -r requirements.txt
# copy current files (app.py and requirements.txt) into system current working directory
COPY . .
Expose 5000
# this will list files in directory
RUN ls -la
# execute the command
CMD ["python","main.py"]
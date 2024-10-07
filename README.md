# FlaskWebAppExample
This is a Flask web application that runs a python script on local machine. 

app.py requests the user to upload a input text or csv file and a number to indicate the number of times the local python script should be executed in parallel using the Thread Python module
To make the upload process efficient in case of larger files, the upload is done in chunks. 

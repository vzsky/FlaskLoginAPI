# FlaskLoginAPI
# start!
Works on python3
```
# clone the project repo.
git clone https://github.com/vzsky/FlaskLoginAPI.git directory
cd directory

# make virtualenvironment and install requirement
mkvirtualenv sample 
pip install -r requirements.txt

# run api server
python app.py
```
# structure
- POST ```{"user":"VZSKY", "pass:"SOMEPASS"}``` to /login return ```{"token":TOKEN}```
- POST ```{"token":TOKEN}``` to /token return full data

full data
```
   {
    "annouce": [
                  [anc1,...],
                  [anc2,...]
               ]
     "user" :  { 
                  "user" : "VZSKY",
                  "first" : "Touch",
                  "last" : "S."
               }
   }
```
     

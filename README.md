## What is this project?  
a simple CRUD app to keep track of utility companies, accounts, amounts, bill and due dates, and their websites

## Why this project?  
twofold: 
- learn flask
- keep track of our utilities in one shared space

### requirements  
an .env file with the following variables set:
- DB_NAME=dbname.sqlite (right now only sqlite databases are supported)
- SECRET_KEY=random-string-of-characters (can generate with `openssl rand -base64 32`)
- ADMIN_USERNAME=yourname
- ADMIN_EMAIL=youremail
- ADMIN_PASSWORD=yourpassword

---

before you start using the app, run `python create_user.py` to create the database and insert the admin user (a registration module *may* follow later but for now, only one account is needed)

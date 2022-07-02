from flask import request, Flask, render_template, redirect
import json

database = {}
app = Flask(__name__)
app.config.update(
  DEBUG = True,
)

try: database = eval(open("database.json", "r", encoding="utf-8").read())
except: open("database.json", "w", encoding="utf-8").write("{}")

def update_database(): open("database.json", "w", encoding="utf-8").write(json.dumps(database, indent=4))

@app.route("/")
def index(): return render_template("home.html")

@app.route("/short", methods=["POST","GET"])
def shorter():
  base_url = '/'.join(request.base_url.split("/")[0:3])
  if request.method.lower() == "post":
    url = request.form.get("url").strip()
    if (url==''): return render_template("error.html", data={'message':"Don't leave the link null!"})
    else:
      try:
        if url in list(database.values()):
          lid = list(database.keys())[list(database.values()).index(url)]
          short_link = f"{base_url}/{lid}"
          # print(short_link)
        else:
          lid = str(len(database)+1)
          database[lid] = url
          update_database()
          short_link = f"{base_url}/{lid}"
      except: return render_template("error.html", data={'message':'Something is wrong!'})
    
    return render_template('short.html', data={'short_url':short_link})
  else: return redirect('/')

@app.errorhandler(404)
def page_not_found(e): return render_template('error.html', data={'message': 'Page Not Found'}), 404

@app.route("/<int:lid>")
def redirect_to_url(lid):
  try: return redirect(database[lid])
  except: return render_template("error.html", data={'message':'Something is wrong!'})

app.run() if __name__=='__main__' else quit("\r\n  [!] run `python3 UrlShorter.py` command. \n")

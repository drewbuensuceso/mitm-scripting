from flask import Flask, render_template
import mitm_scripting

app = Flask(__name__)

headings = ("Product", "Price")
data = (
    ("Pencil", "2000"),
    ("Ballpen", "4000")
)

@app.route("/")
def table():
    data = mitm_scripting.response_df
    return(render_template("table.html", headings=headings, data=data))
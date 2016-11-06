from flask import Flask, request, redirect
import twilio.twiml
app = Flask(__name__)

import datetime
print(datetime.date.day)

@app.route("/user/<string:meals>")
def hello_monkey(meals):
    """Respond to incoming calls with a simple text message."""

    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey " + meals)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
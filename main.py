import os
import base64

from flask import Flask, request
from model import Message 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        m = Message(content=request.form['content'])
        m.save()

    body = """
<html>
<body>
<h1>Class Message Board</h1>
<h2>Contribute to the Knowledge of Others</h2>
<form method="POST">
    <textarea name="content"></textarea>
    <input type="submit" value="Submit">
</form>

<h2>Wisdom From Your Fellow Classmates</h2>
"""
    
    for m in Message.select():
        body += """
<div class="message">
{}
</div>
""".format(m.content.replace('<', '&lt;').replace('>', '&gt;'))
# The XSS attack relied on the use of control characters. In this case, the control characters were for HTML: the
# greater than (>) and less than (<) or angle bracket characters. By replacing these with equivalent HTML escape
# sequences, we were able to render the submitted text of an attacker's message without allowing them to insert
# JavaScript code into the page.
# There are more HTML control characters than just the angle brackets. The best practice to use when rendering user-
# submitted content into an HTML page is to sanitize that content with the html.escape method.

    return body 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)


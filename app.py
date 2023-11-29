from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import bcrypt
from db import query_db, modify_db, upload_message


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('signin.html')

@app.route('/index')
def index():
    return render_template('index.html')


globalname = ""
@app.route('/signin', methods=['POST','GET'])
def signin():
    global globalname
    if request.method == 'POST':
        username = request.form['username']

        globalname=username
        entered_password = request.form['password']
        try:
            result = query_db("SELECT password FROM users WHERE username = %s", (username,), one=True)

            # If the user is found in the database
            if result:
                stored_hashed_password = result[0]
                entered_password_bytes = entered_password.encode('utf-8')
                stored_hashed_password_bytes = stored_hashed_password.encode('utf-8')

                # Check if the entered password matches the stored hashed password
                if bcrypt.checkpw(entered_password_bytes, stored_hashed_password_bytes):
                    return redirect(url_for('index'))
                else:
                    return "Invalid username or password", 401
            else:
                return "User not found", 404

        except Exception as e:
            print(e)
            return "An error occurred", 500
        print("Form data received", username, entered_password)

    else:
        return render_template('signin.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/searchuser',methods=['POST'])
def searchuser():
    user = request.json.get('user')
    try:
        result = query_db("SELECT password FROM users WHERE username = %s", (user,), one=True)
        if result:
            return jsonify(username=user)
        else:
            flash('User not found','danger')
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/sendmessage',methods=['POST'])
def sendmessage():
    message = request.form['text-message']
    recipient_username = request.form['form-recipient-id']
    user_username = globalname

    recipient_id = query_db("SELECT id FROM users WHERE username = %s", (recipient_username,), one=True)
    user_id = query_db("SELECT id FROM users WHERE username = %s", (user_username,), one=True)

    upload_message(user_id,recipient_id,message)
    return "Message sent successfully"





def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            confirmPassword = request.form['confirmPassword']

            if confirmPassword != password:
                return "Passwords Don't Match"

            hashed = hash_password(password)


            modify_db("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
            return redirect(url_for('signin'))  # Redirect to the signin route
        except Exception as e:
            # Handle errors...
            return f"An error occurred: {e}"

    else:
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)

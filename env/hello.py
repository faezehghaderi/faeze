from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    status= None
    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']   
    #return render_template('index.html', name=name,items=['hi','how are'],rstatus=['you select ',status])
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Encrypt') == 'Encrypt':
                # pass
            print("Encrypted", request.form['alg'])
        elif  request.form.get('Decrypt') == 'Decrypt':
            # pass # do something else
            print("Decrypted")
        else:
            # pass # unknown
            return render_template("index.html")
    elif request.method == 'GET':
            # return render_template("index.html")
        print("No Post Back Call")
    return render_template('index1.html')




# =============================================================================
# @app.route("/", methods=['GET', 'POST'])
#     def index():
#         print(request.method)
#         if request.method == 'POST':
#             if request.form.get('Encrypt') == 'Encrypt':
#                 # pass
#                 print("Encrypted")
#             elif  request.form.get('Decrypt') == 'Decrypt':
#                 # pass # do something else
#                 print("Decrypted")
#             else:
#                 # pass # unknown
#                 return render_template("index.html")
#         elif request.method == 'GET':
#             # return render_template("index.html")
#             print("No Post Back Call")
#         return render_template("index.html")
# 
# 
# =============================================================================



# =============================================================================
# @app.route('/')
# def hello():
#     return "Hello World!"
# 
# if __name__ == '__main__':
#     app.run()
# 
# =============================================================================

if __name__ == '__main__':
    app.run(debug=True)





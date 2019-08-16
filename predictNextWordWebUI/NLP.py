from flask import Flask, render_template, request, redirect
from nextWord import makeModel,returnTop5
app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        input_string = request.form['Input text']
        return render_template('index.html', input=freq(input_string))
    else:
        return render_template('index.html')

def freq(s):
    #s = input()
    char_count = {}
    for c in s:
        if c in char_count.keys():
            char_count[c] = char_count[c] + 1
        else:
            char_count[c] = 1
    #print("The frequency of the character's are:")
    return char_count

@app.route('/ajax', methods=['POST', 'GET'])
def ajax():
    
    argstring = request.args.get('words', '')
    print(model)
    tt = returnTop5(model,argstring)
    print(tt)
    if request.method == 'POST':
        return str(tt)
    else:
        return str(tt)


if __name__  == "__main__":
    global model
    model = makeModel()
    

    app.run(debug = True)
    

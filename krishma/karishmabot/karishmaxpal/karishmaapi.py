'''
Simple Flask API to receive a message as a JSON object and return a response as a JSON object.
'''
messagelogfile="../data/messagelog"
from datetime import datetime
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/listener', methods=["POST"])
def listener():
     input_json = request.get_json(force=True) 
     dictToReturn = {
                        'from':input_json['sender'],
                        'text':input_json['text'],
                        'timercvd': datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")    
                    }  # This is the response that will be returned to the user    
    
     with open(messagelogfile, 'a') as f:
         f.write(str(dictToReturn) + '\n')
     # send dictToReturn to processing function
     result = process_message(dictToReturn)
     return jsonify(dictToReturn)

def process_message(message):
    # do something with the message
    return message

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





    

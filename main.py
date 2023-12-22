from flask import Flask, request, Response
from db_handler import DB_Handler
from scrape_handler import scrape
import json

app = Flask(__name__)
db = DB_Handler()


@app.route('/salve_info', methods=['POST'])
def salve_info():
    if request.is_json != True:
        return Response("Invalid Request", status=400)
    
    try:
        url = request.json['url']
    except:
        return Response("Missing or Invalid URL parameter", status=400)
    
    scraped_data = scrape(url)

    if scraped_data['error'] == True:
        return Response("Failed to scrape site.", status=500)

    db.save_website(url, scraped_data)
    
    return Response("Saved", status=200)

@app.route('/get_info', methods=['GET'])
def get_info():
    try:
        url = request.args.get('url')
    except:
        return Response("Missing or Invalid URL parameter", status=400)
    
    result = db.get_website(url)

    if result == None:
        return Response("Not found", status=404)

    return Response(json.dumps(result), status=200, content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)
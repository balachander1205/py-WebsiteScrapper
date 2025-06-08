import logging
from flask import Flask,render_template, request,json,Response
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS, cross_origin
from website_scrapper import web_scrapper, parse_table_data

app = Flask(__name__)
CORS(app)

# swagger config
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : 'Sample flask Application'
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)


@app.route('/')
@cross_origin()
def hello():
    return 'Welcome to Sample flask Application!'

@app.route('/home')
@cross_origin()
def parkingManagement():
    return render_template('index.html')

@app.route('/api/web/scrapper', methods=['POST'])    
@cross_origin()
def websiteScrapper():
    data = json.loads(request.data)
    url = data.get('link', '')
    _response_ = web_scrapper(url)
    print(_response_) 
    return json.dumps(_response_);


@app.route('/api/web/scrapper/profiles', methods=['POST'])    
@cross_origin()
def profileScrapper():
    data = json.loads(request.data)
    url = data.get('link', '')
    _response_ = parse_table_data(url)
    print(_response_) 
    return json.dumps(_response_);

if __name__=="__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)    
    logging.info('Started')
    app.run(host='127.0.0.1', port=5001,debug=True, threaded=True)

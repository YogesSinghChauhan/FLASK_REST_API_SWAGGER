from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from flasgger import LazyString, LazyJSONEncoder


app = Flask(__name__)


app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

template = dict(
    swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
)

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, config=swagger_config, template=template)


@app.route('/chat', methods=['POST'])
@swag_from('swagger_config.yml')
def chat():
    result={}
    data = request.get_json()
    marks=data['Marks']
    subject = data['Subject']
    if marks <33:
        result[subject]='fail'
    else:
        result[subject]='pass'

    return jsonify(result)  


@app.route('/subject', methods=['POST'])
@swag_from('swagger_config_subject.yml')
def total_subject():
    data = request.get_json()
    subject = data['Subject']
    

    return jsonify({'subject':subject})  


if __name__ == '__main__':
    app.run(debug=True)

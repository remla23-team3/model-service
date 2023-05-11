from flask import Flask, request
from flasgger import Swagger
from markdown import markdown
from pygments.formatters import HtmlFormatter

from model_training.predicting import predict_single_review

app = Flask(__name__)
swagger = Swagger(app)

# create a route for the app at "/" that serves the content from the README.md file
@app.route('/')
def home():
    """
    Home endpoint.
    ---
    responses:
      200:
        description: README.md content.
    """
    readme_content = open("README.md", "r").read()
    page_content = markdown(readme_content, extensions=['fenced_code'])

    return page_content

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict sentiment of a restaurant review.
    ---
    consumes:
      - application/json
    parameters:
      - name: review
        in: body
        required: true
        schema:
          type: object
          required: content
          properties:
            content:
              type: string
              example: "This is a great restaurant!"
    definitions:
      Review:
        type: object
        properties:
          content:
            type: string
          sentiment:
            type: number
            minimum: 0
            maximum: 1
    responses:
      200:
        description: Restaurant review with predicted sentiment.
        schema:
          $ref: '#/definitions/Review'
      400:
        description: Error message.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid request."
    """

    review_data = request.get_json()
    review_content = review_data['content']

    prediction = predict_single_review(review_content)
    
    return {
        'content': review_content,
        'sentiment': prediction
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6789)

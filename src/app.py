from flask import Flask, request
from flasgger import Swagger

# TODO: fetch model from `model-training` repository.
from sentiment_analysis.model import model
from sentiment_analysis.preprocess import prepare

app = Flask(__name__)
swagger = Swagger(app)

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

    raw_data = request.get_json()
    restaurant_review = prepare(raw_data)
    prediction = model.predict(restaurant_review)
    
    return {
        'prediction': prediction,
    }

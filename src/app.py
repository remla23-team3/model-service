from flasgger import Swagger
from flask import Flask, request

from model_training.src.models.predict_model import predict_single


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

    review_data = request.get_json()
    review_content = review_data['content']

    prediction = predict_single(review_content)
    
    return {
        'content': review_content,
        'sentiment': prediction
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6789)

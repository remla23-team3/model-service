from flasgger import Swagger
from flask import Flask, request
import urllib.request
import pickle
import joblib

from model_training.src.models.predict_model import predict_single


app = Flask(__name__)
swagger = Swagger(app)


def download_models():
    # google drive auto-downloadable link
    classifier_URL = 'https://drive.google.com/uc?export=download&id=1Jxnu5e0eiv6RAgdGnHZton5IMv2wyHTn'
    bow_URL ='https://drive.google.com/uc?export=download&id=12j3aHN8336FGhceGPoKv1wS2lIE3s_HH'

    cv_path, proba = urllib.request.urlretrieve(bow_URL,
                                                 filename="c1_BoW_Sentiment_Model.pkl")
    classifier_path, proba = urllib.request.urlretrieve(classifier_URL,
                                                 filename="c2_Classifier_Sentiment_Model")
    print(cv_path)
    print(classifier_path)

    with open(cv_path, 'rb') as f:
        cv = pickle.load(f)

    classifier = joblib.load(classifier_path)

    return cv, classifier



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
    cv, classifier = download_models()


    review_data = request.get_json()
    review_content = review_data['content']

    prediction = predict_single(review_content, classifier, cv)
    
    return {
        'content': review_content,
        'sentiment': prediction
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6789)

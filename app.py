from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

movie_reviews = {}
review_id_counter = 1

@app.route('/reviews', methods=['POST'])
def create_review():
    global review_id_counter
    data = request.json
    if not all(k in data for k in ("title", "review", "rating", "reviewer")):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_review = {
        "id": review_id_counter,
        "title": data["title"],
        "review": data["review"],
        "rating": data["rating"],
        "reviewer": data["reviewer"]
    }
    movie_reviews[review_id_counter] = new_review
    review_id_counter += 1
    return jsonify(new_review), 201

@app.route('/reviews', methods=['GET'])
def get_reviews():
    return jsonify(list(movie_reviews.values())), 200

@app.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = movie_reviews.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review), 200

@app.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = movie_reviews.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    
    data = request.json
    review.update({
        "title": data.get("title", review["title"]),
        "review": data.get("review", review["review"]),
        "rating": data.get("rating", review["rating"]),
        "reviewer": data.get("reviewer", review["reviewer"])
    })
    return jsonify(review), 200

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = movie_reviews.pop(review_id, None)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({"message": "Review deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)

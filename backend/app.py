from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}

# Create database
with app.app_context():
    db.create_all()

# Routes
@app.route("/api/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    new_item = Item(name=data["name"], description=data.get("description", ""))
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@app.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get_or_404(item_id)
    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)
    db.session.commit()
    return jsonify(item.to_dict())

@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, jsonify

app = Flask(__name__)

notes = []

@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json
    notes.append({"id": len(notes) + 1, "text": data["text"]})
    return jsonify({"message": "Note added!"}), 201

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return jsonify({"message": "Note deleted!"})

if __name__ == "__main__":
    app.run(debug=True)

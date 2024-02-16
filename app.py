from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/info')
def get_info():
  info_data = {
    "name": "Holy Bible API",
    "version": "1.0.0",
    "translations": ["American Standard Version (1901)", "King James Version"]
  }
  return jsonify(info_data)

#if __name__ == '__main__':
#  app.run(debug=True)

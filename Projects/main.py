import requests
from flask import Flask, request, jsonify
from pytrends.request import TrendReq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/trends', methods=['GET'])
def get_trends():
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            return jsonify({"error": "Missing keyword"}), 400

        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

        pytrend = TrendReq(hl='en-US', tz=330, requests_args={'headers': session.headers})
        pytrend.build_payload([keyword])
        data = pytrend.interest_over_time()

        if data.empty:
            return jsonify({"error": "No data found"}), 404

        result = [
            {"date": str(date.date()), "interest": int(value)}
            for date, value in zip(data.index, data[keyword])
        ]

        return jsonify(result)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)

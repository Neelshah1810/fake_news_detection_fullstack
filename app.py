from flask import Flask, request, render_template, jsonify
import features  # Import your features code
from g4f.client import Client
from dl_model import predict_news

app = Flask(__name__)

# Initialize GPT-4 client
client = Client()

# Function to check news with GPT-4
def check_news_with_gpt4(headline):
    try:
        prompt = (
            f"Evaluate the following news headline and determine if it is 'Real News' or 'Fake News'. "
            f"Respond with only 'Real News' or 'Fake News'. Consider common signs of fake news such as sensationalism, lack of credible sources, and implausibility.\n\n"
            f"News Headline: '{headline}'"
        )
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip().lower()
        if "real" in result:
            result = "Real News"
        elif "fake" in result:
            result = "Fake News"
        else:
            result = "Unable to determine"
        return result
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_headline', methods=['POST'])
def detect_headline():
    data = request.get_json()
    headline = data.get('headline')
    method = data.get('method')  # Get the method (dl or g4f)
    
    if method == 'g4f':
        result = check_news_with_gpt4(headline)
    elif method == 'dl':
        result = predict_news(headline)
    else:
        result = "Invalid method"
    
    return jsonify({'result': result})

@app.route('/search_news', methods=['POST'])
def search_news():
    query = request.form.get('query')
    url = features.search_news(query)
    return jsonify({'url': url})


@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form.get('user_input')
    response = features.get_response(user_input)
    return jsonify({'response': response})

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/global_news')
def global_news():
    global_news = features.get_top_news()
    return render_template('news.html', title="Global News", news=global_news)

@app.route('/india_news')
def india_news():
    india_news = features.get_top_news_for_india()
    return render_template('news.html', title="India News", news=india_news)

@app.route('/check_url_safety', methods=['POST'])
def check_url_safety():
    data = request.get_json()  # Fetch JSON data from the request
    url = data.get('url')

    if not url:
        return jsonify({'result': 'No URL provided'}), 400  # Handle missing URL

    try:
        api_key = 'AIzaSyB_lsa8oM10TlKWt72E4CrkZYvLWfzOU-Y'  # Use your actual API key
        result = features.check_url_safety(api_key, url)  # This function should return a string result
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'result': f'Error: {str(e)}'}), 500  # Return any errors

if __name__ == '__main__':
    app.run(debug=True)
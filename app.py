from flask import Flask, render_template, request, jsonify
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def generate_summary(text, num_sentences):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize each sentence into words
    words = [word_tokenize(sentence) for sentence in sentences]
    
    # Flatten the list of words
    flattened_words = [word for sublist in words for word in sublist]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words_without_stopwords = [word.lower() for word in flattened_words if word.lower() not in stop_words and word.isalnum()]
    
    # Join words into a single string for TF-IDF vectorization
    processed_text = ' '.join(words_without_stopwords)
    
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the processed text
    tfidf_matrix = vectorizer.fit_transform([processed_text])
    
    # Get feature names (words)
    feature_names = vectorizer.get_feature_names_out()
    
    # Calculate TF-IDF scores for each word
    word_scores = {}
    for word, score in zip(feature_names, tfidf_matrix.toarray()[0]):
        word_scores[word] = score
    
    # Create a dictionary to keep the score of each sentence
    sentence_scores = {}
    for sentence in sentences:
        sentence_scores[sentence] = 0
        for word in word_tokenize(sentence):
            if word.lower() in word_scores:
                sentence_scores[sentence] += word_scores[word.lower()]
    
    # Sort sentences by their scores
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    
    # Select top N sentences
    summary = ' '.join(ranked_sentences[:num_sentences])
    
    return summary.strip()

def analyze_sentiment(text):
    # Use TextBlob for sentiment analysis
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    # Determine sentiment based on polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        text = data.get('text', '')
        length = int(data.get('length', 1))
        
        # Generate summary
        summary = generate_summary(text, length)
        
        # Analyze sentiment of the summary
        sentiment = analyze_sentiment(summary)
        
        response = {
            'summary': summary,
            'sentiment': sentiment
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5020)

from textblob import TextBlob

phrases = ["Can you recommend some upscale restaurants in New York?",
           "What are the famous places we should not miss in Russia?"]

for phrase in phrases:
    print("-" * 100)
    print("Input_phrase: ", phrase)
    print("-" * 100)
    
    analysis = TextBlob(phrase)
    
    # Perform sentiment analysis
    sentiment = analysis.sentiment
    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity
    
    # Classify sentiment
    if polarity > 0:
        sentiment_label = "Positive"
    elif polarity < 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    
    print("Sentiment: {}, Polarity: {:.2f}, Subjectivity: {:.2f}".format(sentiment_label, polarity, subjectivity))

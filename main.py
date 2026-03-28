import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Sample data
data = {
    'text': [
        'Win money now',
        'Hello how are you',
        'Free offer just for you',
        'Let’s meet tomorrow',
        'Claim your prize now'
    ],
    'label': [1, 0, 1, 0, 1]  # 1 = spam, 0 = not spam
}

df = pd.DataFrame(data)

# Convert text to numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

# Train model
model = MultinomialNB()
model.fit(X, y)

# Test
test = [input("Enter a message: ")]
test_vec = vectorizer.transform(test)
prediction = model.predict(test_vec)

print("Spam" if prediction[0] == 1 else "Not Spam")
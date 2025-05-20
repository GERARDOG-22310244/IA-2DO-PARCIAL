import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from nltk import ngrams
from nltk.tokenize import word_tokenize
import tensorflow as tf
import tensorflow_probability as tfp
from sklearn.feature_extraction.text import CountVectorizer

tfd = tfp.distributions

# ----------------------------
# 1. Modelos de N-gramas
# ----------------------------

class NGramLanguageModel:
    def __init__(self, n=2):
        self.n = n
        self.ngram_counts = defaultdict(Counter)
        self.vocab = set()
    
    def train(self, corpus):
        """Entrena un modelo de n-gramas con suavizado de Laplace"""
        for sentence in corpus:
            tokens = word_tokenize(sentence.lower())
            self.vocab.update(tokens)
            for ngram in ngrams(tokens, self.n, pad_left=True, pad_right=False):
                prefix = ' '.join(ngram[:-1])
                self.ngram_counts[prefix][ngram[-1]] += 1
    
    def probability(self, word, context):
        """Calcula P(word|context) con suavizado de Laplace"""
        context = ' '.join(context)
        total = sum(self.ngram_counts[context].values())
        vocab_size = len(self.vocab)
        return (self.ngram_counts[context][word] + 1) / (total + vocab_size)
    
    def generate_text(self, seed, length=10):
        """Genera texto usando el modelo"""
        context = seed.split()[-self.n+1:] if self.n > 1 else []
        generated = list(context)
        
        for _ in range(length):
            context_str = ' '.join(context)
            next_word_probs = {
                word: self.probability(word, context)
                for word in self.ngram_counts[context_str]
            }
            next_word = max(next_word_probs.items(), key=lambda x: x[1])[0]
            generated.append(next_word)
            context = generated[-(self.n-1):] if self.n > 1 else []
        
        return ' '.join(generated)

# Ejemplo de uso
corpus = [
    "El lenguaje humano es complejo",
    "El lenguaje de programación Python es poderoso",
    "El aprendizaje probabilístico es fundamental en NLP",
    "Los modelos de lenguaje predicen palabras"
]

ngram_model = NGramLanguageModel(n=2)
ngram_model.train(corpus)

print("Ejemplo de generación de texto:")
print(ngram_model.generate_text("El lenguaje", length=5))

# ----------------------------
# 2. Modelo de Bolsa de Palabras Probabilístico
# ----------------------------

class ProbabilisticBagOfWords:
    def __init__(self):
        self.word_probs = None
        self.class_probs = None
    
    def train(self, X, y):
        """Entrena un modelo Naive Bayes multinomial"""
        vectorizer = CountVectorizer()
        X_counts = vectorizer.fit_transform(X)
        self.vocab = vectorizer.get_feature_names_out()
        
        # Calcular P(clase)
        class_counts = np.bincount(y)
        self.class_probs = class_counts / class_counts.sum()
        
        # Calcular P(palabra|clase) con suavizado
        self.word_probs = np.zeros((len(np.unique(y)), len(self.vocab)))
        for c in np.unique(y):
            class_mask = (y == c)
            word_counts = X_counts[class_mask].sum(axis=0) + 1  # Laplace smoothing
            total_words = word_counts.sum()
            self.word_probs[c] = word_counts / total_words
    
    def predict_proba(self, text):
        """Predice probabilidades para cada clase"""
        word_indices = [i for i, word in enumerate(self.vocab) if word in text.lower()]
        log_probs = np.log(self.class_probs) + np.sum(np.log(self.word_probs[:, word_indices]), axis=1)
        return np.exp(log_probs) / np.sum(np.exp(log_probs))

# Ejemplo de uso
X_text = ["python programación código", "lenguaje humano comunicación", 
          "algoritmo datos python", "habla lenguaje lingüística"]
y_classes = [0, 1, 0, 1]  # 0=programación, 1=lingüística

bow_model = ProbabilisticBagOfWords()
bow_model.train(X_text, y_classes)

print("\nPredicción probabilística para 'python lenguaje':")
print(bow_model.predict_proba("python lenguaje"))

# ----------------------------
# 3. Modelo Neuronal Probabilístico para NLP
# ----------------------------

def build_probabilistic_lstm(vocab_size, embedding_dim=64):
    """Construye un modelo LSTM con incertidumbre"""
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim),
        
        # LSTM con dropout recurrente probabilístico
        tf.keras.layers.LSTM(128, return_sequences=True, 
                            recurrent_dropout=0.2, dropout=0.2),
        
        # Capa densa bayesiana
        tfp.layers.DenseVariational(
            units=64,
            make_prior_fn=lambda t: tfd.Normal(loc=0., scale=1.),
            make_posterior_fn=lambda t: tfp.util.TransformedVariable(
                tf.random.normal(shape=[128, 64]),
                bijector=tfp.bijectors.Identity()),
            kl_weight=1/1000
        ),
        
        # Salida probabilística
        tf.keras.layers.Dense(vocab_size),
        tfp.layers.DistributionLambda(lambda t: tfd.Categorical(logits=t))
    ])
    
    model.compile(
        optimizer=tf.optimizers.Adam(0.01),
        loss=lambda y, p_y: -p_y.log_prob(y),
        metrics=['accuracy']
    )
    
    return model

# Ejemplo simplificado (requiere preparación de datos más completa)
vocab_size = 1000  # Tamaño del vocabulario
model = build_probabilistic_lstm(vocab_size)

# ----------------------------
# Visualización de Distribuciones
# ----------------------------

def plot_word_distribution(model, word, context_words, ngram_model):
    """Visualiza la distribución de palabras siguientes"""
    context = context_words.split()
    probs = []
    words = []
    
    for w in ngram_model.vocab:
        if w != word:
            p = ngram_model.probability(w, context)
            probs.append(p)
            words.append(w)
    
    # Tomar las top 10 palabras
    top_indices = np.argsort(probs)[-10:]
    top_words = [words[i] for i in top_indices]
    top_probs = [probs[i] for i in top_indices]
    
    plt.figure(figsize=(10, 5))
    plt.barh(top_words, top_probs)
    plt.title(f"Distribución de probabilidad para palabras siguientes a '{' '.join(context)}'")
    plt.xlabel("Probabilidad")
    plt.show()

plot_word_distribution(ngram_model, "lenguaje", "el", ngram_model)
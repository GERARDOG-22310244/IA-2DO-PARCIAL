import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_probability as tfp
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

tfd = tfp.distributions
tfpl = tfp.layers

# 1. Modelo Probabilístico de Percepción Visual (Filtros Bayesianos)
class BayesianPerception:
    def __init__(self, image_shape=(8, 8)):
        self.image_shape = image_shape
        self.prior = None
        self.posterior = None
    
    def learn_prior(self, images):
        """Aprende la distribución previa de los píxeles"""
        # Modelar cada píxel como una distribución Bernoulli independiente
        self.prior = tfd.Independent(
            tfd.Bernoulli(probs=np.mean(images, axis=0)),
            reinterpreted_batch_ndims=2
        )
    
    def update_posterior(self, observed_images):
        """Actualiza la distribución posterior dado datos observados"""
        # Actualización bayesiana simple (para demostración)
        alpha = np.mean(observed_images, axis=0) + 1  # Suavizado
        beta = (1 - np.mean(observed_images, axis=0)) + 1
        self.posterior = tfd.Independent(
            tfd.Beta(alpha, beta),
            reinterpreted_batch_ndims=2
        )
    
    def reconstruct_image(self, noisy_image):
        """Reconstrucción probabilística de imágenes"""
        if self.posterior is None:
            raise ValueError("Entrenar el modelo primero")
        
        # Muestreo de la distribución posterior
        reconstructed_probs = self.posterior.sample()
        reconstructed = (reconstructed_probs > 0.5).astype(np.float32)
        return reconstructed
    
    def visualize_distributions(self):
        """Visualiza las distribuciones previa y posterior"""
        plt.figure(figsize=(12, 5))
        
        plt.subplot(131)
        plt.imshow(self.prior.probs.numpy(), cmap='gray')
        plt.title('Distribución Previa (Medias)')
        plt.colorbar()
        
        plt.subplot(132)
        plt.imshow(self.posterior.mean().numpy(), cmap='gray')
        plt.title('Distribución Posterior (Medias)')
        plt.colorbar()
        
        plt.subplot(133)
        plt.imshow(self.posterior.variance().numpy(), cmap='hot')
        plt.title('Incertidumbre Posterior (Varianza)')
        plt.colorbar()
        
        plt.tight_layout()
        plt.show()

# Cargar dataset de dígitos
digits = load_digits()
X = digits.images / 16.0  # Normalizar
X_binary = (X > 0.5).astype(np.float32)  # Convertir a binario

# Entrenar modelo bayesiano
bp = BayesianPerception()
bp.learn_prior(X_binary)
bp.update_posterior(X_binary[:100])  # Usar solo 100 muestras

# Visualizar distribuciones
bp.visualize_distributions()

# 2. Red Neuronal Probabilística para Clasificación Visual
def build_probabilistic_cnn(input_shape=(8, 8, 1), num_classes=10):
    """Construye una CNN con capas probabilísticas"""
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=input_shape),
        
        # Capa convolucional con dropout espacial
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.SpatialDropout2D(0.2),
        tf.keras.layers.MaxPooling2D(),
        
        # Capa convolucional bayesiana
        tfpl.Convolution2DFlipout(
            64, 3, activation='relu',
            kernel_prior_fn=tfp.layers.default_multivariate_normal_fn,
            kernel_posterior_fn=tfp.layers.default_mean_field_normal_fn(is_singular=False)
        ),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        
        # Capa densa con incertidumbre
        tfpl.DenseVariational(
            units=128,
            make_prior_fn=lambda t: tfd.Normal(loc=0., scale=1.),
            make_posterior_fn=lambda t: tfp.util.TransformedVariable(
                tf.random.normal(shape=[7*7*64, 128]),
                bijector=tfp.bijectors.Identity()),
            kl_weight=1/X.shape[0]
        ),
        
        # Capa de salida probabilística
        tfpl.DenseVariational(
            units=tfpl.OneHotCategorical.params_size(num_classes),
            make_prior_fn=lambda t: tfd.Normal(loc=0., scale=1.),
            make_posterior_fn=lambda t: tfp.util.TransformedVariable(
                tf.random.normal(shape=[128, tfpl.OneHotCategorical.params_size(num_classes)]),
                bijector=tfp.bijectors.Identity()),
            kl_weight=1/X.shape[0]
        ),
        tfpl.OneHotCategorical(event_size=num_classes)
    ])
    
    model.compile(
        optimizer=tf.optimizers.Adam(0.001),
        loss=lambda y, p_y: -p_y.log_prob(y),
        metrics=['accuracy']
    )
    
    return model

# Preparar datos para CNN
X_cnn = np.expand_dims(X, -1)  # Añadir dimensión de canal
y = digits.target
X_train, X_test, y_train, y_test = train_test_split(X_cnn, y, test_size=0.2)

# Entrenar modelo
pcnn = build_probabilistic_cnn()
history = pcnn.fit(
    X_train, 
    tf.one_hot(y_train, 10),
    epochs=30,
    batch_size=32,
    validation_data=(X_test, tf.one_hot(y_test, 10))
)

# 3. Visualización de Incertidumbre en Predicciones
def analyze_uncertainty(model, X_sample, n_samples=100):
    """Analiza la incertidumbre en las predicciones"""
    y_probs = []
    for _ in range(n_samples):
        y_prob = model(X_sample, training=True)  # Muestreo durante predicción
        y_probs.append(y_prob.probs_parameter().numpy())
    
    y_probs = np.stack(y_probs)
    
    plt.figure(figsize=(15, 5))
    
    # Visualizar imagen de entrada
    plt.subplot(131)
    plt.imshow(X_sample[0].squeeze(), cmap='gray')
    plt.title('Imagen de Entrada')
    
    # Visualizar media de predicciones
    plt.subplot(132)
    plt.bar(range(10), np.mean(y_probs[:, 0], axis=0))
    plt.title('Probabilidades Promedio')
    plt.xlabel('Clase')
    plt.ylabel('Probabilidad')
    
    # Visualizar incertidumbre
    plt.subplot(133)
    plt.bar(range(10), np.std(y_probs[:, 0], axis=0))
    plt.title('Incertidumbre en Predicciones')
    plt.xlabel('Clase')
    plt.ylabel('Desviación Estándar')
    
    plt.tight_layout()
    plt.show()

# Ejemplo con imagen ambigua (mezcla de dígitos)
ambiguous_image = np.clip((X[0] + X[1])/2, 0, 1)  # Mezcla dos dígitos
analyze_uncertainty(pcnn, np.expand_dims(np.expand_dims(ambiguous_image, 0), -1))
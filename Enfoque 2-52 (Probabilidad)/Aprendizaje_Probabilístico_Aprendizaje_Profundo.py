import tensorflow as tf
import tensorflow_probability as tfp
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons

tfd = tfp.distributions
tfpl = tfp.layers

# 1. Generar datos de ejemplo (media luna)
X, y = make_moons(n_samples=1000, noise=0.1, random_state=42)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis')
plt.title("Datos de Entrenamiento")
plt.show()

# 2. Modelo probabilístico con capas Bayesianas
def construir_modelo_probabilistico():
    modelo = tf.keras.Sequential([
        # Capa densa con incertidumbre en los pesos (Bayesiana)
        tfpl.DenseVariational(
            units=16,
            input_shape=(2,),
            make_prior_fn=lambda t: tfd.Normal(loc=0., scale=1.),
            make_posterior_fn=lambda t: tfp.util.TransformedVariable(
                tf.random.normal(shape=[2, 16]),
                bijector=tfp.bijectors.Identity()),
            kl_weight=1/X.shape[0],
            activation='relu'
        ),
        
        # Capa densa estándar
        tf.keras.layers.Dense(32, activation='relu'),
        
        # Capa de salida probabilística
        tfpl.DenseVariational(
            units=tfpl.OneHotCategorical.params_size(2),
            make_prior_fn=lambda t: tfd.Normal(loc=0., scale=1.),
            make_posterior_fn=lambda t: tfp.util.TransformedVariable(
                tf.random.normal(shape=[32, tfpl.OneHotCategorical.params_size(2)]),
                bijector=tfp.bijectors.Identity()),
            kl_weight=1/X.shape[0],
        ),
        
        # Distribución de salida categórica
        tfpl.OneHotCategorical(event_size=2, convert_to_tensor_fn=tfd.Distribution.mode)
    ])
    
    modelo.compile(
        optimizer=tf.optimizers.Adam(learning_rate=0.01),
        loss=lambda y, p_y: -p_y.log_prob(y),
        metrics=['accuracy']
    )
    
    return modelo

# 3. Entrenamiento del modelo
modelo = construir_modelo_probabilistico()
history = modelo.fit(X, tf.one_hot(y, depth=2), epochs=100, verbose=0)

# 4. Visualización del aprendizaje
plt.plot(history.history['accuracy'], label='Precisión')
plt.title('Curva de Aprendizaje')
plt.xlabel('Época')
plt.ylabel('Precisión')
plt.legend()
plt.show()

# 5. Predicción con incertidumbre
def predecir_con_incertidumbre(modelo, X, n_muestras=100):
    """Realiza predicciones muestreando de la distribución posterior"""
    y_pred_list = []
    for _ in range(n_muestras):
        y_pred = modelo(X, training=True)  # Muestrear pesos durante predicción
        y_pred_list.append(y_pred.numpy())
    
    y_preds = np.stack(y_pred_list)
    return y_preds

# Ejemplo de predicción con incertidumbre
X_test = np.array([[0.5, -0.5], [1.5, 0.5]])
y_probs = predecir_con_incertidumbre(modelo, X_test)

print("\nPredicciones con incertidumbre:")
for i, (x, probs) in enumerate(zip(X_test, y_probs.mean(axis=0))):
    print(f"\nPunto {i+1}: {x}")
    print(f"Clase 0: {probs[0]:.3f} ± {y_probs[:,i,0].std():.3f}")
    print(f"Clase 1: {probs[1]:.3f} ± {y_probs[:,i,1].std():.3f}")

# 6. Visualización de la frontera de decisión con incertidumbre
def plot_decision_boundary_with_uncertainty(modelo, X, y, n_muestras=50):
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 50),
                         np.linspace(y_min, y_max, 50))
    
    grid = np.c_[xx.ravel(), yy.ravel()]
    probs = predecir_con_incertidumbre(modelo, grid, n_muestras)
    mean_probs = probs.mean(axis=0)
    uncertainty = probs.std(axis=0).sum(axis=1)
    
    plt.figure(figsize=(12, 5))
    
    # Plot mean predictions
    plt.subplot(121)
    Z = mean_probs[:, 1].reshape(xx.shape)
    plt.contourf(xx, yy, Z, levels=20, cmap='viridis', alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='white', cmap='viridis')
    plt.title("Predicción Media")
    
    # Plot uncertainty
    plt.subplot(122)
    Z_uncertainty = uncertainty.reshape(xx.shape)
    plt.contourf(xx, yy, Z_uncertainty, levels=20, cmap='plasma', alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='white', cmap='viridis')
    plt.title("Incertidumbre de Predicción")
    
    plt.tight_layout()
    plt.show()

plot_decision_boundary_with_uncertainty(modelo, X, y)
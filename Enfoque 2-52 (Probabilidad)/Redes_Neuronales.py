import tensorflow as tf
import tensorflow_probability as tfp
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

tfd = tfp.distributions
tfpl = tfp.layers

# 1. Generar datos de clasificación no lineal
X, y = make_classification(n_samples=1000, n_features=10, n_classes=3, 
                          n_clusters_per_class=1, n_informative=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Construir red neuronal probabilística
def construir_red_neuronal_probabilistica():
    modelo = tf.keras.Sequential([
        # Capa de entrada
        tf.keras.layers.Input(shape=(10,)),
        
        # Capa oculta con dropout probabilístico (aleatorización)
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        
        # Capa bayesiana con distribución sobre los pesos
        tfpl.DenseVariational(
            units=32,
            make_prior_fn=lambda t: tfd.Normal(loc=0., scale=1.),
            make_posterior_fn=lambda t: tfp.util.TransformedVariable(
                tf.random.normal(shape=[64, 32]),
                bijector=tfp.bijectors.Identity()),
            kl_weight=1/X_train.shape[0],
            activation='relu'
        ),
        
        # Capa de salida probabilística
        tfpl.DenseVariational(
            units=tfpl.OneHotCategorical.params_size(3),
            make_prior_fn=lambda t: tfd.Normal(loc=0., scale=1.),
            make_posterior_fn=lambda t: tfp.util.TransformedVariable(
                tf.random.normal(shape=[32, tfpl.OneHotCategorical.params_size(3)]),
                bijector=tfp.bijectors.Identity()),
            kl_weight=1/X_train.shape[0]
        ),
        
        # Distribución de salida categórica
        tfpl.OneHotCategorical(event_size=3, convert_to_tensor_fn=tfd.Distribution.mode)
    ])
    
    modelo.compile(
        optimizer=tf.optimizers.Adam(learning_rate=0.005),
        loss=lambda y, p_y: -p_y.log_prob(y),
        metrics=['accuracy']
    )
    
    return modelo

# 3. Entrenamiento del modelo
modelo = construir_red_neuronal_probabilistica()
history = modelo.fit(
    X_train, 
    tf.one_hot(y_train, depth=3), 
    epochs=100, 
    batch_size=32,
    validation_data=(X_test, tf.one_hot(y_test, depth=3)),
    verbose=1
)

# 4. Evaluación del modelo
def evaluar_modelo(modelo, X_test, y_test, n_muestras=100):
    # Predicción puntual
    y_pred = modelo.predict(X_test[:5])
    print("\nEjemplos de predicción:")
    for i in range(5):
        print(f"Real: {y_test[i]}, Predicho: {np.argmax(y_pred[i])}")
    
    # Evaluación de incertidumbre
    y_probs = []
    for _ in range(n_muestras):
        y_prob = modelo(X_test, training=True)
        y_probs.append(y_prob.numpy())
    
    y_probs = np.stack(y_probs)
    mean_probs = np.mean(y_probs, axis=0)
    std_probs = np.std(y_probs, axis=0)
    
    print("\nIncertidumbre en predicciones (primeros 3 ejemplos):")
    for i in range(3):
        print(f"\nEjemplo {i+1}:")
        for c in range(3):
            print(f"Clase {c}: {mean_probs[i,c]:.3f} ± {std_probs[i,c]:.3f}")

# 5. Visualización de resultados
def plot_resultados(history):
    plt.figure(figsize=(12, 4))
    
    plt.subplot(121)
    plt.plot(history.history['accuracy'], label='Entrenamiento')
    plt.plot(history.history['val_accuracy'], label='Validación')
    plt.title('Precisión durante Entrenamiento')
    plt.xlabel('Época')
    plt.ylabel('Precisión')
    plt.legend()
    
    plt.subplot(122)
    plt.plot(history.history['loss'], label='Entrenamiento')
    plt.plot(history.history['val_loss'], label='Validación')
    plt.title('Pérdida durante Entrenamiento')
    plt.xlabel('Época')
    plt.ylabel('Pérdida')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Ejecutar evaluación y visualización
evaluar_modelo(modelo, X_test, y_test)
plot_resultados(history)

# 6. Interpretación probabilística
def interpretar_incertidumbre(modelo, X_sample, n_muestras=500):
    probs = []
    for _ in range(n_muestras):
        prob = modelo(X_sample, training=True)
        probs.append(prob.numpy())
    
    probs = np.stack(probs)
    
    plt.figure(figsize=(10, 5))
    for i in range(3):
        plt.hist(probs[:, 0, i], bins=30, alpha=0.7, label=f'Clase {i}')
    
    plt.title('Distribución de Probabilidades para una Muestra')
    plt.xlabel('Probabilidad')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.show()

# Ejemplo de interpretación
interpretar_incertidumbre(modelo, X_test[:1])
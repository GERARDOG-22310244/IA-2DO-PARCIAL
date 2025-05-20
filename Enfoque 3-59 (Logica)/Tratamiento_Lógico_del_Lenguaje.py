import nltk
from nltk import word_tokenize, pos_tag
from nltk.sem import logic
from nltk.sem.logic import LogicParser, ApplicationExpression, Variable, LambdaExpression
from sympy import symbols, Function, And, Or, Not, Implies, ForAll, Exists
import re

# Descargar recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

## ----------------------------
## 1. Representación Lógica de Frases
## ----------------------------

class TraductorLogico:
    def __init__(self):
        self.lexico = {
            'hombre': 'hombre',
            'mujer': 'mujer',
            'perro': 'perro',
            'gato': 'gato',
            'camina': 'camina',
            'corre': 'corre',
            'duerme': 'duerme',
            'ama': 'ama',
            'todo': 'all',
            'algún': 'some',
            'ningún': 'no',
            'el': 'el',
            'la': 'la',
            'un': 'un',
            'una': 'una'
        }
        self.parser = LogicParser()
    
    def analizar_oracion(self, oracion):
        """Convierte una oración en representación lógica"""
        tokens = word_tokenize(oracion.lower())
        tagged = pos_tag(tokens)
        return self._traducir(tagged)
    
    def _traducir(self, tagged_words):
        """Traduce palabras etiquetadas a lógica"""
        # Implementación simplificada
        if len(tagged_words) == 2 and tagged_words[1][1] == 'VBZ':
            # Oración simple: "Sujeto Verbo"
            sujeto = self.lexico.get(tagged_words[0][0], tagged_words[0][0])
            verbo = self.lexico.get(tagged_words[1][0], tagged_words[1][0])
            return f"{verbo}({sujeto})"
        
        if len(tagged_words) == 3 and tagged_words[1][1] == 'VBZ':
            # Oración con objeto: "Sujeto Verbo Objeto"
            sujeto = self.lexico.get(tagged_words[0][0], tagged_words[0][0])
            verbo = self.lexico.get(tagged_words[1][0], tagged_words[1][0])
            objeto = self.lexico.get(tagged_words[2][0], tagged_words[2][0])
            return f"{verbo}({sujeto},{objeto})"
        
        # Implementar más patrones gramaticales aquí
        return " ".join(word for word, tag in tagged_words)

## ----------------------------
## 2. Semántica de Eventos
## ----------------------------

class SemanticaEventos:
    def __init__(self):
        self.parser = LogicParser()
    
    def representar_evento(self, oracion):
        """Representa una oración como evento lógico"""
        tokens = word_tokenize(oracion.lower())
        
        # Identificar verbo y argumentos
        verbo = None
        sujeto = None
        objeto = None
        
        for word, tag in pos_tag(tokens):
            if tag.startswith('VB') and not verbo:
                verbo = word
            elif tag.startswith('NN') and not sujeto:
                sujeto = word
            elif tag.startswith('NN') and sujeto and not objeto:
                objeto = word
        
        if verbo and sujeto and objeto:
            e = Variable('e')  # Variable de evento
            return f"exists e.{verbo}(e) & sujeto(e,{sujeto}) & objeto(e,{objeto})"
        elif verbo and sujeto:
            e = Variable('e')
            return f"exists e.{verbo}(e) & sujeto(e,{sujeto})"
        else:
            return oracion

## ----------------------------
## 3. Resolución de Referencias
## ----------------------------

class ResolucionReferencias:
    def __init__(self):
        self.referencias = {}
        self.contador = 1
    
    def analizar_texto(self, texto):
        """Resuelve referencias anafóricas en un texto"""
        oraciones = nltk.sent_tokenize(texto)
        resultados = []
        
        for oracion in oraciones:
            tokens = word_tokenize(oracion)
            tagged = pos_tag(tokens)
            
            # Buscar pronombres y sustituir
            nueva_oracion = []
            for word, tag in tagged:
                if tag == 'PRP' and word.lower() in ['él', 'ella', 'lo', 'la']:
                    # Sustituir por la última referencia adecuada
                    ref = self._buscar_referencia(word.lower(), tagged)
                    nueva_oracion.append(ref if ref else word)
                else:
                    nueva_oracion.append(word)
                    
                    # Registrar nombres propios y sustantivos como referencias
                    if tag in ['NNP', 'NN']:
                        self.referencias[word.lower()] = word
            
            resultados.append(" ".join(nueva_oracion))
        
        return " ".join(resultados)
    
    def _buscar_referencia(self, pronombre, contexto):
        """Busca la referencia más probable para un pronombre"""
        genero = {
            'él': 'masculino',
            'lo': 'masculino',
            'ella': 'femenino',
            'la': 'femenino'
        }.get(pronombre.lower(), None)
        
        # Buscar el último sustantivo del género adecuado
        for word, tag in reversed(contexto):
            if tag in ['NNP', 'NN']:
                # En una implementación real usaríamos información de género
                return word
        
        return None

## ----------------------------
## 4. Inferencia en Lenguaje Natural
## ----------------------------

class InferenciaLenguaje:
    def __init__(self):
        self.base_conocimiento = []
    
    def agregar_hecho(self, hecho):
        """Agrega un hecho a la base de conocimiento"""
        self.base_conocimiento.append(hecho)
    
    def verificar_entailment(self, oracion):
        """Verifica si una oración se sigue de la base de conocimiento"""
        logica_oracion = self._convertir_a_logica(oracion)
        
        # Verificar si la negación es insatisfacible (simplificado)
        try:
            return not satisfiable(And(*self.base_conocimiento, Not(logica_oracion)))
        except:
            return False
    
    def _convertir_a_logica(self, oracion):
        """Convierte una oración a lógica de primer orden (simplificado)"""
        if "todo" in oracion.lower():
            match = re.match(r"todo (\w+) es (\w+)", oracion.lower())
            if match:
                x = symbols('x')
                return ForAll(x, Implies(Function(match.group(1))(x), Function(match.group(2))(x)))
        
        if "algún" in oracion.lower():
            match = re.match(r"algún (\w+) es (\w+)", oracion.lower())
            if match:
                x = symbols('x')
                return Exists(x, And(Function(match.group(1))(x), Function(match.group(2))(x)))
        
        # Implementar más patrones...
        return oracion

## ----------------------------
## Ejemplos de Uso
## ----------------------------

if __name__ == "__main__":
    print("=== Representación Lógica ===")
    traductor = TraductorLogico()
    oracion = "El hombre camina"
    logica = traductor.analizar_oracion(oracion)
    print(f"'{oracion}' -> {logica}")
    
    oracion2 = "La mujer ama al gato"
    logica2 = traductor.analizar_oracion(oracion2)
    print(f"'{oracion2}' -> {logica2}")
    
    print("\n=== Semántica de Eventos ===")
    sem_eventos = SemanticaEventos()
    evento = "Juan comió una manzana"
    rep_evento = sem_eventos.representar_evento(evento)
    print(f"'{evento}' -> {rep_evento}")
    
    print("\n=== Resolución de Referencias ===")
    resolutor = ResolucionReferencias()
    texto = "Pedro vio a María. Él sonrió. Ella lo saludó."
    texto_resuelto = resolutor.analizar_texto(texto)
    print(f"Original: {texto}")
    print(f"Resuelto: {texto_resuelto}")
    
    print("\n=== Inferencia en Lenguaje ===")
    inferencia = InferenciaLenguaje()
    inferencia.agregar_hecho(ForAll(symbols('x'), Implies(Function('hombre')('x'), Function('mortal')('x'))))
    inferencia.agregar_hecho(Function('hombre')('Socrates'))
    
    pregunta = "Sócrates es mortal"
    resultado = inferencia.verificar_entailment(pregunta)
    print(f"¿'{pregunta}' se sigue de la base de conocimiento? {resultado}")
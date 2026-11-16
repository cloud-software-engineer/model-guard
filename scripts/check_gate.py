import json
import sys

def main():
    try:
        # Intentamos leer como utf-8 (Linux) o utf-16 (Windows)
        try:
            with open('scan-results.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except UnicodeDecodeError:
            with open('scan-results.json', 'r', encoding='utf-16') as f:
                data = json.load(f)
                
        if data.get('verdict') == 'block':
            print('Veredicto: BLOQUEADO. Revisa el comentario en el PR.')
            sys.exit(1) # Falla el workflow intencionadamente
        else:
            print('Veredicto: PERMITIDO.')
            sys.exit(0)
            
    except Exception as e:
        print(f'Error al verificar el veredicto: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()
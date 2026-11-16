import json
import sys

def generate_comment(json_path: str) -> str:
    try:
        # Intento 1: Leer como UTF-8 (estándar en Linux/Mac y GitHub Actions)
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except UnicodeDecodeError:
        try:
            # Intento 2: Leer como UTF-16 (por culpa de PowerShell en Windows)
            with open(json_path, 'r', encoding='utf-16') as f:
                data = json.load(f)
        except Exception as e:
            return f"## Error al leer el informe de seguridad\n\nNo se pudo procesar el JSON (Encoding fallido): {str(e)}"
    except Exception as e:
        return f"## Error al leer el informe de seguridad\n\nNo se pudo procesar el JSON: {str(e)}"

    # Extraer datos del resumen
    summary = data.get('summary', {}).get('findings_by_severity', {})
    critical = summary.get('critical', 0)
    high = summary.get('high', 0)
    verdict = data.get('verdict', 'allow')

    # Si es seguro, mostramos el check verde
    if verdict != 'block' and critical == 0 and high == 0:
        return (
            "## AI Model Security Gate: **ALLOWED**\n\n"
            "No se encontraron hallazgos de severidad Alta o Crítica en los artefactos modificados."
        )

    # Si llegamos aquí, el PR está bloqueado
    body = "##  AI Model Security Gate: **BLOCKED**\n\n"
    body += "Este Pull Request introduce artefactos de modelo con hallazgos de seguridad.\n\n"
    
    # Tabla resumen
    body += "| Severidad | Hallazgos |\n| :--- | :--- |\n"
    body += f"| Crítica | {critical} |\n"
    body += f"| Alta | {high} |\n\n"

    # Listar los hallazgos principales
    findings = data.get('findings', [])
    top_findings = [f for f in findings if f.get('severity') in ['critical', 'high']]
    
    if top_findings:
        body += "### Principales Hallazgos\n"
        for f in top_findings[:3]: # Mostrar máximo 3 para no saturar
            title = f.get('title', 'Hallazgo desconocido')
            artifact = f.get('artifact_path', 'desconocido')
            desc = f.get('description', '')
            body += f"- **{f['severity'].upper()}**: {title} en `{artifact}`.\n"
            if desc:
                body += f"  *{desc}*\n"

    body += (
        "\n> **¿Cómo solucionarlo?** Revisa el archivo afectado. Si es un modelo de terceros, "
        "considera usar un formato más seguro como `.safetensors` en lugar de `.pkl`.\n\n"
    )
    body += "_Escaneado automáticamente por [Model Guard](https://github.com/cloud-software-engineer/model-guard)._"

    return body

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generate_comment.py <ruta_al_json>")
        sys.exit(1)

    comment = generate_comment(sys.argv[1])
    print(comment)
    
    with open('pr_comment.md', 'w', encoding='utf-8') as f:
        f.write(comment)
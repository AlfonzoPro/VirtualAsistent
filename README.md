# Planteamiento de Problema
En muchas organizaciones, empresas, o instituciones educativas, los usuarios necesitan cargar archivos en diferentes formatos (como documentos de texto, PDFs o Word) para analizarlos, compartir su contenido, o generar reportes. Sin embargo, no todas las plataformas son capaces de manejar múltiples formatos de manera eficiente. Esto genera inconvenientes tales como:
- Tiempo perdido al convertir documentos a formatos aceptados.
- Imposibilidad de leer o analizar el contenido sin herramientas externas.
- Riesgos de errores al procesar archivos manualmente.

Por ejemplo, en una oficina administrativa, los empleados podrían necesitar subir documentos de proyectos, actas de reuniones, o propuestas en diferentes formatos. Si la plataforma utilizada para gestionar estos documentos no admite formatos variados, los usuarios tendrían que recurrir a procesos externos para convertir los archivos, lo que ralentiza el flujo de trabajo y genera frustración.

# Solución:
Este código puede implementar una solución eficiente al permitir que los usuarios carguen archivos en una plataforma, leer su contenido independientemente del formato, y mostrarlo directamente en una interfaz web para su revisión. Al admitir archivos **.txt, .pdf, y .docx**, este sistema automatiza el proceso de lectura, eliminando la necesidad de conversión manual y facilitando el acceso al contenido.

# Herramientas Usadas
- Python
- Flask
- Librerías:  os, PyPDF2, docx (para el manejo de archivos)
- Librería: io (para el manejo de distintos tipos de E/S)

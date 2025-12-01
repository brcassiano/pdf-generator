from flask import Flask, request, send_file
from weasyprint import HTML
import io

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json(force=True)
        html_content = data.get('html', '')

        if not html_content:
            return {'error': 'HTML content is required'}, 400

        # Gerar PDF (API compatível com versões novas)
        html = HTML(string=html_content, base_url=".")
        pdf_bytes = html.write_pdf()

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='relatorio.pdf'
        )
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

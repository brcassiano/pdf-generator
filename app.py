from flask import Flask, request, send_file
from xhtml2pdf import pisa
import io

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200

def html_to_pdf_bytes(html: str) -> bytes:
    pdf_io = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        html,
        dest=pdf_io,
        encoding='utf-8'
    )
    if pisa_status.err:
        raise Exception('Error generating PDF with xhtml2pdf')
    return pdf_io.getvalue()

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json(force=True)
        html_content = data.get('html', '')

        if not html_content:
            return {'error': 'HTML content is required'}, 400

        pdf_bytes = html_to_pdf_bytes(html_content)

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

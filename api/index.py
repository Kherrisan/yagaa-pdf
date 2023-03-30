from flask import Flask, request, jsonify, send_file
import urllib.parse
import fitz
import requests

app = Flask(__name__)

@app.route('/test')
def home():
    return 'Hello, World!'

@app.route('/pdf', methods=['GET'])
def pdf():
    try:
        args = request.args
        title = urllib.parse.unquote(args.get('title'))
        pdf_url = urllib.parse.unquote(args.get('pdf'))
        print(title, pdf_url)
        pdf_resp = requests.get(pdf_url)
        pdf_resp_content = pdf_resp.content
        pdf_doc = fitz.Document(stream=pdf_resp_content, filetype="pdf")
        pdf_text = ''
        for i in range(pdf_doc.page_count):
            pdf_text += pdf_doc.get_page_text(i)
        pdf_text = pdf_text.replace('\n', '')
        return jsonify({'title': title, 'pageCnt': pdf_doc.page_count, 'text': pdf_text})
    except Exception as e:
        return jsonify({'msg': str(e), 'pdf_resp': pdf_resp_content})
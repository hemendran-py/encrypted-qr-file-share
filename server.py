from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/download/<filename>')
def download_file(filename):
    """Serves the encrypted file for download."""
    # TODO: Set the correct directory for encrypted files
    return send_from_directory('encrypted_files', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 
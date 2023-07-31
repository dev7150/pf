import azure.functions as func
import logging
import os
import base64
import io
import PyPDF2

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HttpTrigger", methods=["POST"])
def HttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the base64 encoded text from the request body
    try:
        req_body = req.get_json()
        encoded_text = req_body.get('base64_text')
    except ValueError:
        return func.HttpResponse(
            "Invalid request body. Please provide base64_text in the request JSON.",
            status_code=400
        )

    # Check if the base64 encoded text is provided
    if not encoded_text:
        return func.HttpResponse(
            "No base64_text provided in the request.",
            status_code=400
        )

    # Decode the base64 encoded text
    try:
        decoded_data = base64.b64decode(encoded_text)
    except Exception as e:
        return func.HttpResponse(
            f"Error decoding the base64_text: {str(e)}",
            status_code=400
        )

    # Create a PDF file with the decoded data
    try:
        pdf_file = create_pdf(decoded_data)
    except Exception as e:
        return func.HttpResponse(
            f"Error creating PDF: {str(e)}",
            status_code=500
        )

    # Return the PDF file in the HTTP response
    response = func.HttpResponse(pdf_file.getvalue(), mimetype='application/pdf')
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response

def create_pdf(decoded_data):
    # Create an in-memory buffer for the PDF file
    pdf_buffer = io.BytesIO()

    # Write the decoded data to the PDF buffer
    pdf_buffer.write(decoded_data)

    # Reset the buffer position to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer

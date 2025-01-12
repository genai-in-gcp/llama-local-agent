import base64

from IPython.display import Image, display

def display_graph_image(graph):
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        pass
    
    
def encode_pdf_to_base64(pdf_path):
    """
    Reads a PDF file and encodes its content in Base64

    Args:
        pdf_path (str): The path to the PDF file to be encoded

    Returns:
        str: Base64-encoded string of the PDF content
    """
    try:
        with open(pdf_path, "rb") as file:
            base64_pdf = base64.b64encode(file.read()).decode("utf-8")
            return base64_pdf
    except FileNotFoundError:
        print(f"Error: The file at {pdf_path} was not found")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
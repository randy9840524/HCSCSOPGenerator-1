import socket
from app import app, logger

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return False
        except socket.error:
            return True

if __name__ == "__main__":
    logger.info("Starting HCSC Shared Services SOP Generator")
    port = 5000
    while is_port_in_use(port):
        logger.warning(f"Port {port} is in use, trying port {port + 1}")
        port += 1
    logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)

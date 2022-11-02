import logging
import uvicorn
from loader import app
import route

# original port 8080

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, filename="log.txt")
    uvicorn.run(app, port=1212)

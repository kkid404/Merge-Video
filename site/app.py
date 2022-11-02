from flask_cors import CORS

from loader import app

import route


CORS(app, supports_credentials=True)

if __name__ == "__main__":
    app.run(debug=False)  # Выключить debug на релизе

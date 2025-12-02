from pathlib import Path
from dotenv import load_dotenv
from flask import Flask

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from commands.polyrhythm_gen import polyrhythm_gen_bp
from commands.beat_gen import beat_gen_bp


app = Flask(__name__)
app.register_blueprint(polyrhythm_gen_bp)
app.register_blueprint(beat_gen_bp)


if __name__ == '__main__':
    app.run(debug=True)
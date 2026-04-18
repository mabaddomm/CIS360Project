print("run.py started")

from app import create_app
print("imported create_app")

app = create_app()
print("app created")

if __name__ == "__main__":
    print("starting server")
    app.run(host="0.0.0.0", port=5000, debug=True)
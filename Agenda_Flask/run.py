from app import crear_app

app, get_db = crear_app()

if __name__ == '__main__':
    app.run(debug=True)

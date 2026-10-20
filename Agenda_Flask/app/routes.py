from flask import render_template, request, redirect, url_for


def registrar_rutas(app, get_db):

    @app.route('/')
    def inicio():
        conn = get_db()
        actividades = conn.execute(
            'SELECT * FROM actividades ORDER BY fecha').fetchall()
        conn.close()
        return render_template('index.html', actividades=actividades)

    @app.route('/agregar', methods=['POST'])
    def agregar():
        titulo = request.form['titulo']
        desc = request.form['descripcion']
        fecha = request.form['fecha']
        conn = get_db()
        conn.execute(
            'INSERT INTO actividades (titulo, descripcion, fecha) VALUES (?,?,?)',
            (titulo, desc, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('inicio'))

    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        conn = get_db()
        if request.method == 'POST':
            titulo = request.form['titulo']
            desc = request.form['descripcion']
            fecha = request.form['fecha']
            completada = 1 if request.form.get('completada') else 0
            conn.execute(
                'UPDATE actividades SET titulo=?, descripcion=?, fecha=?, completada=? WHERE id=?',
                (titulo, desc, fecha, completada, id))
            conn.commit()
            conn.close()
            return redirect(url_for('inicio'))
        actividad = conn.execute(
            'SELECT * FROM actividades WHERE id=?', (id,)).fetchone()
        conn.close()
        if actividad is None:
            return redirect(url_for('inicio'))
        return render_template('editar.html', actividad=actividad)

    @app.route('/completar/<int:id>')
    def completar(id):
        conn = get_db()
        conn.execute(
            'UPDATE actividades SET completada = 1 - completada WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('inicio'))

    @app.route('/eliminar/<int:id>')
    def eliminar(id):
        conn = get_db()
        conn.execute('DELETE FROM actividades WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('inicio'))

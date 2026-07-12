from flask import Flask, render_template, g, redirect, url_for, session, request, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'ufr_sta_secret_2026'
DATABASE = 'database/ufr.db'

# ── Base de données ────────────────────────────────────────
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('database/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# ── Helper admin ───────────────────────────────────────────
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ══════════════════════════════════════════════════════════
# ROUTES PUBLIQUES
# ══════════════════════════════════════════════════════════

@app.route('/')
def index():
    db = get_db()
    actualites = db.execute('SELECT * FROM actualite ORDER BY date DESC LIMIT 3').fetchall()
    return render_template('index.html', actualites=actualites)

@app.route('/departements')
def departements():
    db = get_db()
    deps = db.execute('SELECT * FROM departement').fetchall()
    return render_template('departements.html', departements=deps)

@app.route('/formations')
def formations():
    db = get_db()
    formations = db.execute('SELECT * FROM formation').fetchall()
    return render_template('formations.html', formations=formations)

@app.route('/actualites')
def actualites():
    db = get_db()
    actu = db.execute('SELECT * FROM actualite ORDER BY date DESC').fetchall()
    return render_template('actualites.html', actualites=actu)

@app.route('/activites')
def activites():
    db = get_db()
    acts = db.execute('SELECT * FROM activite ORDER BY date DESC').fetchall()
    return render_template('activites.html', activites=acts)

@app.route('/galerie')
def galerie():
    db = get_db()
    albums = db.execute('SELECT * FROM album ORDER BY date DESC').fetchall()
    return render_template('galerie.html', albums=albums)

@app.route('/enseignants')
def enseignants():
    db = get_db()
    ens = db.execute('SELECT * FROM enseignant ORDER BY nom').fetchall()
    return render_template('enseignants.html', enseignants=ens)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom     = request.form.get('nom', '').strip()
        email   = request.form.get('email', '').strip()
        sujet   = request.form.get('sujet', '').strip()
        message = request.form.get('message', '').strip()
        if nom and email and sujet and message:
            db = get_db()
            db.execute(
                'INSERT INTO contact_message (nom, email, sujet, message) VALUES (?, ?, ?, ?)',
                (nom, email, sujet, message)
            )
            db.commit()
            flash('Votre message a bien été envoyé. Nous vous répondrons rapidement.', 'success')
        else:
            flash('Merci de remplir tous les champs obligatoires.', 'error')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# ══════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        db = get_db()
        user = db.execute(
            'SELECT * FROM admin WHERE username=? AND password=?',
            (request.form['username'], request.form['password'])
        ).fetchone()
        if user:
            session['admin'] = True
            flash('Connexion réussie.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Identifiants incorrects.', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    db = get_db()
    nb_actu  = db.execute('SELECT COUNT(*) FROM actualite').fetchone()[0]
    nb_act   = db.execute('SELECT COUNT(*) FROM activite').fetchone()[0]
    nb_album = db.execute('SELECT COUNT(*) FROM album').fetchone()[0]
    nb_msg   = db.execute('SELECT COUNT(*) FROM contact_message').fetchone()[0]
    nb_ens   = db.execute('SELECT COUNT(*) FROM enseignant').fetchone()[0]
    return render_template('admin/dashboard.html',
                           nb_actu=nb_actu, nb_act=nb_act,
                           nb_album=nb_album, nb_msg=nb_msg,
                           nb_ens=nb_ens)

# ── Actualités CRUD ────────────────────────────────────────
@app.route('/admin/actualites')
@login_required
def admin_actualites():
    db = get_db()
    actu = db.execute('SELECT * FROM actualite ORDER BY date DESC').fetchall()
    return render_template('admin/actualites.html', actualites=actu)

@app.route('/admin/actualites/ajouter', methods=['GET', 'POST'])
@login_required
def admin_ajouter_actualite():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            'INSERT INTO actualite (titre, date, description, photo) VALUES (?, ?, ?, ?)',
            (request.form['titre'], request.form['date'],
             request.form['description'], request.form.get('photo', ''))
        )
        db.commit()
        flash('Actualité ajoutée avec succès.', 'success')
        return redirect(url_for('admin_actualites'))
    return render_template('admin/form_actualite.html', actualite=None)

@app.route('/admin/actualites/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_modifier_actualite(id):
    db = get_db()
    if request.method == 'POST':
        db.execute(
            'UPDATE actualite SET titre=?, date=?, description=?, photo=? WHERE id=?',
            (request.form['titre'], request.form['date'],
             request.form['description'], request.form.get('photo', ''), id)
        )
        db.commit()
        flash('Actualité modifiée.', 'success')
        return redirect(url_for('admin_actualites'))
    actu = db.execute('SELECT * FROM actualite WHERE id=?', (id,)).fetchone()
    return render_template('admin/form_actualite.html', actualite=actu)

@app.route('/admin/actualites/supprimer/<int:id>', methods=['POST'])
@login_required
def admin_supprimer_actualite(id):
    db = get_db()
    db.execute('DELETE FROM actualite WHERE id=?', (id,))
    db.commit()
    flash('Actualité supprimée.', 'success')
    return redirect(url_for('admin_actualites'))

# ── Activités CRUD ─────────────────────────────────────────
@app.route('/admin/activites')
@login_required
def admin_activites():
    db = get_db()
    acts = db.execute('SELECT * FROM activite ORDER BY date DESC').fetchall()
    return render_template('admin/activites.html', activites=acts)

@app.route('/admin/activites/ajouter', methods=['GET', 'POST'])
@login_required
def admin_ajouter_activite():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            'INSERT INTO activite (titre, date, lieu, organisateur, description) VALUES (?, ?, ?, ?, ?)',
            (request.form['titre'], request.form['date'], request.form.get('lieu', ''),
             request.form.get('organisateur', ''), request.form['description'])
        )
        db.commit()
        flash('Activité ajoutée.', 'success')
        return redirect(url_for('admin_activites'))
    return render_template('admin/form_activite.html', activite=None)

@app.route('/admin/activites/supprimer/<int:id>', methods=['POST'])
@login_required
def admin_supprimer_activite(id):
    db = get_db()
    db.execute('DELETE FROM activite WHERE id=?', (id,))
    db.commit()
    flash('Activité supprimée.', 'success')
    return redirect(url_for('admin_activites'))

# ── Galerie ────────────────────────────────────────────────
@app.route('/admin/galerie')
@login_required
def admin_galerie():
    db = get_db()
    albums = db.execute('SELECT * FROM album ORDER BY date DESC').fetchall()
    return render_template('admin/galerie.html', albums=albums)

@app.route('/admin/galerie/ajouter', methods=['GET', 'POST'])
@login_required
def admin_ajouter_album():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            'INSERT INTO album (titre, description, date) VALUES (?, ?, ?)',
            (request.form['titre'], request.form.get('description', ''), request.form['date'])
        )
        db.commit()
        flash('Album ajouté avec succès.', 'success')
        return redirect(url_for('admin_galerie'))
    return render_template('admin/form_album.html')

@app.route('/admin/galerie/supprimer/<int:id>', methods=['POST'])
@login_required
def admin_supprimer_album(id):
    db = get_db()
    db.execute('DELETE FROM photo WHERE album_id=?', (id,))
    db.execute('DELETE FROM album WHERE id=?', (id,))
    db.commit()
    flash('Album supprimé.', 'success')
    return redirect(url_for('admin_galerie'))

# ── Formations ─────────────────────────────────────────────
@app.route('/admin/formations')
@login_required
def admin_formations():
    db = get_db()
    formations = db.execute('SELECT f.*, d.nom as dept_nom FROM formation f LEFT JOIN departement d ON f.departement_id = d.id').fetchall()
    return render_template('admin/formations.html', formations=formations)

@app.route('/admin/formations/ajouter', methods=['GET', 'POST'])
@login_required
def admin_ajouter_formation():
    db = get_db()
    if request.method == 'POST':
        db.execute(
            'INSERT INTO formation (nom, niveau, duree, conditions, debouches, departement_id) VALUES (?, ?, ?, ?, ?, ?)',
            (request.form['nom'], request.form['niveau'], request.form['duree'],
             request.form.get('conditions', ''), request.form.get('debouches', ''),
             request.form.get('departement_id') or None)
        )
        db.commit()
        flash('Formation ajoutée.', 'success')
        return redirect(url_for('admin_formations'))
    deps = db.execute('SELECT * FROM departement').fetchall()
    return render_template('admin/form_formation.html', formation=None, departements=deps)

@app.route('/admin/formations/supprimer/<int:id>', methods=['POST'])
@login_required
def admin_supprimer_formation(id):
    db = get_db()
    db.execute('DELETE FROM formation WHERE id=?', (id,))
    db.commit()
    flash('Formation supprimée.', 'success')
    return redirect(url_for('admin_formations'))

# ── Messages ───────────────────────────────────────────────
@app.route('/admin/messages')
@login_required
def admin_messages():
    db = get_db()
    messages = db.execute('SELECT * FROM contact_message ORDER BY date_envoi DESC').fetchall()
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/messages/supprimer/<int:id>', methods=['POST'])
@login_required
def admin_supprimer_message(id):
    db = get_db()
    db.execute('DELETE FROM contact_message WHERE id=?', (id,))
    db.commit()
    flash('Message supprimé.', 'success')
    return redirect(url_for('admin_messages'))


# ── Enseignants CRUD ───────────────────────────────────────
@app.route('/admin/enseignants')
@login_required
def admin_enseignants():
    db = get_db()
    ens = db.execute('SELECT * FROM enseignant ORDER BY nom').fetchall()
    return render_template('admin/enseignants.html', enseignants=ens)

@app.route('/admin/enseignants/ajouter', methods=['GET', 'POST'])
@login_required
def admin_ajouter_enseignant():
    db = get_db()
    if request.method == 'POST':
        db.execute(
            'INSERT INTO enseignant (nom, grade, departement_id, email, recherche, photo) VALUES (?, ?, ?, ?, ?, ?)',
            (request.form['nom'], request.form['grade'],
             request.form.get('departement_id') or None,
             request.form.get('email', ''), request.form.get('recherche', ''),
             request.form.get('photo', ''))
        )
        db.commit()
        flash('Enseignant ajouté avec succès.', 'success')
        return redirect(url_for('admin_enseignants'))
    deps = db.execute('SELECT * FROM departement').fetchall()
    return render_template('admin/form_enseignant.html', enseignant=None, departements=deps)

@app.route('/admin/enseignants/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_modifier_enseignant(id):
    db = get_db()
    if request.method == 'POST':
        db.execute(
            'UPDATE enseignant SET nom=?, grade=?, departement_id=?, email=?, recherche=?, photo=? WHERE id=?',
            (request.form['nom'], request.form['grade'],
             request.form.get('departement_id') or None,
             request.form.get('email', ''), request.form.get('recherche', ''),
             request.form.get('photo', ''), id)
        )
        db.commit()
        flash('Enseignant modifié.', 'success')
        return redirect(url_for('admin_enseignants'))
    ens = db.execute('SELECT * FROM enseignant WHERE id=?', (id,)).fetchone()
    deps = db.execute('SELECT * FROM departement').fetchall()
    return render_template('admin/form_enseignant.html', enseignant=ens, departements=deps)

@app.route('/admin/enseignants/supprimer/<int:id>', methods=['POST'])
@login_required
def admin_supprimer_enseignant(id):
    db = get_db()
    db.execute('DELETE FROM enseignant WHERE id=?', (id,))
    db.commit()
    flash('Enseignant supprimé.', 'success')
    return redirect(url_for('admin_enseignants'))

if __name__ == '__main__':
    if not os.path.exists('database/ufr.db'):
        os.makedirs('database', exist_ok=True)
        init_db()
    app.run(debug=True)

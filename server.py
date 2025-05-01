from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "cle_secrete_pour_sessions"

# Chargement des mots depuis un fichier
def charger_mots():
    with open("dictionnaire.txt", "r", encoding="utf-8") as f:
        return [ligne.strip().split(";")[0].lower() for ligne in f if ligne.strip()]

MOTS = charger_mots()
ALPHABET = list("abcdefghijklmnopqrstuvwxyz")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "POST":
        nom = request.form["nom"]
        mot = random.choice(MOTS)

        # Initialisation de la session
        session["nom"] = nom
        session["mot"] = mot
        session["lettres_trouvees"] = []
        session["vies"] = 5

        return redirect(url_for("play"))  # Redirige vers GET pour afficher l'interface

    nom = session.get("nom")
    mot = session.get("mot")
    lettres_trouvees = session.get("lettres_trouvees", [])
    vies = session.get("vies", 5)

    lettre = request.args.get("lettre")
    if lettre and lettre not in lettres_trouvees:
        lettres_trouvees.append(lettre)
        if lettre not in mot:
            vies -= 1
        session["lettres_trouvees"] = lettres_trouvees
        session["vies"] = vies

    mot_affiche = " ".join([l if l in lettres_trouvees else "_" for l in mot])
    fini = "_" not in mot_affiche
    perdu = vies <= 0

    return render_template("play.html",
                           nom=nom,
                           mot_affiche=mot_affiche,
                           vies=vies,
                           alphabet=ALPHABET,
                           lettres_trouvees=lettres_trouvees,
                           mot=mot if (fini or perdu) else None,
                           fini=fini,
                           perdu=perdu)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))

from audioop import reverse
from flask import Blueprint, render_template, request, url_for, redirect
from .forms import DarkysForm
from .models import Darckysources, Phishing
from .func import typer, net
from datetime import datetime
from .darky import DarkyToreq, PhishingUpdate, PhishScan
views = Blueprint("views", __name__)

@views.get("/")
def index():

    all_darkys = Darckysources.objects()
    return render_template("index.html", title="Darkeys", darkeys=all_darkys, date=datetime.now())

@views.route("/darkymonitor/", methods=["POST", "GET"])
def darkymonitor():

    form = DarkysForm(request.form)
    all_darky = Darckysources.objects()
    if request.method == "POST":
    
        if form.validate():

            darky = Darckysources(name=form.name.data,
                                  type=typer(form.type.data),
                                  network=net(form.network.data), 
                                  onion=form.onion.data)
            darky.save()
            track = DarkyToreq(
                url=darky.onion,
                network=darky.network
            )
            track.start()
            print(darky)

        return redirect(url_for("views.darkymonitor"))
    return render_template("add.html", title="Add Darky", darkys=all_darky)

@views.get("/phishing/<int:page>")
def phishing(page):
    items_per_page = 15
    offset = (page -1) * items_per_page
    all_phish = list(Phishing.objects())[::-1][offset: page*items_per_page]

    return render_template("phish.html", urls=all_phish)

@views.get("/del/<item>/<id>/")
def del_darky(item, id):
    if item == "darky":
        darky = Darckysources.objects(id=id).first()
        darky.delete()
        return redirect(url_for("views.darkymonitor"))
    if item == "phishing":
        phishing = Phishing.objects(id=id).first()
        phishing.delete()
        return redirect(url_for("views.phishing", page=1))


@views.post("/isphish/")
def isphish():

    methode = request.form.get("methode")
    stdin   = request.form.get("stdin")
    if stdin:
        if methode == "url":
            scan = PhishScan(methode, stdin)
        
        elif methode == "word":
            scan = PhishScan(methode, stdin)
        
        elif methode == "cuntry":
            scan = PhishScan(methode, stdin)
    else:
        scan = []
    
    print(stdin)
    return render_template("phishmonitor.html",
                            phishings=scan)    

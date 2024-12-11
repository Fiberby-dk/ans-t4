import pprint
from urllib.parse import urlparse, parse_qs
from flask import Flask, render_template, url_for, request
import swapi

app = Flask(__name__)

api = swapi.Swapi()


@app.route("/")
def root():
    return render_template("root.html")


@app.route("/people_list")
def people_list():
    req_qs = parse_qs(request.query_string.decode("utf-8"))
    page = int(req_qs["page"][0]) if "page" in req_qs else None
    resp = api.get(swapi.People, page=page)
    pprint.pprint(resp)
    page_next = [None, None]
    pprint.pprint(resp.next)
    if resp.next is not None:
        urlp = urlparse(resp.next)
        qs = parse_qs(urlp.query)
        pprint.pprint(qs)
        if "page" in qs:
            page_next[0] = url_for("root", page=qs["page"][0])
            page_next[1] = f"Page: {qs['page'][0]}"
    page_previous = [None, None]
    if resp.previous is not None:
        urlp = urlparse(resp.previous)
        qs = parse_qs(urlp.query)
        if "page" in qs:
            page_previous[0] = url_for("root", page=qs["page"][0])
            page_previous[1] = f"Page: {qs['page'][0]}"

    return render_template(
        "people_list.html",
        peoples=resp,
        next=page_next,
        previous=page_previous,
    )


@app.route("/people/<int:people_id>")
def people(people_id):
    return render_template(
        "people.html", people=api.get(swapi.People, obj_id=people_id)
    )


@app.route("/film_list")
def film_list():
    req_qs = parse_qs(request.query_string.decode("utf-8"))
    page = int(req_qs["page"][0]) if "page" in req_qs else None
    resp = api.get(swapi.Film, page=page)

    pprint.pprint(resp)
    page_next = [None, None]
    pprint.pprint(resp.next)
    if resp.next is not None:
        urlp = urlparse(resp.next)
        qs = parse_qs(urlp.query)
        pprint.pprint(qs)
        if "page" in qs:
            page_next[0] = url_for("root", page=qs["page"][0])
            page_next[1] = f"Page: {qs['page'][0]}"
    page_previous = [None, None]
    if resp.previous is not None:
        urlp = urlparse(resp.previous)
        qs = parse_qs(urlp.query)
        if "page" in qs:
            page_previous[0] = url_for("root", page=qs["page"][0])
            page_previous[1] = f"Page: {qs['page'][0]}"
    return render_template(
        "film_list.html",
        films=resp,
        next=page_next,
        previous=page_previous,
    )


@app.route("/films/<int:film_id>")
def film(film_id):
    film = api.get(swapi.Film, obj_id=film_id)
    film.get_people()
    return render_template("film.html", film=film)

#!/usr/bin/env python
# coding: utf-8

import json
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, render_template, request, url_for

load_dotenv()

# set token value in order to validate posts
SECRET = os.getenv("TOKEN")
QUEUE_PATH = os.getenv("QUEUE_PATH", "cache/queue.json")
# Load JSON message store if available
# (saved to a disk volume, preserves status across restarts)
try:
    QUEUE = json.load(open(QUEUE_PATH, "r"))
except (ValueError, FileNotFoundError):
    QUEUE = {}

# Instantiate app
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"], defaults={"handle": None})
@app.route("/<handle>", methods=["GET", "POST", "DELETE"])
def api_endpoint(handle):
    if request.method == "POST":
        args = request.get_json()
        if not handle:
            handle = args["handle"]
        status = args["status"]
        token = args["token"]
        color = args["color"]
        stamp = str(datetime.now())
        if (token == SECRET) or (SECRET is None):  # check that token is valid
            content = {
                "link": url_for("api_endpoint", handle=handle),
                "handle": handle,
                "status": status,
                "color": color,
                "at": stamp,
                "client_ip": request.remote_addr,
            }
            QUEUE[handle] = content
            with open(QUEUE_PATH, "w") as fh:
                json.dump(QUEUE, fh)
            return jsonify(QUEUE[handle]), 201
        else:
            return "invalid token", 403

    if request.method == "GET":
        if not handle:
            lst = [item for item in QUEUE.values()]
            return jsonify(lst)
        try:
            return jsonify(QUEUE[handle]), 201
        except KeyError:
            no_status = {"handle": handle, "status": "No such handle"}
            return jsonify(no_status), 404

    if request.method == "DELETE":
        QUEUE.pop(handle, None)
        with open(QUEUE_PATH, "w") as fh:
            json.dump(QUEUE, fh)
        return jsonify({handle: "Deleted"}), 204


# Little web UI
# Log monitor page
@app.route("/view")
def index():
    stamp = str(datetime.now())
    freight = render_template("statuslist.html", queue=QUEUE, dt=stamp)
    v = make_response(freight)
    return v


# view only one handle status
@app.route("/view/n/<handle>")
def nick_view(handle):
    stamp = str(datetime.now())
    handle_queue = {}
    handle_queue[handle] = QUEUE[handle]
    freight = render_template(
        "filtered_status.html", queue=handle_queue, dt=stamp, handle=handle
    )
    v = make_response(freight)
    return v


# view only one color status
@app.route("/view/c/<color>")
def color_view(color):
    stamp = str(datetime.now())
    color_queue = {}
    for alias, content in QUEUE.items():
        if color in content["color"]:
            color_queue[alias] = content
    freight = render_template(
        "filtered_status.html", queue=color_queue, dt=stamp, handle=color
    )
    v = make_response(freight)
    return v


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

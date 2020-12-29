# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
from webapp import create_app

app = create_app()


@app.route('/')
def hello_world():
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)

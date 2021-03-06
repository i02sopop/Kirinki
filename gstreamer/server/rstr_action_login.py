#!/usr/bin/env python
# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

import web

render = web.ctx.session['render']
usr = web.ctx.session['usr']

class Login:
    def GET(self):
        blocks = [render.login(usr.loginForm())]
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "static/javascript.js")
    def POST(self):
        if not usr.loginForm().validates(): 
            blocks = [render.login(usr.lForm)]
        else:
            if not usr.login(usr.lForm['username'].value, usr.lForm['password'].value):
                blocks = ["Error. Usuario o contrasena incorrectos", render.login(usr.lForm)]
            else:
                blocks = [render.article("Title","abstract","content")]
        #blocks.append(render.section(render.article("Title","abstract","content")))
        left = render.left(blocks)
        center = render.center()
        right = render.right()
        return render.index(left, center, right, "Ritho's streaming", "static/style.css", "static/jquery.js", "static/javascript.js")

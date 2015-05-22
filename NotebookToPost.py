""" Script to convert a ipynb notebook to a Jekyll blog post """

import sys
import subprocess

ipynb_fn = sys.argv[1]
print "Converting {}".format(ipynb_fn)

ipynb_content = subprocess.check_output(
    "ipython nbconvert --to html --stdout {}".format(ipynb_fn), shell=True)

html_fn = ipynb_fn.strip("ipynb")+"html"
html_fn = html_fn.replace("notebooks", "posts")

post_title = ipynb_fn.split("/")[1].replace(".ipynb", "").replace("-", " ")
post_title = ''.join([i for i in post_title if not i.isdigit()])
post_title = post_title.lstrip()

html = open(html_fn, "w+")
html.write("""---
type: post
title: {}
---

""".format(post_title))

html.write(ipynb_content)



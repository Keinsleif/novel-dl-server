#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, render_template, url_for, make_response, flash, send_file, redirect
import tempfile
from http import HTTPStatus
import os,shutil,zipfile,time,json
import novel_dl
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

tmp_dir=tempfile.TemporaryDirectory()
root=os.path.dirname(os.path.abspath(__file__))+"/"

executor=ThreadPoolExecutor(max_workers=2, thread_name_prefix="th")
proc={}

def make_novel_pkg(args):
	try:
		result=novel_dl.main(args)
	except novel_dl.NovelDLException as e:
		print(e.return_message())
		return {"success":False,"result":e.return_message()}
	ncode=result[2]
	nc=[ncode,args["theme"],args["media"]]
	[nc.remove("") for i in range(0,nc.count(""))]
	if result[0]==1:
		filename=root+"static/files/"+"-".join(nc)+"-single.zip"
	else:
		filename=root+"static/files/"+"-".join(nc)+"-multi.zip"
	if os.path.isfile(filename):
		return {"success":True,"result":os.path.basename(filename)}
	if result[0]==1:
		with zipfile.ZipFile(filename,"w",compression=zipfile.ZIP_DEFLATED) as new_zip:
			new_zip.write(result[1],arcname=os.path.basename(result[1]))
	else:
		shutil.make_archive(os.path.splitext(filename)[0],'zip',root_dir=result[1])
	return {"success":True,"result":os.path.basename(filename)}

def prepare_response(response):
	di=dir(response)
	if 'set_cookie' not in di:
		response=make_response(response)
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
#	response.headers['Content-Security-Policy'] = 'default-src \'self\' wss:;'
#	response.headers['Content-Security-Policy'] = 'script-src mypcnotes.mydns.jp \'nonce-vYVbljBJeUY/GB+OZXSmzCN6yKw\' \'nonce-t3vbtCpFUM4Id5mqM1HVPuCKRmE\''
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	return response

def show_home():
	files=os.listdir(root+"static/files/")
	novelpks=[]
	for file in files:
		if os.path.splitext(file)[1]==".zip":
			novelpks.append(file)
	return render_template("home.html",title="メインページ",themes=novel_dl.THEMES,files=novelpks)

def do_add_download():
	args=novel_dl.args()
	dirname=tmp_dir.name+"/{ncode}/"
	args["url"]=request.form.get("url")
	if request.form.get("theme"):
		args["theme"]=request.form.get("theme")
		dirname=dirname+args["theme"]
	else:
		dirname=dirname+"-auto"
	if request.form.get("media"):
		args["media"]=request.form.get("media")
		dirname=dirname+"-"+args["media"]
	if request.form.get("renew"):
		args["renew"]=eval(request.form.get("renew"))
	if request.form.get("axel"):
		args["axel"]=eval(request.form.get("axel"))
	if request.form.get("episode"):
		args["episode"]=request.form.get("episode")
		dirname=dirname+"-"+args["episode"]
		if request.form.get("short"):
			args["short"]=eval(request.form.get("short"))
			dirname=dirname+"s"
	args["dir"]=dirname
	pid=len(proc)
	proc[pid]=executor.submit(make_novel_pkg,args)
	return str(pid)

def do_download_proc(pid):
	if proc.get(pid):
		if proc[pid].done():
			return json.dumps(proc[pid].result())
	time.sleep(5)
	return "Never"

def do_del_cache(file):
	files=os.listdir(os.path.join(root,"static/files"))
	if file in files:
		os.remove(os.path.join(root,"static/files",file))
	return redirect(url_for('index'))

def do_return_themes():
	return " ".join(novel_dl.THEMES)

def after_request(response):
	return  prepare_response(response)

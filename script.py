from js import document, window, navigator
from pyodide.ffi import create_proxy
import math

def encode(text,key,chars):
  if chars == chars.lower():
    text = text.lower()
  elif chars == chars.upper():
    text = text.upper()
  if not key:
    return text
  encoded = ""
  key = key.lower()
  old_key = key
  j = 0
  for i in range(math.ceil(len(text)/len(key))):
    key += old_key
  for i in range(len(text)):
    if text[i] in chars:
      encoded += chars[(chars.index(text[i])+chars.index(key[j]))%len(chars)]
      j+=1
    else:
      encoded += text[i]
  return encoded
def decode(text,key,chars):
  if chars == chars.lower():
    text = text.lower()
  elif chars == chars.upper():
    text = text.upper()
  if not key:
    return text
  decoded = ""
  key = key.lower()
  old_key = key
  j = 0
  for i in range(math.ceil(len(text)/len(key))):
    key += old_key
  for i in range(len(text)):
    if text[i] in chars:
      decoded += chars[(chars.index(text[i])-chars.index(key[j]))%len(chars)]
      j+=1
    else:
      decoded += text[i]
  return decoded

def details():
   if document.querySelector('p').innerHTML:
      document.querySelector('p').innerHTML = "The vigenere cipher is a cipher where each letter of the input will be encoded by a different caesar cipher with the offset of the letter with the same index in the key"
   else:
      document.querySelector('p').innerHTML = ""
def copy_encode(event):
    text = document.getElementById("encode").innerText
    navigator.clipboard.writeText(text)
def copy_decode(event):
    text = document.getElementById("decode").innerText
    navigator.clipboard.writeText(text)
document.getElementById("copy-encode").onclick = copy_encode
document.getElementById("copy-decode").onclick = copy_decode

def collect_encode(event=None):
    form = document.getElementById("formencode")
    if not form:
        return
    data = {el.name: el.value for el in form.elements if el.name}
    out = encode(
        data.get("input", ""),
        data.get("key", ""),
        data.get("charset", "abcdefghijklmnopqrstuvwxyz")
    )
    document.querySelector("#encode").innerHTML = out if out else "no input"
def collect_decode(event=None):
    form = document.getElementById("formdecode")
    if not form:
        return
    data = {el.name: el.value for el in form.elements if el.name}
    out = decode(
        data.get("input", ""),
        data.get("key", ""),
        data.get("charset", "abcdefghijklmnopqrstuvwxyz")
    )
    document.querySelector("#decode").innerHTML = out if out else "no input"

def attach_listeners():
    encode_form = document.getElementById("formencode")
    decode_form = document.getElementById("formdecode")

    if encode_form is None or decode_form is None:
        window.setTimeout(attach_listeners, 100)
        return

    global encode_proxy, decode_proxy
    encode_proxy = create_proxy(collect_encode)
    decode_proxy = create_proxy(collect_decode)
    encode_form.addEventListener("input", encode_proxy)
    decode_form.addEventListener("input", decode_proxy)
    collect_encode()
    collect_decode()

attach_listeners()

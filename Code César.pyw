import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from codecs import open
from winsound import PlaySound, SND_ALIAS, SND_ASYNC
import os

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r" ,"s", "t", "u", "v", "w", "x", "y", "z"]
chiffres = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}

class CodeCesar(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.title("Code César - indyteo")
		self.tk.call("wm", "iconphoto", self._w, tk.PhotoImage(file = "./icone.gif"))
		self.resizable(False, False)
		self.grid()
		
		self.choix_action = tk.StringVar()
		self.choix_action.set("Crypter")
		self.liste_actions = ttk.Combobox(self, textvariable = self.choix_action, values = ["Crypter", "Décrypter"], font = "Arial 15", height = 2)
		self.liste_actions.state(["!disabled", "readonly"])
		self.liste_actions.grid(row = 0, column = 0, columnspan = 3, sticky = "NSEW")
		
		self.texte = tk.Text(self, font = "Arial 12", height = 5, width = 50)
		self.texte.grid(row = 1, column = 0, sticky = "NSEW")
		self.texte.insert(tk.END, "Entrez votre texte ici...")
		self.texte.tag_add(tk.SEL, "1.0", tk.END)
		self.texte.focus_set()
		
		self.disp = tk.Button(self, text = "==>", font = "Arial 18", command = self.crypter)
		self.disp.grid(row = 1, column = 1, sticky = "NSEW")
		
		self.cle = tk.StringVar()
		self.cle.set("0")
		self.demander_cle = tk.Entry(self, textvariable = self.cle, font = "Arial 15", validate = "all", validatecommand = (self.register(self.verifierCle), "%s", "%P"), width = 5)
		self.demander_cle.grid(row = 2, column = 1, sticky = "NSEW")
		
		self.phrase_cryptee = tk.StringVar()
		self_texte_crypte = tk.LabelFrame(self, text = "Texte crypté")
		self_texte_crypte.grid(row = 1, column = 2, sticky = "NSEW")
		self.texte_crypte = tk.Label(self_texte_crypte, textvariable = self.phrase_cryptee, font = "Arial 12")
		self.texte_crypte.grid(sticky = "NSEW")
		
		self.ou1 = tk.Label(self, text = "OU", font = "Arial 15")
		self.ou1.grid(row = 2, column = 0, sticky = "NSEW")
		self.ou2 = tk.Label(self, text = "OU", font = "Arial 15")
		self.ou2.grid(row = 2, column = 2, sticky = "NSEW")
		
		self.charger_fichier = tk.Button(self, text = "Importer depuis un fichier texte", font = "Arial 12", fg = "blue", bg = "#1496f3", command = self.chargerFichier)
		self.charger_fichier.grid(row = 3, column = 0, sticky = "NSEW")
		
		self.enregistrer_fichier = tk.Button(self, text = "Enregistrer dans un fichier texte", font = "Arial 12", fg = "green", bg = "#c8f0c5", command = self.enregistrerFichier)
		self.enregistrer_fichier.grid(row = 3, column = 2, sticky = "NSEW")
	
	def crypter(self):
		texte = self.simplifier(self.texte.get("1.0", tk.END))
		if self.choix_action.get() == "Crypter":
			cle = int(self.cle.get())
		else:
			cle = - int(self.cle.get())
		self.phrase_cryptee.set("")
		for lettre in texte:
			if lettre.lower().isalpha() and lettre != "":
				if lettre in [maj.upper() for maj in alphabet]:
					caractere = alphabet[(chiffres[lettre.lower()] + cle) % 26].upper()
				else:
					caractere = alphabet[(chiffres[lettre] + cle) % 26]
			else:
				caractere = lettre
			self.phrase_cryptee.set(self.phrase_cryptee.get() + caractere)

	def simplifier(self, texte):
		accents = {"é": "e", "è": "e", "ê": "e", "ë": "e", "à": "a", "â": "a", "î": "i", "ï": "i", "ô": "o", "ö": "o", "ù": "u", "û": "u", "ü": "u", "ç": "c", "œ": "oe"}
		texte = [char for char in list(texte) if char != "\r"]
		for i in range(len(texte)):
			lettre = texte[i]
			if lettre.lower() in accents.keys():
				if lettre in [maj.upper() for maj in accents.keys()]:
					texte[i] = accents[lettre.lower()].upper()
				else:
					texte[i] = accents[lettre.lower()]
		return "".join(texte)
	
	def verifierCle(self, old, new):
		if new.isdigit() or new == "":
			return True
		else:
			self.cle.set(old)
			PlaySound("SystemExit", SND_ALIAS | SND_ASYNC)
			return False
	
	def chargerFichier(self):
		self.file = askopenfilename(initialdir = ".", title = "Choisissez un document texte", defaultextension = ".txt", filetypes = [("Document texte", "*.txt")])
		if self.file != "":
			self.texte.delete("1.0", tk.END)
			with open(self.file, "r", "utf-8") as contenu:
				self.texte.insert(tk.END, contenu.read())
	
	def enregistrerFichier(self):
		if self.phrase_cryptee.get() == "":
			PlaySound("SystemExit", SND_ALIAS | SND_ASYNC)
		else:
			try:
				nom = self.file.split("/")[-1][0:-4]
			except AttributeError:
				nom = "Texte"
			if self.choix_action.get() == "Crypter":
				nom += " crypté " + self.cle.get()
			else:
				nom += " décrypté"
			self.file = asksaveasfilename(initialdir = ".", title = "Enregistrer un document texte", defaultextension = ".txt", initialfile = nom, filetypes = [("Document texte", "*.txt")])
			if self.file != "":
				open(self.file, "w", "utf-8").write(self.phrase_cryptee.get()[0:len(self.phrase_cryptee.get()) - 1])

CodeCesar = CodeCesar()
CodeCesar.mainloop()
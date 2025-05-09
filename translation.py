import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
import pyttsx3
from googletrans import Translator, LANGUAGES

# Initialisation de la voix
engine = pyttsx3.init()

# Fonction de reconnaissance vocale
def ecouter_micro():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Microphone", "Parlez maintenant...")
        try:
            audio = recognizer.listen(source, timeout=5)
            texte = recognizer.recognize_google(audio, language='fr-FR')
            texte_source.delete(1.0, "end")
            texte_source.insert(tk.END, texte)
        except Exception as e:
            messagebox.showerror("Erreur", "Je n'ai pas compris, réessayez.")

# Fonction de traduction
def traduire():
    texte = texte_source.get(1.0, "end-1c")
    src_lang = combobox_source.get()
    dest_lang = combobox_dest.get()

    if not texte.strip():
        messagebox.showwarning("Attention", "Le champ texte est vide.")
        return

    try:
        src_code = get_lang_code(src_lang)
        dest_code = get_lang_code(dest_lang)
        translator = Translator()
        traduction = translator.translate(texte, src=src_code, dest=dest_code)
        texte_dest.delete(1.0, "end")
        texte_dest.insert(tk.END, traduction.text)
    except Exception as e:
        messagebox.showerror("Erreur", "La traduction a échoué.")

# Fonction pour lire le texte traduit
def lire_texte():
    texte = texte_dest.get(1.0, "end-1c")
    if texte.strip():
        engine.say(texte)
        engine.runAndWait()

# Convertir la langue en code ISO
def get_lang_code(nom):
    for code, langue in LANGUAGES.items():
        if langue.lower() == nom.lower():
            return code
    return "en"

# Fenêtre principale
root = tk.Tk()
root.title("Traducteur vocal intelligent 🌍")
root.geometry("700x500")
root.config(bg="#f0f0f0")

# Styles
style_font = ("Arial", 14)

# Titre
titre = tk.Label(root, text="🗣️ Traducteur Multilingue avec Voix", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#007acc")
titre.pack(pady=10)

# Zone de texte source
texte_source = tk.Text(root, height=5, width=60, font=style_font)
texte_source.pack(pady=10)

# Bouton micro
btn_micro = tk.Button(root, text="🎤 Parler", command=ecouter_micro, font=style_font, bg="#007acc", fg="white")
btn_micro.pack()

# Sélecteurs de langue
frame_langues = tk.Frame(root, bg="#f0f0f0")
frame_langues.pack(pady=10)

langues = list(LANGUAGES.values())

combobox_source = ttk.Combobox(frame_langues, values=langues, width=25)
combobox_source.set("french")
combobox_source.grid(row=0, column=0, padx=10)

btn_traduire = tk.Button(frame_langues, text="🔁 Traduire", command=traduire, font=style_font, bg="#28a745", fg="white")
btn_traduire.grid(row=0, column=1, padx=10)

combobox_dest = ttk.Combobox(frame_langues, values=langues, width=25)
combobox_dest.set("english")
combobox_dest.grid(row=0, column=2, padx=10)

# Zone de texte traduite
texte_dest = tk.Text(root, height=5, width=60, font=style_font, bg="#e6ffe6")
texte_dest.pack(pady=10)

# Bouton pour lire le texte
btn_lecture = tk.Button(root, text="🔊 Écouter la traduction", command=lire_texte, font=style_font, bg="#17a2b8", fg="white")
btn_lecture.pack(pady=10)

# Lancer l'application
root.mainloop()

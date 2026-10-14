import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox

# Caminho para o executável do teu jogo (altera conforme o nome/caminho real)
GAME_EXECUTABLE_PATH = "caminho/para/o/teu_jogo.exe"


class GameLauncher:

  def __init__(self, root):
    self.root = root
    self.root.title("Portal do Jogo - Launcher PAP")
    self.root.geometry("450x300")
    self.root.resizable(False, False)
    self.root.configure(bg="#1e1e2e")

    # Título do Launcher
    self.title_label = tk.Label(
        self.root,
        text="Aventura 2D: RPG & Sandbox",
        font=("Helvetica", 16, "bold"),
        fg="#cdd6f4",
        bg="#1e1e2e",
    )
    self.title_label.pack(pady=20)

    # Subtítulo / Descrição
    self.subtitle_label = tk.Label(
        self.root,
        text="Explora, Constrói e Combate por Turnos",
        font=("Helvetica", 10, "italic"),
        fg="#a6adc8",
        bg="#1e1e2e",
    )
    self.subtitle_label.pack(pady=5)

    # Indicador de Estado
    self.status_label = tk.Label(
        self.root,
        text="Estado: Pronto para Jogar",
        font=("Helvetica", 10),
        fg="#a6e3a1",
        bg="#1e1e2e",
    )
    self.status_label.pack(pady=15)

    # Botão para Iniciar
    self.play_button = tk.Button(
        self.root,
        text="INICIAR JOGO",
        font=("Helvetica", 12, "bold"),
        bg="#89b4fa",
        fg="#11111b",
        activebackground="#b4befe",
        activeforeground="#11111b",
        padx=20,
        pady=10,
        bd=0,
        cursor="hand2",
        command=self.launch_game,
    )
    self.play_button.pack(pady=10)

  def launch_game(self):
    if not os.path.exists(GAME_EXECUTABLE_PATH):
      messagebox.showerror(
          "Erro de Execução",
          f"Não foi possível encontrar o executável do jogo em:\n{GAME_EXECUTABLE_PATH}\n\nVerifica o caminho no ficheiro do launcher.",
      )
      return

    self.status_label.config(
        text="Estado: Jogo em Execução...", fg="#f9e2af"
    )
    self.play_button.config(state=tk.DISABLED)

    # Executa o jogo numa thread separada para não encravar o launcher
    threading.Thread(target=self._run_process, daemon=True).start()

  def _run_process(self):
    try:
      process = subprocess.Popen([GAME_EXECUTABLE_PATH])
      process.wait()
    except Exception as e:
      messagebox.showerror("Erro", f"Ocorreu um erro ao abrir o jogo: {e}")
    finally:
      self.root.after(0, self._reset_launcher)

  def _reset_launcher(self):
    self.status_label.config(text="Estado: Pronto para Jogar", fg="#a6e3a1")
    self.play_button.config(state=tk.NORMAL)


if __name__ == "__main__":
  root = tk.Tk()
  app = GameLauncher(root)
  root.mainloop()
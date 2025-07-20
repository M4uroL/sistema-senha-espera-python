import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os


class SistemasenhaEspera:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Senhas de Espera")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Dados das senhas
        self.senhas_arquivo = "senhas_dados.json"
        self.senhas_data = self.carregar_dados()

        # Variáveis de controle
        self.proxima_senha = tk.StringVar()
        self.total_senhas = tk.IntVar()
        self.senhas_chamadas = tk.IntVar()
        self.senhas_pendentes = tk.IntVar()

        self.criar_interface()
        self.atualizar_contador()

    def carregar_dados(self):
        """Carrega dados salvos ou cria estrutura inicial"""
        if os.path.exists(self.senhas_arquivo):
            try:
                with open(self.senhas_arquivo, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            'contador': 0,
            'senhas_geradas': [],
            'senhas_chamadas': [],
            'data_atual': datetime.now().strftime("%Y-%m-%d")
        }

    def salvar_dados(self):
        """Salva dados no arquivo"""
        try:
            with open(self.senhas_arquivo, 'w') as f:
                json.dump(self.senhas_data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")

    def verificar_nova_data(self):
        """Verifica se é um novo dia e reseta o contador"""
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        if self.senhas_data['data_atual'] != data_hoje:
            self.senhas_data['contador'] = 0
            self.senhas_data['senhas_geradas'] = []
            self.senhas_data['senhas_chamadas'] = []
            self.senhas_data['data_atual'] = data_hoje
            self.salvar_dados()

    def criar_interface(self):
        """Cria a interface principal"""
        # Título principal
        titulo = tk.Label(
            self.root,
            text="Sistema de Senhas de Espera",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        titulo.pack(pady=20)

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20)

        # Seção de geração de senha
        self.criar_secao_gerar(main_frame)

        # Seção de chamar senha
        self.criar_secao_chamar(main_frame)

        # Seção de estatísticas
        self.criar_secao_estatisticas(main_frame)

        # Seção de controles
        self.criar_secao_controles(main_frame)

    def criar_secao_gerar(self, parent):
        """Cria seção para gerar novas senhas"""
        frame = tk.LabelFrame(
            parent,
            text="Gerar Nova Senha",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        frame.pack(fill="x", pady=10)

        # Display da próxima senha
        self.label_proxima = tk.Label(
            frame,
            textvariable=self.proxima_senha,
            font=("Arial", 48, "bold"),
            bg="#3498db",
            fg="white",
            relief="raised",
            bd=3,
            padx=20,
            pady=15
        )
        self.label_proxima.pack(pady=10)

        # Botão gerar senha
        btn_gerar = tk.Button(
            frame,
            text="GERAR NOVA SENHA",
            font=("Arial", 16, "bold"),
            bg="#27ae60",
            fg="white",
            relief="raised",
            bd=3,
            padx=30,
            pady=15,
            command=self.gerar_senha
        )
        btn_gerar.pack(pady=10)

    def criar_secao_chamar(self, parent):
        """Cria seção para chamar senhas"""
        frame = tk.LabelFrame(
            parent,
            text="Chamar Próxima Senha",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        frame.pack(fill="x", pady=10)

        # Frame para entrada da senha
        entrada_frame = tk.Frame(frame, bg="#f0f0f0")
        entrada_frame.pack(pady=10)

        tk.Label(
            entrada_frame,
            text="Senha a chamar:",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(side="left", padx=(0, 10))

        self.entrada_senha = tk.Entry(
            entrada_frame,
            font=("Arial", 14),
            width=10,
            justify="center"
        )
        self.entrada_senha.pack(side="left", padx=(0, 10))

        btn_chamar = tk.Button(
            entrada_frame,
            text="CHAMAR SENHA",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=5,
            command=self.chamar_senha
        )
        btn_chamar.pack(side="left", padx=10)

        # Lista de senhas pendentes
        tk.Label(
            frame,
            text="Senhas Pendentes:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        ).pack(anchor="w", pady=(10, 5))

        # Frame para lista com scrollbar
        lista_frame = tk.Frame(frame, bg="#f0f0f0")
        lista_frame.pack(fill="both", expand=True, pady=5)

        self.lista_senhas = tk.Listbox(
            lista_frame,
            font=("Arial", 12),
            height=6,
            selectmode=tk.SINGLE
        )
        scrollbar = tk.Scrollbar(lista_frame, orient="vertical")
        scrollbar.config(command=self.lista_senhas.yview)
        self.lista_senhas.config(yscrollcommand=scrollbar.set)

        self.lista_senhas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def criar_secao_estatisticas(self, parent):
        """Cria seção de estatísticas"""
        frame = tk.LabelFrame(
            parent,
            text="Estatísticas do Dia",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        frame.pack(fill="x", pady=10)

        stats_frame = tk.Frame(frame, bg="#f0f0f0")
        stats_frame.pack(fill="x", pady=10)

        # Total de senhas
        self.criar_stat_box(stats_frame, "Total Geradas", self.total_senhas, "#3498db")
        self.criar_stat_box(stats_frame, "Chamadas", self.senhas_chamadas, "#27ae60")
        self.criar_stat_box(stats_frame, "Pendentes", self.senhas_pendentes, "#f39c12")

    def criar_stat_box(self, parent, titulo, variavel, cor):
        """Cria uma caixa de estatística"""
        box_frame = tk.Frame(parent, bg=cor, relief="raised", bd=2)
        box_frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            box_frame,
            text=titulo,
            font=("Arial", 12, "bold"),
            bg=cor,
            fg="white"
        ).pack(pady=(10, 5))

        tk.Label(
            box_frame,
            textvariable=variavel,
            font=("Arial", 20, "bold"),
            bg=cor,
            fg="white"
        ).pack(pady=(0, 10))

    def criar_secao_controles(self, parent):
        """Cria seção de controles administrativos"""
        frame = tk.LabelFrame(
            parent,
            text="Controles",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        frame.pack(fill="x", pady=10)

        controles_frame = tk.Frame(frame, bg="#f0f0f0")
        controles_frame.pack(pady=10)

        btn_reset = tk.Button(
            controles_frame,
            text="Resetar Dia",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=5,
            command=self.resetar_dia
        )
        btn_reset.pack(side="left", padx=10)

        btn_relatorio = tk.Button(
            controles_frame,
            text="Gerar Relatório",
            font=("Arial", 12),
            bg="#9b59b6",
            fg="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=5,
            command=self.gerar_relatorio
        )
        btn_relatorio.pack(side="left", padx=10)

    def gerar_senha(self):
        """Gera uma nova senha"""
        self.verificar_nova_data()

        self.senhas_data['contador'] += 1
        nova_senha = f"A{self.senhas_data['contador']:03d}"

        senha_info = {
            'numero': nova_senha,
            'hora_gerada': datetime.now().strftime("%H:%M:%S"),
            'status': 'pendente'
        }

        self.senhas_data['senhas_geradas'].append(senha_info)
        self.salvar_dados()
        self.atualizar_contador()
        self.atualizar_lista_senhas()

        messagebox.showinfo("Senha Gerada", f"Sua senha é: {nova_senha}")

    def chamar_senha(self):
        """Chama uma senha específica"""
        senha_chamada = self.entrada_senha.get().strip().upper()

        if not senha_chamada:
            messagebox.showwarning("Aviso", "Digite o número da senha a ser chamada!")
            return

        # Procura a senha nas pendentes
        senha_encontrada = None
        for senha in self.senhas_data['senhas_geradas']:
            if senha['numero'] == senha_chamada and senha['status'] == 'pendente':
                senha_encontrada = senha
                break

        if senha_encontrada:
            senha_encontrada['status'] = 'chamada'
            senha_encontrada['hora_chamada'] = datetime.now().strftime("%H:%M:%S")
            self.senhas_data['senhas_chamadas'].append(senha_encontrada)

            self.salvar_dados()
            self.atualizar_contador()
            self.atualizar_lista_senhas()
            self.entrada_senha.delete(0, tk.END)

            messagebox.showinfo("Senha Chamada", f"Senha {senha_chamada} foi chamada!")
        else:
            messagebox.showwarning("Aviso", f"Senha {senha_chamada} não encontrada ou já foi chamada!")

    def atualizar_contador(self):
        """Atualiza contadores na interface"""
        total = len(self.senhas_data['senhas_geradas'])
        chamadas = len([s for s in self.senhas_data['senhas_geradas'] if s['status'] == 'chamada'])
        pendentes = total - chamadas

        self.total_senhas.set(total)
        self.senhas_chamadas.set(chamadas)
        self.senhas_pendentes.set(pendentes)

        # Próxima senha a ser gerada
        proximo_num = self.senhas_data['contador'] + 1
        self.proxima_senha.set(f"A{proximo_num:03d}")

    def atualizar_lista_senhas(self):
        """Atualiza lista de senhas pendentes"""
        self.lista_senhas.delete(0, tk.END)

        senhas_pendentes = [
            s for s in self.senhas_data['senhas_geradas']
            if s['status'] == 'pendente'
        ]

        for senha in senhas_pendentes:
            self.lista_senhas.insert(tk.END, f"{senha['numero']} - {senha['hora_gerada']}")

    def resetar_dia(self):
        """Reseta contador do dia"""
        resposta = messagebox.askyesno(
            "Confirmar Reset",
            "Tem certeza que deseja resetar todas as senhas do dia?"
        )

        if resposta:
            self.senhas_data['contador'] = 0
            self.senhas_data['senhas_geradas'] = []
            self.senhas_data['senhas_chamadas'] = []
            self.salvar_dados()
            self.atualizar_contador()
            self.atualizar_lista_senhas()
            messagebox.showinfo("Reset", "Senhas resetadas com sucesso!")

    def gerar_relatorio(self):
        """Gera relatório do dia"""
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        total = len(self.senhas_data['senhas_geradas'])
        chamadas = len([s for s in self.senhas_data['senhas_geradas'] if s['status'] == 'chamada'])
        pendentes = total - chamadas

        relatorio = f"""
RELATÓRIO DIÁRIO - {data_hoje}

=== RESUMO ===
Total de senhas geradas: {total}
Senhas chamadas: {chamadas}
Senhas pendentes: {pendentes}

=== SENHAS GERADAS ===
"""

        for senha in self.senhas_data['senhas_geradas']:
            status = "✓ Chamada" if senha['status'] == 'chamada' else "⏳ Pendente"
            relatorio += f"{senha['numero']} - {senha['hora_gerada']} - {status}\n"

        # Salva relatório em arquivo
        nome_arquivo = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(relatorio)

            messagebox.showinfo("Relatório", f"Relatório salvo como: {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar relatório: {e}")

    def executar(self):
        """Inicia a aplicação"""
        # Atualiza lista inicial
        self.atualizar_lista_senhas()

        # Configura evento de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar)

        # Inicia loop principal
        self.root.mainloop()

    def ao_fechar(self):
        """Ações ao fechar aplicação"""
        self.salvar_dados()
        self.root.destroy()


if __name__ == "__main__":
    app = SistemasenhaEspera()
    app.executar()
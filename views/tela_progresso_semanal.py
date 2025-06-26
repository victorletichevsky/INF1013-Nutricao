import tkinter as tk
from tkinter import ttk, messagebox
from controllers.progresso_semanal_controller import ProgressoSemanalController
from utils.session import get_usuario
from datetime import datetime, timedelta

class TelaProgressoSemanal:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ProgressoSemanalController()

        self.setup_ui()
        self.carregar_progresso()
    
    def setup_ui(self):
        # Frame principal
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(self.frame, text="Progresso Semanal", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # Frame de navegação
        nav_frame = ttk.Frame(self.frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="← Semana Anterior", command=self.semana_anterior).pack(side=tk.LEFT)
        self.label_semana = ttk.Label(nav_frame, font=('Arial', 12, 'bold'))
        self.label_semana.pack(side=tk.LEFT, expand=True)
        ttk.Button(nav_frame, text="Próxima Semana →", command=self.proxima_semana).pack(side=tk.RIGHT)
        
        # Frame do resumo
        resumo_frame = ttk.LabelFrame(self.frame, text="Resumo da Semana", padding=10)
        resumo_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.labels_resumo = {}
        resumo_info = [
            ('total_calorias', 'Total de Calorias:'),
            ('media_calorias', 'Média Diária:'),
            ('taxa_cumprimento', 'Taxa de Cumprimento:')
        ]
        
        for i, (key, text) in enumerate(resumo_info):
            ttk.Label(resumo_frame, text=text).grid(row=i, column=0, sticky=tk.W, padx=(0, 10))
            self.labels_resumo[key] = ttk.Label(resumo_frame, font=('Arial', 10, 'bold'))
            self.labels_resumo[key].grid(row=i, column=1, sticky=tk.W)
        
        # Tabela de progresso diário
        self.criar_tabela()
        
        self.data_atual = datetime.now().date()
        self.data_inicio_semana = self.data_atual - timedelta(days=self.data_atual.weekday())
    
    def criar_tabela(self):
        # Frame da tabela
        table_frame = ttk.LabelFrame(self.frame, text="Progresso Diário", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ('dia', 'data', 'calorias', 'refeicoes')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        # Cabeçalhos
        self.tree.heading('dia', text='Dia')
        self.tree.heading('data', text='Data')
        self.tree.heading('calorias', text='Calorias')
        self.tree.heading('refeicoes', text='Refeições')
        
        # Largura das colunas
        self.tree.column('dia', width=100)
        self.tree.column('data', width=100)
        self.tree.column('calorias', width=100)
        self.tree.column('refeicoes', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def carregar_progresso(self):
        try:
            usuario = get_usuario()
            if not usuario:
                messagebox.showerror("Erro", "Usuário não encontrado")
                return
            
            progresso = self.controller.obter_progresso_semana_especifica(
                usuario['id_usuario'], self.data_inicio_semana
            )
            
            self.atualizar_interface(progresso)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar progresso: {str(e)}")
    
    def atualizar_interface(self, progresso):
        # Atualizar label da semana
        data_fim = progresso['data_fim']
        self.label_semana.config(text=f"{progresso['data_inicio'].strftime('%d/%m')} - {data_fim.strftime('%d/%m/%Y')}")
        
        # Atualizar resumo
        resumo = progresso['resumo']
        self.labels_resumo['total_calorias'].config(text=f"{resumo['total_calorias']:.0f} kcal")
        self.labels_resumo['media_calorias'].config(text=f"{resumo['media_calorias']:.0f} kcal/dia")
        self.labels_resumo['taxa_cumprimento'].config(text=f"{resumo['taxa_cumprimento']:.1f}%")
        
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Preencher tabela
        dados_formatados = self.controller.formatar_dados_para_exibicao(progresso)
        for dia in dados_formatados:
            self.tree.insert('', tk.END, values=(
                dia['dia_semana'],
                dia['data'].strftime('%d/%m'),
                f"{dia['calorias']:.0f} kcal",
                f"{dia['refeicoes_realizadas']}/{dia['refeicoes_planejadas']}"
            ))
    
    def semana_anterior(self):
        self.data_inicio_semana -= timedelta(days=7)
        self.carregar_progresso()
    
    def proxima_semana(self):
        self.data_inicio_semana += timedelta(days=7)
        self.carregar_progresso()
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.constants import *
from pathlib import Path
from tkinter import TclError
import random

PATH = Path(__file__).parent / 'assets'

#############################################################

# Cria e define os parametros da janela principal
def cria_janela():

    # Calcula o valor minimo de tamanho da janela
    min_width = 1000
    min_height = 700

    # Criação da janela principal
    root = ttk.Window(
        title="Organizador de OS", 
        themename="darkly",
        minsize=(min_width,min_height)
    )

    # Obtém as dimensões da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcula a posição x e y para centralizar
    position_x = (screen_width - min_width) // 2
    position_y = (screen_height - min_height) // 2

    # Define a geometria da janela centralizada
    root.geometry(f"{min_width}x{min_height}+{position_x}+{position_y}")

    return root

#############################################################

# Cria a coleção de frames que serao criados na janela
class OrganizadorOS(ttk.Frame):
    # Selecionador de tema (dark, light).
    def theme_select(self):
        theme=None
 
    # Mostra mensagem toast no canto da tela.    
    def toast_msg(self, text):
        toast = ToastNotification(
            title="ttkbootstrap toast message",
            message=text,
            duration=3000,
            alert=True,
        )
        toast.show_toast()

    # Painel superior, com a barra de botões.
    def top_bar_buttons(self):
        buttonbar = ttk.Frame(self, bootstyle='primary')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        ## Nova otimização
        _func = lambda: self.create_new_os()
        btn = ttk.Button(
            master=buttonbar, text='Gerar Otimização',
            image='add-os-op-light', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        ## Iniciar
        _func = lambda: Messagebox.ok(message='Rodando...')
        btn = ttk.Button(
            master=buttonbar, 
            text='Iniciar', 
            image='play', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## Parar
        _func = lambda: Messagebox.ok(message='parando...')
        btn = ttk.Button(
            master=buttonbar, 
            text='Parar', 
            image='stop-light',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

         ## Resetar
        _func = lambda: self.reset_os_op()
        btn = ttk.Button(
            master=buttonbar, 
            text='Resetar', 
            image='refresh',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## Opções
        _func = lambda: Messagebox.ok(message='Opções...')
        btn = ttk.Button(
            master=buttonbar, 
            text='Opções', 
            image='properties-light',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

    # Painel de parametros da esquerda.
    def parameters_panel(self):
       
        left_panel = ttk.Frame(self, style='bg.TFrame')
        left_panel.pack(side=LEFT, fill=Y)
        lbl_params = ttk.Label(left_panel, text="Parâmetros das OS", font='Helvetica 10 bold')
        lbl_params.pack(anchor=W, padx=(10,150), pady=5)
        
        # PARAMETROS DEFAULT ----------------------------
        renamed_params = {
            "_N_ORDERS" : "Nº de OS",
            "_N_OPERATORS" : "Nº de Operadores",
            "_POPULATION_SIZE" : "Tam. População",
            "_GENERATIONS" : "Gerações",
            "_MUTATION_RATE" : "Taxa mutação %",
            "_ELITISM_SIZE" : "Elitismo",
            "_REINITIALIZE_INTERVAL" : "Reinicialização",
            "_DAYS": "Dias" 
        }

        # Valores máximos para alocar nos parametros.
        max_params = {
            "_N_ORDERS" : 500,
            "_N_OPERATORS" : 500,
            "_POPULATION_SIZE" : 200,
            "_GENERATIONS" : 1000,
            "_MUTATION_RATE" : 100,
            "_ELITISM_SIZE" : 50,
            "_REINITIALIZE_INTERVAL" : 100,
            "_DAYS": 31
        }

        default_parameters = ttk.Frame(left_panel, padding=5)
        default_parameters.pack(fill=X, pady=5, padx=(30, 150))

        # PARAMETROS DINAMICOS ----------------------------
        def toggle_parameters_state():
            """Habilita ou desabilita os widgets no parameters_frame."""
            check_state = self.default_parameters_checkbox.get()
            for child in scale_frame.winfo_children():
                # Verifica se o widget suporta a opção 'state'
                try:
                    # Verifica se é um ttk.Scale e ajusta de forma especial
                    if isinstance(child, ttk.Scale):
                        child.configure(state="disabled" if check_state else "normal")
                except TclError:
                    # Ignora widgets que não suportam a opção 'state'
                    pass
        
        # Variável para o estado do Checkbutton.
        self.default_parameters_checkbox = ttk.BooleanVar(value=False)
        # Command habilita ou desabilita os parametros internos/seus filhos.
        op_default = ttk.Checkbutton(left_panel, 
                                     text='Valores default:', 
                                     bootstyle="info-round-toggle",
                                     variable=self.default_parameters_checkbox, 
                                     command=toggle_parameters_state)
        op_default.pack(fill=X, padx=10, pady=5)

        # Parametros Scroll ---------------------
        parameters_frame = ttk.Frame(left_panel)
        parameters_frame.pack(fill=X, padx=(15, 0), pady=5)

        scale_frame = ttk.Frame(parameters_frame)
        scale_frame.pack(fill=X, pady=(5, 10))

        def update_scale_value(value, scale_var):
            scale_var.set(int(float(value)))

        # ------ Numero de Ordens.
        ttk.Label(scale_frame, text=renamed_params["_N_ORDERS"]).grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.n_orders_scale_value = ttk.IntVar(value=self.params["_N_ORDERS"])  # Valor inicial do Scale
        scale_n_orders = ttk.Scale(scale_frame, from_=1, to=max_params["_N_ORDERS"], value=self.params["_N_ORDERS"], variable=self.n_orders_scale_value,
                                command=lambda value, sv=self.n_orders_scale_value: update_scale_value(value, sv))
        scale_n_orders.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
        # Exibe o valor atual do Scale dinamicamente
        scale_label = ttk.Label(scale_frame, textvariable=self.n_orders_scale_value, width=4)
        scale_label.grid(row=0, column=2, sticky=W, padx=5)
        # Botão para voltar ao valor padrão.
        _func = lambda: update_scale_value(self.params["_N_ORDERS"], scale_n_orders)
        scale_btn = ttk.Button(master=scale_frame, image='reset-small', bootstyle=LINK, command=_func)
        scale_btn.grid(row=0, column=3, sticky=E)

        # ------ Numero de Operadores.
        ttk.Label(scale_frame, text=renamed_params["_N_OPERATORS"]).grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.n_operators_scale_value = ttk.IntVar(value=self.params["_N_OPERATORS"])  # Valor inicial do Scale
        scale_n_operators = ttk.Scale(scale_frame, from_=1, to=max_params["_N_OPERATORS"], value=self.params["_N_OPERATORS"], variable=self.n_operators_scale_value,
                                command=lambda value, sv=self.n_operators_scale_value: update_scale_value(value, sv))
        scale_n_operators.grid(row=1, column=1, sticky=EW, padx=5, pady=5)
        # Exibe o valor atual do Scale dinamicamente
        scale_label = ttk.Label(scale_frame, textvariable=self.n_operators_scale_value, width=4)
        scale_label.grid(row=1, column=2, sticky=W, padx=5)
        # Botão para voltar ao valor padrão.
        _func = lambda: update_scale_value(self.params["_N_OPERATORS"], scale_n_operators)
        scale_btn = ttk.Button(master=scale_frame, image='reset-small', bootstyle=LINK, command=_func)
        scale_btn.grid(row=1, column=3, sticky=W)

        # ------ Tamanho da População.
        ttk.Label(scale_frame, text=renamed_params["_POPULATION_SIZE"]).grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.population_size_scale_value = ttk.IntVar(value=self.params["_POPULATION_SIZE"])  # Valor inicial do Scale
        scale_population_size = ttk.Scale(scale_frame, from_=1, to=max_params["_POPULATION_SIZE"], value=self.params["_POPULATION_SIZE"], variable=self.population_size_scale_value,
                                command=lambda value, sv=self.population_size_scale_value: update_scale_value(value, sv))
        scale_population_size.grid(row=2, column=1, sticky=EW, padx=5, pady=5)
        # Exibe o valor atual do Scale dinamicamente
        scale_label = ttk.Label(scale_frame, textvariable=self.population_size_scale_value, width=4)
        scale_label.grid(row=2, column=2, sticky=W, padx=5)
        # Botão para voltar ao valor padrão.
        _func = lambda: update_scale_value(self.params["_POPULATION_SIZE"], scale_population_size)
        scale_btn = ttk.Button(master=scale_frame, image='reset-small', bootstyle=LINK, command=_func)
        scale_btn.grid(row=2, column=3, sticky=W)

        # ------ Numero de Gerações.
        ttk.Label(scale_frame, text=renamed_params["_GENERATIONS"]).grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.generation_scale_value = ttk.IntVar(value=self.params["_GENERATIONS"])  # Valor inicial do Scale
        scale_generation = ttk.Scale(scale_frame, from_=1, to=max_params["_GENERATIONS"], value=self.params["_GENERATIONS"], variable=self.generation_scale_value,
                                command=lambda value, sv=self.generation_scale_value: update_scale_value(value, sv))
        scale_generation.grid(row=3, column=1, sticky=EW, padx=5, pady=5)
        # Exibe o valor atual do Scale dinamicamente
        scale_label = ttk.Label(scale_frame, textvariable=self.generation_scale_value, width=4)
        scale_label.grid(row=3, column=2, sticky=W, padx=(5,0))
        # Botão para voltar ao valor padrão.
        _func = lambda: update_scale_value(self.params["_GENERATIONS"], scale_generation)
        scale_btn = ttk.Button(master=scale_frame, image='reset-small', bootstyle=LINK, command=_func)
        scale_btn.grid(row=3, column=3, sticky=W)

        # ------ Taxa de Mutabilidade.
        ttk.Label(scale_frame, text=renamed_params["_MUTATION_RATE"]).grid(row=4, column=0, sticky=W, padx=5, pady=5)
        initial_value = int(self.params["_MUTATION_RATE"]*100)
        self.mutation_rate_scale_value = ttk.IntVar(value=initial_value)  # Valor inicial do Scale
        scale_mutation_rate = ttk.Scale(scale_frame, from_=1, to=max_params["_MUTATION_RATE"], value=self.params["_MUTATION_RATE"], variable=self.mutation_rate_scale_value,
                                command=lambda value, sv=self.mutation_rate_scale_value: update_scale_value(value, sv))
        scale_mutation_rate.grid(row=4, column=1, sticky=EW, padx=5, pady=5)
        # Exibe o valor atual do Scale dinamicamente
        scale_label = ttk.Label(scale_frame, textvariable=self.mutation_rate_scale_value, width=4)
        scale_label.grid(row=4, column=2, sticky=W, padx=5)
        # Botão para voltar ao valor padrão.
        _func = lambda: update_scale_value(initial_value, scale_mutation_rate)
        scale_btn = ttk.Button(master=scale_frame, image='reset-small', bootstyle=LINK, command=_func)
        scale_btn.grid(row=4, column=3, sticky=W)

        # ------ Tamanho do Elitismo.
        ttk.Label(scale_frame, text=renamed_params["_ELITISM_SIZE"]).grid(row=5, column=0, sticky=W, padx=5, pady=5)
        self.elitism_size_scale_value = ttk.IntVar(value=self.params["_ELITISM_SIZE"])  # Valor inicial do Scale
        scale_elitism_size = ttk.Scale(scale_frame, from_=1, to=max_params["_ELITISM_SIZE"], value=self.params["_ELITISM_SIZE"], variable=self.elitism_size_scale_value,
                                command=lambda value, sv=self.elitism_size_scale_value: update_scale_value(value, sv))
        scale_elitism_size.grid(row=5, column=1, sticky=EW, padx=5, pady=5)
        # Exibe o valor atual do Scale dinamicamente
        scale_label = ttk.Label(scale_frame, textvariable=self.elitism_size_scale_value, width=4)
        scale_label.grid(row=5, column=2, sticky=W, padx=5)
        # Botão para voltar ao valor padrão.
        _func = lambda: update_scale_value(self.params["_ELITISM_SIZE"], scale_elitism_size)
        scale_btn = ttk.Button(master=scale_frame, image='reset-small', bootstyle=LINK, command=_func)
        scale_btn.grid(row=5, column=3, sticky=W)

        # ------ Intervalo de Reinicialização da população.
        ttk.Label(scale_frame, text=renamed_params["_REINITIALIZE_INTERVAL"]).grid(row=6, column=0, sticky=W, padx=5, pady=5)
        self.reinit_interval_scale_value = ttk.IntVar(value=self.params["_REINITIALIZE_INTERVAL"])  # Valor inicial do Scale
        scale_reinit_interval = ttk.Scale(scale_frame, from_=1, to=max_params["_REINITIALIZE_INTERVAL"], value=self.params["_REINITIALIZE_INTERVAL"], variable=self.reinit_interval_scale_value,
                                command=lambda value, sv=self.reinit_interval_scale_value: update_scale_value(value, sv))
        scale_reinit_interval.grid(row=6, column=1, sticky=EW, padx=5, pady=5)
        # Exibe o valor atual do Scale dinamicamente
        scale_label = ttk.Label(scale_frame, textvariable=self.reinit_interval_scale_value, width=4)
        scale_label.grid(row=6, column=2, sticky=W, padx=5)
        # Botão para voltar ao valor padrão.
        _func = lambda: update_scale_value(self.params["_REINITIALIZE_INTERVAL"], scale_reinit_interval)
        scale_btn = ttk.Button(master=scale_frame, image='reset-small', bootstyle=LINK, command=_func)
        scale_btn.grid(row=6, column=3, sticky=W)

        # ------ Dias a serem organizados.
        ttk.Label(scale_frame, text=renamed_params["_DAYS"]).grid(row=7, column=0, sticky=W, padx=5, pady=5)
        self.max_days_scale_value = ttk.IntVar(value=self.params["_DAYS"])  # Valor inicial do Scale
        scale_max_days = ttk.Scale(scale_frame, from_=1, to=max_params["_DAYS"], value=self.params["_DAYS"], variable=self.max_days_scale_value,
                                command=lambda value, sv=self.max_days_scale_value: update_scale_value(value, sv))
        scale_max_days.grid(row=7, column=1, sticky=EW, padx=5, pady=5)
        # Exibe o valor atual do Scale dinamicamente
        scale_label = ttk.Label(scale_frame, textvariable=self.max_days_scale_value, width=4)
        scale_label.grid(row=7, column=2, sticky=W, padx=5)
        # Botão para voltar ao valor padrão.
        _func = lambda: update_scale_value(self.params["_DAYS"], scale_max_days)
        scale_btn = ttk.Button(master=scale_frame, image='reset-small', bootstyle=LINK, command=_func)
        scale_btn.grid(row=7, column=3, sticky=W)

        # SEPARADOR ----------------------------
        sep = ttk.Separator(left_panel, bootstyle=SECONDARY)
        sep.pack(fill=X)

        # MEDIDOR ----------------------------
        meter_frame = ttk.Frame(left_panel, padding=5)
        meter_frame.pack(fill=X, pady=30, padx=30)

        meter = ttk.Meter(
            meter_frame, 
            metersize=180,
            padding=5,
            amountused=0,
            metertype="full",
            subtext="Best Fitness",
            interactive=True,
        )
        meter.pack(fill=X, padx=10, pady=10)

        generation_value = ttk.IntVar(value=1)
        lbl_generation = ttk.Label(meter_frame, text="Geração:", font='Helvetica 10 bold')
        lbl_generation.pack(side=LEFT, padx=(50, 10), pady=10)
        lbl_generation_value = ttk.Label(meter_frame, text=str(generation_value.get()), font='Helvetica 10 bold')
        lbl_generation_value.pack(side=LEFT)

        # # Atualiza dinamicamente o valor do lbl_generation_value
        # def update_generation_label(*args):
        #     lbl_generation_value.config(text=str(generation_value.get()))

        # # Associa a função de atualização à variável generation_value
        # generation_value.trace_add("write", update_generation_label)
        
    # Painel de tabs mostrando os resultados por dia, operador e OS.
    def tab_results_panel(self):
        # Painel direito - Tabs para resultados e listagem
        right_panel = ttk.Notebook(self)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Aba: Resultados por dia
        tab_dia = ttk.Frame(right_panel, padding=5)
        right_panel.add(tab_dia, text="Resultados por Dia")

        lbl_dia = ttk.Label(tab_dia, text="Resultados agrupados por dia", font='Helvetica 12 bold')
        lbl_dia.pack(anchor=W, pady=5)

        tree_dia = ttk.Treeview(tab_dia, columns=("Dia", "Total OS", "Operador"), show="headings")
        tree_dia.heading("Dia", text="Dia")
        tree_dia.heading("Operador", text="Operador")
        tree_dia.heading("Total OS", text="Lista OS")
        tree_dia.pack(fill=BOTH, expand=YES, pady=5)

        # Aba: Resultados por operador
        tab_operador = ttk.Frame(right_panel, padding=5)
        right_panel.add(tab_operador, text="Resultados por Operador")

        lbl_operador = ttk.Label(tab_operador, text="Resultados agrupados por operador", font='Helvetica 12 bold')
        lbl_operador.pack(anchor=W, pady=5)

        tree_operador = ttk.Treeview(tab_operador, columns=("Operador", "Total OS", "Dia"), show="headings")
        tree_operador.heading("Operador", text="Operador")
        tree_operador.heading("Total OS", text="Total OS")
        tree_operador.heading("Dia", text="Dia")
        tree_operador.pack(fill=BOTH, expand=YES, pady=5)

        # Aba: Listagem geral das OSs
        tab_os = ttk.Frame(right_panel, padding=5)
        right_panel.add(tab_os, text="Listagem Os")

        lbl_os = ttk.Label(tab_os, text="Listagem geral das OSs", font='Helvetica 12 bold')
        lbl_os.pack(anchor=W, pady=5)

        tree_os = ttk.Treeview(tab_os, columns=("OS", "Status", "Última Execução"), show="headings")
        tree_os.heading("OS", text="OS")
        tree_os.heading("Status", text="Status")
        tree_os.heading("Última Execução", text="Última Execução")
        tree_os.pack(fill=BOTH, expand=YES, pady=5)

    # Reseta as informações contidas na janela de criaçao de OS e volta parametros ao padrao.
    def reset_os_op(self):
        message= "Tem certeza que quer resetar as tabelas?"
        should_clear = Messagebox.show_question(message, 
                                 title="Reset", 
                                 buttons=['Sim:primary', 'Não:secondary'],
                                 parent=self.operators_table_frame,
                                 alert=True,
                                 )
        if should_clear == 'Sim':
            self.clear_tables() 
        
    # Painel de criação de nova OS pelo usuário.
    def create_new_os(self):
        # Painel à direita.
        right_panel = ttk.LabelFrame(self, text=" Gerenciar Operadores e Ordens de Serviço ", padding=(0, 10, 0, 0))
        right_panel.pack(side=RIGHT, fill=BOTH)
        
        right_panel_tabs = ttk.Notebook(right_panel)
        right_panel_tabs.pack(side=RIGHT, fill=BOTH)

        # ========================== Sub-tab para operadores. ==========================
        operators_tab = ttk.Frame(right_panel_tabs)
        right_panel_tabs.add(operators_tab, text="Operadores")

        # Lista de habilidades, níveis e turnos
        skills_op = ["pintura", "elétrica", "alvenaria", "hidráulica", "solda"]
        levels_op = ["júnior", "pleno", "sênior", "especialista"]
        shifts_op = ["manhã", "tarde", "noite"]

        # Lista de operadores
        operators = []

        scales_vars_names = {
            "_N_ORDERS" : self.n_orders_scale_value,
            "_N_OPERATORS" : self.n_operators_scale_value,
            "_POPULATION_SIZE" : self.population_size_scale_value,
            "_GENERATIONS" : self.generation_scale_value,
            "_MUTATION_RATE" : self.mutation_rate_scale_value,
            "_ELITISM_SIZE" : self.elitism_size_scale_value,
            "_REINITIALIZE_INTERVAL" : self.reinit_interval_scale_value,
            "_DAYS": self.max_days_scale_value
        }

        # Obtém o número de operadores dinamicamente do Scale
        def get_scale_value(parameter):
            operators_disabled = self.default_parameters_checkbox.get()
            if operators_disabled:
                return self.params[parameter]
            else:
                return scales_vars_names[parameter].get()

        # Inputs para adicionar operador manualmente
        operators_frame = ttk.LabelFrame(operators_tab, text=" Adicionar Operador ", padding=10)
        operators_frame.pack(fill=X, pady=(10, 0))

        # Linha horizontal para todos os inputs e labels
        input_op_row = ttk.Frame(operators_frame)
        input_op_row.pack(fill=X, pady=5)

        # Habilidades
        ttk.Label(input_op_row, text="Skills:").pack(side=LEFT, padx=5)
        skills_op_var = ttk.StringVar(value=skills_op[0])
        ttk.OptionMenu(input_op_row, skills_op_var, skills_op[0], *skills_op).pack(side=LEFT, padx=5)

        # Nível
        ttk.Label(input_op_row, text="Nível:").pack(side=LEFT, padx=5)
        level_op_var = ttk.StringVar(value=levels_op[0])
        ttk.OptionMenu(input_op_row, level_op_var, levels_op[0], *levels_op).pack(side=LEFT, padx=5)

        # Turno
        ttk.Label(input_op_row, text="Turno:").pack(side=LEFT, padx=5)
        shift_op_var = ttk.StringVar(value=shifts_op[0])
        ttk.OptionMenu(input_op_row, shift_op_var, shifts_op[0], *shifts_op).pack(side=LEFT, padx=5)

        # Horas/Dia
        ttk.Label(input_op_row, text="Horas/Dia:").pack(side=LEFT, padx=5)
        hours_op_var = ttk.IntVar(value=8)
        ttk.Entry(input_op_row, textvariable=hours_op_var, width=5).pack(side=LEFT, padx=5)

        # TODO: FIX paginaçao nao reseta.
        # Limpa as tabelas dos filtros e zera os rows.
        def clear_tables():
            size_operators = len(operators)
            size_orders = len(orders)
            if(size_operators > 0):
                # Resets dos Operadores
                operator_table.reset_table()
                operator_table.delete_rows()
                operator_table.update()
                operators.clear() # reseta o vetor de operadores.
            
            if (size_orders > 0):
                # Resets das OS
                order_table.reset_table()
                order_table.delete_rows()
                order_table.update()
                orders.clear() # reseta o vetor de orders.


        # Armazena a funçao como um método da classe.
        self.clear_tables = clear_tables

        # Atualiza a tabela com os operadores
        def update_operator_list(operator):
            operator_table.insert_row("end", values=(
                operator["id"],
                operator["skills"],
                operator["level"],
                operator["shift"],
                operator["horas_dia"],
            ))
            operator_table.load_table_data()
            # Centraliza as colunas
            for i, col in enumerate(columns_op):
                operator_table.autofit_columns()

        # Botão para adicionar operador manualmente
        def add_operator():
            n_operators = get_scale_value("_N_OPERATORS")
            if len(operators) < n_operators:
                op_id = f"op{len(operators) + 1}"
                operator = {
                    "id": op_id,
                    "skills": skills_op_var.get(),
                    "level": level_op_var.get(),
                    "shift": shift_op_var.get(),
                    "horas_dia": hours_op_var.get(),
                }
                operators.append(operator)
                update_operator_list(operator)

        ttk.Button(input_op_row, text="Add Operador", command=add_operator).pack(side=LEFT, padx=10, pady=10)

        # Botão para gerar operadores aleatórios.
        def generate_operators():
            n_operators = get_scale_value("_N_OPERATORS")
            while len(operators) < n_operators:
                op_id = f"op{len(operators) + 1}"
                operator = {
                    "id": op_id,
                    "skills": ", ".join(random.sample(skills_op, random.randint(1, 2))),
                    "level": random.choice(levels_op),
                    "shift": random.choice(shifts_op),
                    "horas_dia": random.randint(7, 9),
                }
                operators.append(operator)
                update_operator_list(operator)

        # Linha horizontal para todos os botoes de ação.
        op_buton_row = ttk.Frame(operators_tab)
        op_buton_row.pack( fill=X, pady=5)
        ttk.Button(op_buton_row, text="Gerar Operadores Aleatórios", command=generate_operators).pack(side=LEFT, padx=10, pady=10)
        
        # Tabela para exibir operadores
        self.operators_table_frame = ttk.LabelFrame(operators_tab, text=" Lista Operadores ", padding=10)
        self.operators_table_frame.pack(fill=BOTH, expand=YES)

        columns_op=["Id", "Skills", "Nivel", "Turno", "Horas/Dia"]
        striped_color = ttk.Style().colors.secondary

        num_op_rows = 20
        operator_table = Tableview(
            master= self.operators_table_frame,
            coldata= columns_op,
            rowdata= operators,
            paginated=True, 
            pagesize=num_op_rows,
            searchable=True, 
            autofit=True,
            autoalign=True,
            bootstyle=PRIMARY,
            delimiter=',',
            stripecolor=(striped_color, None),
        )

        # Centralize os cabeçalhos
        for i, col in enumerate(columns_op):
            operator_table.tablecolumns[i].configure(stretch=True)
            operator_table.tablecolumns[i].configure(anchor="center")
            operator_table.autofit_columns()
            operator_table.align_heading_center(None, i)
        
        # Exibe a tabela
        operator_table.pack(fill=BOTH, expand=YES)

        # ========================== Sub-tab para ordens de serviço. ==========================
        orders_tab = ttk.Frame(right_panel_tabs)
        right_panel_tabs.add(orders_tab, text="Ordens de Serviço")

        # Lista de habilidades, níveis e turnos
        required_skills_os = ["pintura", "elétrica", "alvenaria", "hidráulica", "solda"]
        priority_levels_os = ["baixa", "média", "alta", "urgente"]

        # Lista de OS
        orders = []

        max_service_days = get_scale_value("_DAYS")
        days_list_os = []
        for i in range(max_service_days):
            days_list_os.append(i+1)

        # Inputs para adicionar operador manualmente.
        orders_frame = ttk.LabelFrame(orders_tab, text="Adicionar OS", padding=10)
        orders_frame.pack(fill=X, pady=(10, 0))

        # Linha horizontal para todos os inputs e labels.
        input_orders_row = ttk.Frame(orders_frame)
        input_orders_row.pack(fill=X, pady=5)

        # Habilidades Requeridas.
        ttk.Label(input_orders_row, text="Required:").pack(side=LEFT, padx=5)
        required_skills_os_var = ttk.StringVar(value=required_skills_os[0])
        ttk.OptionMenu(input_orders_row, required_skills_os_var, required_skills_os[0], *required_skills_os).pack(side=LEFT, padx=5)

        # Horas de trabalho estimadas.
        ttk.Label(input_orders_row, text="Service Time:").pack(side=LEFT, padx=5)
        estimated_hours_os_var = ttk.IntVar(value=1)
        ttk.Entry(input_orders_row, textvariable=estimated_hours_os_var, width=5).pack(side=LEFT, padx=5)

        # Prioridade da OS.
        ttk.Label(input_orders_row, text="Priority:").pack(side=LEFT, padx=5)
        priority_levels_os_var = ttk.StringVar(value=priority_levels_os[0])
        ttk.OptionMenu(input_orders_row, priority_levels_os_var, priority_levels_os[0], *priority_levels_os).pack(side=LEFT, padx=5)

        # Dia esperado de início.
        ttk.Label(input_orders_row, text="Start Day:").pack(side=LEFT, padx=5)
        expected_start_day_os_var = ttk.StringVar(value=days_list_os[0])
        ttk.OptionMenu(input_orders_row, expected_start_day_os_var, days_list_os[0], *days_list_os).pack(side=LEFT, padx=5)

        # Atualiza a tabela com os operadores.
        def update_order_list(order):
            order_table.insert_row("end", values=(
                order["id"],
                order["required_skills"],
                order["estimated_hours"],
                order["priority"],
                order["expected_start_day"],
                order["status"],
            ))
            order_table.load_table_data()
            # Centraliza as colunas
            for i, col in enumerate(columns_os):
                order_table.autofit_columns()

        # Botão para adicionar ordem manualmente
        def add_order():
            n_orders = get_scale_value("_N_ORDERS")
            if len(orders) < n_orders:
                os_id = f"os{len(orders) + 1}"
                order = {
                    "id": os_id,
                    "required_skills": required_skills_os_var.get(),
                    "estimated_hours": estimated_hours_os_var.get(),
                    "priority": priority_levels_os_var.get(),
                    "expected_start_day": expected_start_day_os_var.get(),
                    "status": "não_atendida",
                }
                orders.append(order)
                update_order_list(order)

        ttk.Button(input_orders_row, text="Add OS", command=add_order).pack(side=LEFT, padx=10, pady=10)

        # Botão para gerar operadores aleatórios.
        def generate_orders():
            n_orders = get_scale_value("_N_ORDERS")
            while len(orders) < n_orders:
                os_id = f"os{len(orders) + 1}"
                order = {
                    "id": os_id,
                    "required_skills": ", ".join(random.sample(required_skills_os, random.randint(1, 2))),
                    "estimated_hours": random.randint(1, 8),
                    "priority": random.choice(priority_levels_os),
                    "expected_start_day": random.randint(1, max_service_days),
                    "status": "não_atendida",
                }
                orders.append(order)
                update_order_list(order)

        # Linha horizontal para todos os botoes de ação.
        os_buton_row = ttk.Frame(orders_tab)
        os_buton_row.pack( fill=X, pady=5)
        ttk.Button(os_buton_row, text="Gerar OS Aleatórias", command=generate_orders).pack(side=LEFT, padx=10, pady=10)
        
        # Tabela para exibir OS
        orders_table_frame = ttk.LabelFrame(orders_tab, text=" Lista de OS ", padding=10)
        orders_table_frame.pack(fill=BOTH, expand=YES)

        columns_os=["Id", "Serviço", "Tempo de Serviço", "Prioridade", "Previsão de Inicio", "Status"]
        striped_color = ttk.Style().colors.secondary
        num_os_rows = 20
        order_table = Tableview(
            master= orders_table_frame,
            coldata= columns_os,
            rowdata= orders,
            paginated=True, 
            pagesize=num_os_rows,
            searchable=True, 
            autofit=True,
            autoalign=True,
            bootstyle=PRIMARY,
            delimiter=',',
            stripecolor=(striped_color, None),
        )

        # Centralize os cabeçalhos
        for i, col in enumerate(columns_os):
            order_table.tablecolumns[i].configure(stretch=True)
            order_table.tablecolumns[i].configure(anchor="center")
            order_table.align_heading_center(None, i)
            order_table.autofit_columns()
        
        # Exibe a tabela
        order_table.pack(fill=BOTH, expand=YES)


#######################################################    
    
    # Algoritmo principal da classe.    
    def __init__(self, *args, **kwargs):
        # Extrai os parâmetros personalizados de kwargs, se existirem
        self.params = kwargs.pop('params', {})

        # Inicializa a classe base com os demais argumentos
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        image_files = {
            'properties-dark': 'icons8_settings_24px.png',
            'properties-light': 'icons8_settings_24px_2.png',
            'add-os-op-dark': 'icons8_add_folder_24px.png',
            'add-os-op-light': 'icons8_add_book_24px.png',
            'stop-backup-dark': 'icons8_cancel_24px.png',
            'stop-backup-light': 'icons8_cancel_24px_1.png',
            'play': 'icons8_play_24px_1.png',
            'refresh': 'icons8_refresh_24px_1.png',
            'stop-dark': 'icons8_stop_24px.png',
            'stop-light': 'icons8_stop_24px_1.png',
            'opened-folder': 'icons8_opened_folder_24px.png',
            'reset':'icons8_reset_24px.png',
            'reset-small':'icons8_reset_16px.png',
        }

        
        # Define a lista imagens, salvando cadda key e seu caminho do arquivo.
        self.photoimages = []
        imgpath = Path(__file__).parent / 'assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))
        
        
        # --- ordenaçao dos paineis ---
        self.top_bar_buttons()
        self.parameters_panel()
        self.create_new_os()

#############################################################

# Roda o algoritmo diretamente no arquivo
if __name__ == '__main__':    
    # Cria janela principal
    params = {
        "_N_ORDERS" : 100,
        "_N_OPERATORS" : 10,
        "_POPULATION_SIZE" : 50,
        "_GENERATIONS" : 50,
        "_MUTATION_RATE" : 0.3,
        "_ELITISM_SIZE" : 5,
        "_REINITIALIZE_INTERVAL" : 10,
        "_DAYS": 5,  
    }
    app = cria_janela()
    OrganizadorOS(app, params=params)
    app.mainloop()

from tkinter import *
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.constants import *
from pathlib import Path

import random
import pandas as pd

# Funções dos algoritmos
import common_functions as cf
import genetic_algorithm as ga

PATH = Path(__file__).parent / 'assets'

#############################################################

# Cria e define os parametros da janela principal
def cria_janela():

    # Calcula o valor minimo de tamanho da janela
    min_width = 1070
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
    #============= UTILITIES =============
    # Selecionador de tema (dark, light).
    def theme_select(self, theme_name):
        """
        Altera o tema da interface.
        Args:
            theme_name (str): Nome do tema a ser aplicado.
        """
        style = ttk.Style(theme=theme_name)
        # Atualiza as tabelas para refletir o novo tema
        self.result_table_dia.configure(bootstyle=style)
        self.result_table_operator.configure(bootstyle=style)
        self.result_table_os.configure(bootstyle=style)
 
    # Mostra mensagem toast no canto da tela.    
    def toast_msg(self, text):
        selected = self.selected_alg.get()
        toast = ToastNotification(
            title=selected,
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
        # _func = lambda: self.create_new_os()
        # btn = ttk.Button(
        #     master=buttonbar, text='Gerar Otimização',
        #     image='add-os-op-light', 
        #     compound=LEFT, 
        #     command=_func
        # )
        # btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        ## Iniciar
        _func = lambda: self.run_genetic_algorithm()
        btn = ttk.Button(
            master=buttonbar, 
            text='Iniciar', 
            image='play', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## Parar
        # _func = lambda: self.stop_execution()
        # btn = ttk.Button(
        #     master=buttonbar, 
        #     text='Parar', 
        #     image='stop-light',
        #     compound=LEFT, 
        #     command=_func
        # )
        # btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

         ## Resetar
        _func = lambda: self.reset_infos()
        btn = ttk.Button(
            master=buttonbar, 
            text='Resetar', 
            image='refresh',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## Opções
        # _func = lambda: Messagebox.ok(message='Opções...')
        # btn = ttk.Button(
        #     master=buttonbar, 
        #     text='Opções', 
        #     image='properties-light',
        #     compound=LEFT, 
        #     command=_func
        # )
        # btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

    # Salva arquivo no computador do usuario por filedialog.
    def export_to_file(self):
        # Abre uma janela para o usuário escolher o local e o nome do arquivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",  # Extensão padrão do arquivo
            filetypes=[("Arquivos CSV", "*.csv"), ("Excel files", "*.xlsx"), ("Todos os arquivos", "*.*")],  # Tipos de arquivo permitidos
            title="Salvar Arquivo"  # Título da janela
        )

        if not file_path :
            return  # Usuário cancelou a ação

        # Se o usuário escolher um local (não cancelar a operação)
        try:
            if self.solution_dataframe is not None:
                if file_path.endswith(".csv"):
                    # Salva o DataFrame no local escolhido
                    self.solution_dataframe.to_csv(file_path, index=False, sep=",")
                elif file_path.endswith(".xlsx"):
                    self.solution_dataframe.to_excel(file_path, index=False)
                
                Messagebox.show_info(title="Sucesso", 
                                        message="Arquivo exportado com sucesso!",
                                        parent=self.savefile_btn_row)
        except Exception as e:
            Messagebox.show_error(title="Erro", 
                                    message=f"Falha ao exportar: {e}",
                                    parent=self.savefile_btn_row)

    #============= FUNCTIONS ============= 
    # Reseta as informações contidas na janela de criaçao de OS e volta parametros ao padrao.
    def reset_infos(self):
        message= "Tem certeza que quer resetar as tabelas?"
        should_clear = Messagebox.show_question(message, 
                                 title="Reset", 
                                 buttons=['Sim:primary', 'Não:secondary'],
                                 parent=self.op_btn_row,
                                 alert=True,
                                 )
        if should_clear == 'Sim':
            self.clear_tables() 
            self.clear_results()

    # Limpa as tabelas de criaçao.
    def clear_tables(self):
        """
        Limpa todas as tabelas e seus dados.
        """
        tables = [
            ("operator_table", "operators"),
            ("order_table", "orders"),
        ]

        for table_name, data_name in tables:
            if hasattr(self, table_name) and hasattr(self, data_name):
                table = getattr(self, table_name)
                data = getattr(self, data_name)
                table.reset_table()
                table.delete_rows()
                table.load_table_data()
                data.clear()

    # Cria tabelas organizadas e alinhadas utilizando TableView.
    def create_table(self, master, columns, rowdata, frame_text):
        """
        Cria uma tabela (Tableview) com configurações padrão.
        Args:
            master: O widget pai onde a tabela será inserida.
            columns (list): Lista de colunas da tabela.
            rowdata (list): Dados iniciais das linhas.
            frame_text (str): Texto do LabelFrame que contém a tabela.
        Returns:
            Tableview: A tabela criada.
        """
        frame = ttk.LabelFrame(master, text=frame_text, padding=10)
        frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        table = Tableview(
            master=frame,
            coldata=columns,
            rowdata=rowdata,
            paginated=True,
            pagesize=20,
            searchable=True,
            autofit=True,
            autoalign=True,
            bootstyle=PRIMARY,
            delimiter=',',
            stripecolor=(ttk.Style().colors.secondary, None),
        )

       # Configura todas as colunas para centralizar o conteúdo
        for i in range(len(table.tablecolumns)):
            table.tablecolumns[i].configure(stretch=True, anchor="center")
            table.align_heading_center(None, i)
        
        table.autofit_columns()

        table.pack(fill=BOTH, expand=YES)
        return table

    # Atualiza tabelas com a solução encontrada para visualização.
    def update_tables_with_solution(self, best_solution):
        """
        Atualiza as tabelas de resultados com os dados da melhor solução.
        Args:
            best_solution (dict): A melhor solução encontrada pelo algoritmo.
        """
        # Limpa as tabelas antes de adicionar novos dados
        self.clear_results()

        # Dados para as tabelas
        # result_data_dia = []
        # result_data_operator = []
        result_data_os = []
        operator_daily_hours = {}

        # Processa a best_solution para preencher as tabelas
        for order_id, order_data in best_solution["orders"].items():
            day = order_data["day"]
            operator_id = order_data["operator"]
            status = order_data["status"]

            # Dados do operador (se disponível)
            operator_info = self.operators.get(operator_id, {})
            op_skills = operator_info.get("skills", "")
            level = operator_info.get("level", "N/A")
            shift = operator_info.get("shift", "N/A")           # ---> Não utilizado.
            hours_per_day = operator_info.get("hours_per_day", 0)

            # Dados da ordem
            order_info = self.orders.get(order_id, {})
            required_skills = order_info.get("required_skills", "")
            estimated_hours = order_info.get("estimated_hours", 0)
            priority = order_info.get("priority", "N/A")
            expected_start_day = order_info.get("expected_start_day", 0)

            # Infos adicionais
            late_work = max(0, day - expected_start_day)  # Atraso

            # Ordem correta das habilidades
            skills_order = ["pintura", "elétrica", "alvenaria", "hidráulica", "solda"]
            ordered_required_skills = [skill for skill in skills_order if skill in required_skills]
            ordered_op_skills = [skill for skill in skills_order if skill in op_skills]

            # Converte as listas de habilidades em conjuntos
            required_skills_set = set(ordered_required_skills)
            operator_skills_set = set(ordered_op_skills)

            # Calcula as habilidades correspondentes e faltantes
            matched_skills = required_skills_set & operator_skills_set
            missing_skills = required_skills_set - operator_skills_set

            # Calcula compatibilidade de habilidades
            skill_compatibility = len(matched_skills) / len(required_skills_set) if required_skills_set else 1.0
            skill_match = round(skill_compatibility * 100, 2)

            # Mapeia a compatibilidade de nível de prioridade
            priority_level_map = {
                "alta": ["especialista", "sênior"],
                "urgente": ["especialista", "sênior"],
                "média": ["especialista", "sênior", "pleno"],
                "baixa": ["especialista", "sênior", "pleno", "júnior"]
            }
            compatibility_level = "OK" if level in priority_level_map.get(priority, []) else "NOK"
            
            # Inicializa horas trabalhadas por operador no dia, se necessário.
            if day not in operator_daily_hours:
                operator_daily_hours[day] = {}
            if operator_id not in operator_daily_hours[day]:
                operator_daily_hours[day][operator_id] = 0

            operator_daily_hours[day][operator_id] += estimated_hours
            total_hours = operator_daily_hours[day][operator_id]
            
            extra_hours = "Sim" if total_hours > hours_per_day else "Não"
            total_extra_hours = total_hours - hours_per_day

            # Adiciona dados à tabela de resultados por dia
            # result_data_dia.append([order_id, skills, level, shift, hours_per_day])

            # Adiciona dados à tabela de resultados por operador
            # result_data_operator.append([operator_id, skills, level, shift, hours_per_day])

            # Formata missing_skills como uma string legível
            missing_skills_str = ", ".join(missing_skills) if missing_skills else "N/A"
            required_skills_str = ", ".join(required_skills) if required_skills else "N/A"
            op_skills_str = ", ".join(op_skills) if required_skills else "N/A"

            # Formata skill_match como uma string com o símbolo de porcentagem
            skill_match_str = f"{skill_match}%"
            
            # Adiciona dados à tabela de listagem geral das OS.
            row = [day, order_id, operator_id, required_skills_str, op_skills_str, level, 
                    estimated_hours, hours_per_day, priority, expected_start_day, late_work, 
                    skill_match_str, missing_skills_str, compatibility_level, extra_hours, total_extra_hours, status]
           
            # Converte todos os valores da linha para string.
            # row = [str(value) if value is not None else "" for value in row]

            # Insere a linha na tabela.
            result_data_os.append(row)
            self.result_table_os.insert_row("end", values=row)

        # Atualiza as tabelas com os novos dados
        # self.result_data_dia = result_data_dia  # Substitui os dados antigos
        # self.result_data_operator = result_data_operator  # Substitui os dados antigos
        self.result_data_os = result_data_os  # Substitui os dados antigos
        
        # Atualiza as tabelas na interface
        # self.result_table_dia.load_table_data()
        # self.result_table_operator.load_table_data()

        # Centraliza os cabeçalhos e ajusta as colunas.
        # Configura todas as colunas para centralizar o conteúdo
        
        for i in range(len(self.result_table_os.tablecolumns)):
            self.result_table_os.tablecolumns[i].configure(stretch=True, anchor="center")
            self.result_table_os.align_heading_center(None, i)
        
        # Ajusta as colunas ao tamanho do conteúdo.
        self.result_table_os.autofit_columns()
       
        # Atualiza a tabela na interface.
        self.result_table_os.load_table_data()

        # Transforma a solução em DataFrame e disponibiliza pra salvamento.
        self.solution_dataframe, self.unassigned_orders = cf.solution_to_dataframe(best_solution, self.operators, self.orders)

        # Atualiza botao de salvamento.
        self.update_save_button_state()
    
    # Update nos valores dos scales.
    def update_scale_value(self, value, scale_var):
        """
        Atualiza o valor de uma variável de Scale.
        Args:
            value (str): Valor do Scale (vem como string).
            scale_var (ttk.IntVar): Variável associada ao Scale.
        """
        scale_var.set(int(float(value)))
    
    # Obtem os valores do scale passado na referencia.
    def get_scale_value(self, parameter):
        """
        Obtém o valor de um parâmetro da escala.
        Args:
            parameter (str): Nome do parâmetro (ex: "_N_ORDERS").
        Returns:
            int: Valor da escala.
        """
        if self.default_parameters_checkbox.get():
            return self.params[parameter]  # Usa o valor padrão se o checkbox estiver marcado
        else:
            # Acessa o atributo dinâmico criado pela função create_scale
            scale_value = getattr(self, f"{parameter.lower()}_scale_value")
            value = scale_value.get()
            if parameter == "_MUTATION_RATE":
                value /= 100.0
                return float(value)
            return value
   
    # Cria um scale dinamico com botao de reset.
    def create_scale(self, master, text, param_name, max_value, row):
        """
        Cria um Scale com Label, valor dinâmico e botão de reset.
        Args:
            master: O widget pai onde o Scale será inserido.
            text (str): Texto do Label.
            param_name (str): Nome do parâmetro.
            max_value (int): Valor máximo do Scale.
            row (int): Linha na grade onde o Scale será posicionado.
        Returns:
            ttk.Scale: O Scale criado.
        """
        # Label do parâmetro.
        ttk.Label(master, text=text).grid(row=row, column=0, sticky=W, padx=5, pady=5)


        # Caso especial.
        min_scale_value = 2 if param_name == "_POPULATION_SIZE" or param_name == "_N_ORDERS" else 1

        if param_name == "_MUTATION_RATE":
            value_normalized = int(self.params[param_name] * 100)
        else:
            value_normalized = self.params[param_name]
       
        # Variável do Scale.
        scale_var = ttk.IntVar(value=value_normalized)
       
        # Scale.
        scale = ttk.Scale(
            master,
            from_=min_scale_value,
            to=max_value,
            value=value_normalized,
            variable=scale_var,
            command=lambda value, sv=scale_var: self.update_scale_value(value, sv),
        )
        scale.grid(row=row, column=1, sticky=EW, padx=5, pady=5)

        # Label para exibir o valor atual do Scale.
        scale_label = ttk.Label(master, textvariable=scale_var, width=4)
        scale_label.grid(row=row, column=2, sticky=W, padx=5)

        # Botão para resetar o valor do Scale.
        reset_func = lambda: self.update_scale_value(self.params[param_name], scale_var)
        reset_btn = ttk.Button(master, image='reset-small', bootstyle=LINK, command=reset_func)
        reset_btn.grid(row=row, column=3, sticky=W)

        # Armazena a variável do Scale para uso posterior.
        setattr(self, f"{param_name.lower()}_scale_value", scale_var)

        return scale
    
    # Desabilita os botões de Scale.
    def toggle_parameters_state(self):
        """
        Habilita ou desabilita os widgets no parameters_frame.
        """
        check_state = self.default_parameters_checkbox.get()
        for child in self.scale_frame.winfo_children():
            if isinstance(child, (ttk.Scale, ttk.Button, ttk.Label)):
                child.configure(state="disabled" if check_state else "normal")

    # Atualiza o valor da geração em baixo do Meter.
    def update_generation_value(self, value):
        """
        Atualiza o valor da geração exibido no painel.
        Args:
            value (int): Número da geração atual.
        """
        self.generation_value.set(value)
    
    # Cria o medidor de fitness do painel a esquerda (Meter).
    def create_fitness_meter(self, master):
        """
        Cria o medidor de fitness e o contador de gerações.
        Args:
            master: O widget pai onde o medidor será inserido.
        """
        meter_frame = ttk.Frame(master, padding=5)
        meter_frame.pack(fill=X, padx=30)

        self.meter = ttk.Meter(
            meter_frame,
            metersize=180,
            padding=5,
            amounttotal=3000,
            amountused=0,
            metertype="full",
            subtext="Best Fitness",
            interactive=False,
        )
        self.meter.pack(fill=X, padx=10, pady=10)

        self.generation_value = ttk.IntVar(value=1)
        lbl_generation = ttk.Label(meter_frame, text="Geração:", font='Helvetica 10 bold')
        lbl_generation.pack(side=LEFT, padx=(70, 0), pady=10)
        lbl_generation_value = ttk.Label(meter_frame, textvariable=self.generation_value)
        lbl_generation_value.pack(side=LEFT)
    
    # Para a execução do algoritmo.
    def stop_execution(self):
        self.stop_running = True

    #============= INTERFACE =============
    # Painel de parametros à esquerda.
    def parameters_panel(self):
        """
        Cria o painel de parâmetros à esquerda da interface.
        """
        left_panel = ttk.Frame(self, style='bg.TFrame')
        left_panel.pack(side=LEFT, fill=Y)

        # Título do painel.
        lbl_params = ttk.Label(left_panel, text="Parâmetros das OS", font='Helvetica 10 bold')
        lbl_params.pack(anchor=W, padx=(10, 0), pady=5)
        
        # Frame para parâmetros default.
        default_parameters = ttk.Frame(left_panel)
        default_parameters.pack(fill=X, pady=5, padx=(5, 0))

        # Checkbutton para habilitar/desabilitar parâmetros
        self.default_parameters_checkbox = ttk.BooleanVar(value=False)
        op_default = ttk.Checkbutton(
            default_parameters, 
            text='Valores default:', 
            bootstyle="info-round-toggle",
            variable=self.default_parameters_checkbox, 
            command=self.toggle_parameters_state
        )
        op_default.pack(fill=X, padx=(10, 0), pady=5)

        # Frame para os Scales
        self.scale_frame = ttk.Frame(default_parameters)
        self.scale_frame.pack(fill=X, pady=(5, 10))

        # Cria os Scales para cada parâmetro
        self.create_scale(self.scale_frame, self.renamed_params["_N_ORDERS"], "_N_ORDERS", self.max_params["_N_ORDERS"], row=0)
        self.create_scale(self.scale_frame, self.renamed_params["_N_OPERATORS"], "_N_OPERATORS", self.max_params["_N_OPERATORS"], row=1)
        self.create_scale(self.scale_frame, self.renamed_params["_POPULATION_SIZE"], "_POPULATION_SIZE", self.max_params["_POPULATION_SIZE"], row=2)
        self.create_scale(self.scale_frame, self.renamed_params["_GENERATIONS"], "_GENERATIONS", self.max_params["_GENERATIONS"], row=3)
        self.create_scale(self.scale_frame, self.renamed_params["_MUTATION_RATE"], "_MUTATION_RATE", self.max_params["_MUTATION_RATE"], row=4)
        self.create_scale(self.scale_frame, self.renamed_params["_ELITISM_SIZE"], "_ELITISM_SIZE", self.max_params["_ELITISM_SIZE"], row=5)
        self.create_scale(self.scale_frame, self.renamed_params["_REINITIALIZE_INTERVAL"], "_REINITIALIZE_INTERVAL", self.max_params["_REINITIALIZE_INTERVAL"], row=6)
        self.create_scale(self.scale_frame, self.renamed_params["_DAYS"], "_DAYS", self.max_params["_DAYS"], row=7)

        # Separador
        sep = ttk.Separator(left_panel, bootstyle=SECONDARY)
        sep.pack(fill=X)

        # Seletor de algoritmo
        algorithms = ["Algoritmo Genético"]
        selec = ttk.Frame(left_panel, padding=5)
        selec.pack(fill=X, pady=(10, 0), padx=(30, 0))

        ttk.Label(selec, text="Algoritmo:").pack(side=LEFT, padx=5)
        shift_op_var = ttk.StringVar(value=algorithms[0])
        ttk.OptionMenu(selec, shift_op_var, algorithms[0], *algorithms).pack(side=LEFT, padx=5)
        self.selected_alg = shift_op_var

        # Medidor de fitness
        self.create_fitness_meter(left_panel)
    
    # Painel de tabs mostrando os resultados por dia, operador e OS.
    def tab_results_panel(self, tab):
        """
        Cria um painel de abas para exibir resultados por dia, operador e OS.
        Args:
            tab: O widget pai onde o painel será inserido.
        """
        # Painel direito - Tabs para resultados e listagem
        right_panel = ttk.Notebook(tab)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Limpa as tabelas dos filtros e zera os rows.
        def clear_results():
            """
            Limpa todas as tabelas e seus dados.
            """
            tables = [
                ("result_table_dia", "result_data_dia"),
                ("result_table_operator", "result_data_operator"),
                ("result_table_os", "result_data_os"),
            ]

            for table_name, data_name in tables:
                if hasattr(self, table_name) and hasattr(self, data_name):
                    table = getattr(self, table_name)
                    data = getattr(self, data_name)
                    table.delete_rows()
                    table.load_table_data()
                    data.clear()
                    update_save_button_state()

        # Atribui a função de forma global.
        self.clear_results = clear_results

        # Aba: Resultados por dia -------------------------
        # tab_day = ttk.Frame(right_panel, padding=5)
        # right_panel.add(tab_day, text="Resultados por Dia")

        # columns_results_dia=["Id", "Skills", "Nivel", "Turno", "Horas/Dia"]
        # self.result_data_dia = []
        # self.result_table_dia = self.create_table(tab_day, columns_results_dia, self.result_data_dia, "Resultados")

        # # Aba: Resultados por operador -------------------------
        # tab_operator = ttk.Frame(right_panel, padding=5)
        # right_panel.add(tab_operator, text="Resultados por Operador")

        # columns_results_operator=["Id", "Skills", "Nivel", "Turno", "Horas/Dia"]
        # self.result_data_operator = []
        # self.result_table_operator = self.create_table(tab_operator, columns_results_operator, self.result_data_operator, "Resultados")
        
        # Aba: Listagem geral das OS -------------------------
        results_tab_os = ttk.Frame(right_panel, padding=5)
        right_panel.add(results_tab_os, text="Listagem Os")

        self.savefile_btn_row = ttk.Frame(results_tab_os)
        self.savefile_btn_row.pack( fill=X, pady=5)
        
        def update_save_button_state():
            if self.result_table_os.tablerows:  # Se houver dados na tabela
                self.save_button.config(state=NORMAL)
            else:
                self.save_button.config(state=DISABLED)
        
        self.update_save_button_state = update_save_button_state

        _func = lambda: self.export_to_file()
        self.save_button = ttk.Button(
                    self.savefile_btn_row, 
                    text="Salvar Resultado", 
                    command=_func,
                    state=DISABLED,
        )
        self.save_button.pack(side=LEFT, padx=10, pady=10)
        

        columns_results_os=["dia", "id_os", "id_op", "Serviços", "skills_operador", "nivel_operador", "horas_estimadas",
                            "horas_disponiveis", "prioridade", "inicio_esperado", "atraso", "compatibilidade_os_op", 
                            "habilidades_nao_atendidas", "compatibilidade_prioridade", "hora_extra", "total_hora_extra", "status"]
        self.result_data_os=[]

        self.result_table_os = self.create_table(results_tab_os, columns_results_os, self.result_data_os, "Resultados")
   
    # Painel de criação de nova OS pelo usuário.
    def create_new(self, tab):
        """
        Cria um painel para adicionar operadores e ordens de serviço (OS).
        Args:
            tab: O widget pai onde o painel será inserido.
        """
        # Painel à direita.
        right_panel_tabs = ttk.Notebook(tab)
        right_panel_tabs.pack(side=RIGHT, fill=BOTH, expand=YES)

        # ========================== Sub-tab para operadores. ==========================
        operators_tab = ttk.Frame(right_panel_tabs)
        right_panel_tabs.add(operators_tab, text="Operadores")

        # Lista de habilidades, níveis e turnos.
        skills_op = ["pintura", "elétrica", "alvenaria", "hidráulica", "solda"]
        levels_op = ["júnior", "pleno", "sênior", "especialista"]
        shifts_op = ["manhã", "tarde", "noite"]

        # Inputs para adicionar operador manualmente.
        operators_frame = ttk.LabelFrame(operators_tab, text=" Adicionar Operador ", padding=10)
        operators_frame.pack(fill=X, pady=(10, 0))

        # Função para criar inputs de operadores.
        def create_operator_inputs(master):
            """
            Cria os inputs para adicionar operadores manualmente.
            Args:
                master: O widget pai onde os inputs serão inseridos.
            Returns:
                dict: Dicionário com as variáveis dos inputs.
            """
            input_op_row = ttk.Frame(master)
            input_op_row.pack(fill=X, pady=5)

            # Skills
            ttk.Label(input_op_row, text="Skills:").pack(side=LEFT)

            # Função para atualizar o texto do Menubutton.
            def update_op_menu_text(skill):
                if skills_op_vars[skill].get():
                    if len(skills_op_selected) < 2:
                        skills_op_selected.append(skill)
                    else:
                        skills_op_vars[skill].set(False)
                else:
                    if skill in skills_op_selected:
                        skills_op_selected.remove(skill)
                ordered_selected = [s for s in skills_op if s in skills_op_selected]
                skill_op_menu_btn.config(text=", ".join(ordered_selected) if ordered_selected else "Selecione")

            # Botão do menu
            skill_op_menu_btn = ttk.Menubutton(input_op_row, text="Selecione", direction="below", width=18)
            skill_op_menu = ttk.Menu(skill_op_menu_btn, tearoff=0)
            skill_op_menu_btn["menu"] = skill_op_menu

            skills_op_selected = []  # Lista de skills selecionadas.
            skills_op_vars = {}  # Dicionário de skills e seus checkboxes.
            for skill in skills_op:
                var = ttk.BooleanVar(value=False)
                skills_op_vars[skill] = var
                skill_op_menu.add_checkbutton(label=skill, variable=var, command=lambda s=skill: update_op_menu_text(s))

            skill_op_menu_btn.pack(side=LEFT, padx=5)

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

            return {
                "skills_op_vars": skills_op_vars,
                "level_op_var": level_op_var,
                "shift_op_var": shift_op_var,
                "hours_op_var": hours_op_var,
                "skill_op_menu_btn": skill_op_menu_btn,
            }

        # Cria os inputs de operadores.
        operator_inputs = create_operator_inputs(operators_frame)

        # Lista de operadores.
        self.operators = {}

        # Função para atualizar a tabela de operadores.
        def update_operator_view(operator, op_id):
            """
            Atualiza a tabela de operadores com um novo operador.
            Args:
                operator (dict): Dados do operador.
                op_id (str): ID do operador.
            """
            self.operator_table.insert_row("end", values=(
                op_id,
                operator["skills"],
                operator["level"],
                operator["shift"],
                operator["hours_per_day"],
            ))
            self.operator_table.load_table_data()

        # Função para adicionar operador manualmente
        def add_operator():
            n_operators = self.get_scale_value("_N_OPERATORS")
            selected_skills = [skill for skill, var in operator_inputs["skills_op_vars"].items() if var.get()]
            for i in range(1, n_operators+1):
                op_id = f"op{i}"
                if op_id not in self.operators:
                    self.operators[op_id] = {
                        "skills": list(selected_skills),
                        "level": operator_inputs["level_op_var"].get(),
                        "shift": operator_inputs["shift_op_var"].get(),
                        "hours_per_day": operator_inputs["hours_op_var"].get(),
                    }
                    update_operator_view(self.operators[op_id], op_id)
                    break
            
        ttk.Button(operators_frame, text="Add", command=add_operator).pack(side=LEFT, padx=10, pady=10)

        # Função para gerar operadores aleatórios.
        def generate_operators():
            n_operators = self.get_scale_value("_N_OPERATORS")
            for i in range(1, n_operators+1):
                op_id = f"op{i}"
                if op_id not in self.operators:
                    self.operators[op_id] = {
                        "skills": random.sample(skills_op, random.randint(1, 2)),
                        "level": random.choice(levels_op),
                        "shift": random.choice(shifts_op),
                        "hours_per_day": random.randint(7, 9),
                    }
                    update_operator_view(self.operators[op_id], op_id)

        self.generate_operators = generate_operators
        
        # Linha horizontal para todos os botoes de ação.
        self.op_btn_row = ttk.Frame(operators_tab)
        self.op_btn_row.pack( fill=X, pady=5)
        ttk.Button(self.op_btn_row, text="Gerar Operadores Aleatórios", command=generate_operators).pack(side=LEFT, padx=10, pady=10)
        
        # Tabela para exibir operadores
        self.operator_table = self.create_table(
            operators_tab,
            ["Id", "Skills", "Nivel", "Turno", "Horas/Dia"],
            self.operators,
            "Lista Operadores",
        )

        # ========================== Sub-tab para ordens de serviço. ==========================
        orders_tab = ttk.Frame(right_panel_tabs)
        right_panel_tabs.add(orders_tab, text="Ordens de Serviço")

        # Lista de habilidades, níveis e turnos
        required_skills_os = ["pintura", "elétrica", "alvenaria", "hidráulica", "solda"]
        priority_levels_os = ["baixa", "média", "alta", "urgente"]

        max_service_days = self.get_scale_value("_DAYS")
        days_list_os = list(range(1, max_service_days + 1))

        # Inputs para adicionar operador manualmente.
        orders_frame = ttk.LabelFrame(orders_tab, text=" Adicionar OS ", padding=10)
        orders_frame.pack(fill=X, pady=(10, 0))

        # Função para criar inputs de OS.
        def create_order_inputs(master):
            """
            Cria os inputs para adicionar ordens de serviço manualmente.
            Args:
                master: O widget pai onde os inputs serão inseridos.
            Returns:
                dict: Dicionário com as variáveis dos inputs.
            """
            input_os_row = ttk.Frame(master)
            input_os_row.pack(fill=X, pady=5)

            # Habilidades Requeridas.
            ttk.Label(input_os_row, text="Serviços:").pack(side=LEFT)

            # Função para atualizar o texto do Menubutton.
            def update_os_menu_text(skill):
                if skills_os_vars[skill].get():
                    if len(skills_os_selected) < 2:
                        skills_os_selected.append(skill)
                    else:
                        skills_os_vars[skill].set(False)
                else:
                    if skill in skills_os_selected:
                        skills_os_selected.remove(skill)
                ordered_selected = [s for s in required_skills_os if s in skills_os_selected]
                skill_os_menu_btn.config(text=", ".join(ordered_selected) if ordered_selected else "Selecione")

            # Botão do menu.
            skill_os_menu_btn = ttk.Menubutton(input_os_row, text="Selecione", direction="below", width=18)
            skill_os_menu = ttk.Menu(skill_os_menu_btn, tearoff=0)
            skill_os_menu_btn["menu"] = skill_os_menu

            skills_os_selected = []  # Lista de skills selecionadas.
            skills_os_vars = {}  # Dicionário de skills e seus checkboxes.
            for skill in required_skills_os:
                var = ttk.BooleanVar(value=False)
                skills_os_vars[skill] = var
                skill_os_menu.add_checkbutton(label=skill, variable=var, command=lambda s=skill: update_os_menu_text(s))

            skill_os_menu_btn.pack(side=LEFT, padx=5)

            # Horas de trabalho estimadas.
            ttk.Label(input_os_row, text="Duração/hrs:").pack(side=LEFT, padx=5)
            estimated_hours_os_var = ttk.IntVar(value=1)
            ttk.Entry(input_os_row, textvariable=estimated_hours_os_var, width=5).pack(side=LEFT, padx=5)

            # Prioridade da OS.
            ttk.Label(input_os_row, text="Prioridade:").pack(side=LEFT, padx=5)
            priority_levels_os_var = ttk.StringVar(value=priority_levels_os[0])
            ttk.OptionMenu(input_os_row, priority_levels_os_var, priority_levels_os[0], *priority_levels_os).pack(side=LEFT, padx=5)

            # Dia esperado de início.
            ttk.Label(input_os_row, text="Dia esperado:").pack(side=LEFT, padx=5)
            expected_start_day_os_var = ttk.IntVar(value=days_list_os[0])
            ttk.OptionMenu(input_os_row, expected_start_day_os_var, days_list_os[0], *days_list_os).pack(side=LEFT, padx=5)

            return {
                "skills_os_vars": skills_os_vars,
                "estimated_hours_os_var": estimated_hours_os_var,
                "priority_levels_os_var": priority_levels_os_var,
                "expected_start_day_os_var": expected_start_day_os_var,
                "skill_os_menu_btn": skill_os_menu_btn,
            }

        # Cria os inputs de OS.
        order_inputs = create_order_inputs(orders_frame)

        # Lista de OS.
        self.orders = {}

        # Atualiza a tabela com os operadores.
        def update_order_view(order, os_id):
            """
            Atualiza a tabela de OS com uma nova ordem.
            Args:
                order (dict): Dados da ordem.
                os_id (str): ID da ordem.
            """
            self.order_table.insert_row("end", values=(
                os_id,
                order["required_skills"],
                order["estimated_hours"],
                order["priority"],
                order["expected_start_day"],
                order["status"],
            ))
            self.order_table.load_table_data()

        # Botão para adicionar ordem manualmente
        def add_order():
            n_orders = self.get_scale_value("_N_ORDERS")
            selected_skills = [skill for skill, var in order_inputs["skills_os_vars"].items() if var.get()]
            for i in range(1, n_orders + 1):
                os_id = f"os{i}"
                if os_id not in self.orders:
                    self.orders[os_id] = {
                        "required_skills": list(selected_skills),
                        "estimated_hours": order_inputs["estimated_hours_os_var"].get(),
                        "priority": order_inputs["priority_levels_os_var"].get(),
                        "expected_start_day": order_inputs["expected_start_day_os_var"].get(),
                        "status": "não_atendida",
                    }
                    update_order_view(self.orders[os_id], os_id)
                    break

        ttk.Button(orders_frame, text="Add", command=add_order).pack(side=LEFT, padx=10, pady=10)

        # Botão para gerar operadores aleatórios.
        def generate_orders():
            n_orders = self.get_scale_value("_N_ORDERS")
            for i in range(1, n_orders + 1):
                os_id = f"os{i}"
                if os_id not in self.orders:
                    self.orders[os_id] = {
                        "required_skills": random.sample(required_skills_os, random.randint(1, 2)),
                        "estimated_hours": random.randint(1, 8),
                        "priority": random.choice(priority_levels_os),
                        "expected_start_day": random.randint(1, max_service_days),
                        "status": "não_atendida",
                    }
                    update_order_view(self.orders[os_id], os_id)

        self.generate_orders = generate_orders

        # Linha horizontal para todos os botoes de ação.
        os_btn_row = ttk.Frame(orders_tab)
        os_btn_row.pack( fill=X, pady=5)
        ttk.Button(os_btn_row, text="Gerar OS Aleatórias", command=generate_orders).pack(side=LEFT, padx=10, pady=10)
    
        # Tabela para exibir OS.
        self.order_table = self.create_table(
            orders_tab,
            ["Id", "Serviço", "Tempo de Serviço", "Prioridade", "Previsão de Inicio", "Status"],
            self.orders,
            "Lista de OS",
        )

    # Painel geral da direita para organizar tabs.
    def right_panel_show(self):
        # Painel à direita.        
        self.right_panel_general = ttk.Notebook(self, bootstyle=PRIMARY)
        self.right_panel_general.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Tab de criaçao.
        self.new_creation_tab = ttk.Frame(self.right_panel_general, padding=(0, 10, 0, 0))
        self.right_panel_general.add(self.new_creation_tab, text="Gerenciar Operadores e OS")
        self.create_new(self.new_creation_tab)

        # Tab de mostrar os resultados.
        self.results_tab = ttk.Frame(self.right_panel_general, padding=(0, 10, 0, 0))
        self.right_panel_general.add(self.results_tab, text="Ver Resultados")
        self.tab_results_panel(self.results_tab)

#############################################################    
 
    # Cria orders e operadores iniciais de acordo com o scale dinamico.
    def create_initial_data(self):
        """
        Cria operadores e ordens iniciais com base nos valores dos parâmetros.
        Returns:
            tuple: (operators, orders)
        """
        # Valores default.
        n_operators = self.get_scale_value("_N_OPERATORS")
        n_orders = self.get_scale_value("_N_ORDERS")
        
        if len(self.operators) < n_operators:
            self.generate_operators()
        
        if len(self.orders) < n_orders:
            self.generate_orders()

        return self.operators, self.orders

    # Atualiza os parametros de acordo com os scales.
    def update_parameters(self):
        """
        Atualiza os parâmetros do algoritmo genético com base nos valores dos Scales.
        """
        self.population_size = self.get_scale_value("_POPULATION_SIZE")
        self.generation_max = self.get_scale_value("_GENERATIONS")
        self.mutation_rate = self.get_scale_value("_MUTATION_RATE")
        self.elitism_size = self.get_scale_value("_ELITISM_SIZE")
        self.reinitiation_point = self.get_scale_value("_REINITIALIZE_INTERVAL")
        self.max_days = self.get_scale_value("_DAYS")

    # Execução Algoritmo Genético.
    def run_genetic_algorithm(self):
        """
        Executa o algoritmo genético para otimizar a alocação de ordens de serviço.
        """
        # Muda para a aba de resultados após rodar o algoritmo
        # self.notebook.select(self.notebook.tabs()[1])

        self.stop_running = False
        self.meter.configure(amountused=int(0))

        # Atualiza os parâmetros
        self.update_parameters()

        best_fitness_values = []
        best_schedules = []
        
        # Inicializa operadores e ordens.
        operators, orders = self.create_initial_data()
        
        # Gera populaçao inicial com base nos operadores e ordens iniciais.
        population = [ga.create_initial_solution(operators, orders, self.max_days) 
                        for _ in range(1, self.population_size+1)]

        # Loop do calculo de gerações.
        for generation in range(1, self.generation_max + 1):
            if self.stop_running:
                print("Parada prematura detectada!")
                break

            # Atualiza a geração no label do meter.
            self.update_generation_value(generation)

            # population = sorted(population, key=calculate_fitness).
            population = sorted(population, reverse=True, key=lambda individual: 
                                cf.calculate_fitness(individual, operators, orders, self.max_days))

            # Exibição da aptidão da melhor solução da geração.
            best_fitness = population[0]["fitness"]
            best_schedule = population[0] 
            best_fitness_values.append(best_fitness)
            best_schedules.append(best_schedule)

            # Atualiza o valor do meter com o melhor fitness
            self.meter.configure(amountused=int(best_fitness))

            # Atualiza a interface gráfica
            self.update_idletasks()
            self.update()

            # Geração da nova população.
            new_population = [population[0]]    # Preserva o melhor indivíduo (elitismo)
            population_limited = self.elitism_size if self.population_size >= self.elitism_size else self.population_size
            while len(new_population) < self.population_size:
                parent1, parent2 = random.choices(population[:population_limited], k=2)
                child = ga.crossover(parent1, parent2, operators, orders, self.max_days)
                child = ga.mutate(child, operators, orders, self.mutation_rate, self.max_days)
                new_population.append(child)

            # Reinicialização da população a cada 'reinitalize_interval' gerações.
            # Esta função aumenta a variabilidade na população, trocando a metade da populaçao com menor fit.
            new_population = sorted(new_population, reverse=True,
                                    key=lambda individual: individual["fitness"])
            
            if generation % self.reinitiation_point == 0:
                num_to_reinitialize = self.population_size // 2
                new_population[-num_to_reinitialize:] = [
                    ga.create_initial_solution(operators, orders, self.max_days) 
                    for _ in range(num_to_reinitialize)]
                    
                
                # Recalcula o fitness da nova populaçao
                for individual in new_population[-num_to_reinitialize:]:
                    individual["fitness"] = cf.calculate_fitness(individual, operators, orders, self.max_days)
            
            population = new_population

        # Encontrando a melhor solução com base no fitness.
        best_solution = max(best_schedules, key=lambda individual: individual["fitness"])
        
        # Atualiza a tabela de resultados.
        self.update_tables_with_solution(best_solution)

        # Mensagem de termino da execução do algoritmo.
        self.toast_msg("A execução do algoritmo terminou!")

        # Troca a aba ativa para ver os resultados.
        self.right_panel_general.select(self.right_panel_general.tabs()[1])
        

#############################################################

    # Algoritmo principal da classe.    
    def __init__(self, *args, **kwargs):
    
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

        # Inicialização da classe
        self.params = {
            "_N_ORDERS" : 100,
            "_N_OPERATORS" : 10,
            "_POPULATION_SIZE" : 50,
            "_GENERATIONS" : 50,
            "_MUTATION_RATE" : 0.3,
            "_ELITISM_SIZE" : 5,
            "_REINITIALIZE_INTERVAL" : 10,
            "_DAYS": 5,  
        }
        
        self.renamed_params = {
            "_N_ORDERS": "Nº de OS",
            "_N_OPERATORS": "Nº de Operadores",
            "_POPULATION_SIZE": "Tam. População",
            "_GENERATIONS": "Gerações",
            "_MUTATION_RATE": "Taxa mutação %",
            "_ELITISM_SIZE": "Elitismo",
            "_REINITIALIZE_INTERVAL": "Reinicialização",
            "_DAYS": "Dias",
        }

        self.max_params = {
            "_N_ORDERS": 500,
            "_N_OPERATORS": 500,
            "_POPULATION_SIZE": 200,
            "_GENERATIONS": 1000,
            "_MUTATION_RATE": 100,
            "_ELITISM_SIZE": 50,
            "_REINITIALIZE_INTERVAL": 100,
            "_DAYS": 31,
        }

        # --- ordenaçao dos paineis ---
        self.top_bar_buttons()
        self.parameters_panel()
        self.right_panel_show()
                

#############################################################

# Roda o algoritmo diretamente no arquivo
if __name__ == '__main__':    
    # Cria janela principal
    app = cria_janela()
    OrganizadorOS(app)
    app.mainloop()

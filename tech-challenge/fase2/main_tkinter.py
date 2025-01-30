# Imports para o funcionamento da interface tkinter
from functions.tkinter_interface import *

# TODO Colocar no streamlit, executar e print o DF (pandas) no final.

# Loop principal.
if __name__ == '__main__':
    """
        Seleciona a interface a ser executada: 
        Args:   "tkinter_interface"
    """

    # Seleciona a interface a ser usada.
    # selected_interface

    # Cria a janela principal da interface.
    app = cria_janela()

    # Executa a classe referente ao organizador.
    OrganizadorOS(app)

    # Executa o loop principal
    app.mainloop()
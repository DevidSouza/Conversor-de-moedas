from tkinter.ttk import Combobox
from tkinter import ttk
from tkinter import *
import requests
import json
from tkinter import messagebox

azul = '#225077'
preto = '#050505'
branco = '#f9f9f9'
cinza = '#4f4a48'

jan = Tk()
jan.title('')
jan.geometry('330x380')
jan.resizable(width=False, height=False)

estilo = ttk.Style(jan)
estilo.theme_use('alt')

# carregando imagem
imagem = PhotoImage(file='imagens/conversor.png')
frame_cima = Frame(jan, width=330, height=70, bg=azul)
frame_cima.grid(row=0, column=0)

# exibindo ícone
jan.iconphoto(False, PhotoImage(file='imagens/conversor_moeda.png'))

#exibindo imagem
exibe_imagem = Label(frame_cima, image=imagem, bg=azul)
exibe_imagem.place(x=5, y=10)

titulo = Label(frame_cima, text='Conversor de Moedas', width=17, height=1, bg=azul, fg=preto, font=('BodoniMT 19 bold'))
titulo.place(x=60, y=20)

frame_exibe_valor = Frame(jan, width=330, height=82)
frame_exibe_valor.grid(row=1, column=0)

valor_convertido = StringVar()
valor_convertido.set('0,00')

# criando função converter
def converter():
    valor_que_e_convertido, valor_que_converte, simbolos_das_moedas = 0, 0, {}

    moeda_que_e_convertida = combobox1.get().upper()
    moeda_que_converte = combobox2.get().upper()

    while True:
        moedas = ['BRL', 'USD', 'AUD', 'CAD', 'EUR', 'ARS']
        if moeda_que_e_convertida not in moedas or moeda_que_converte not in moedas:
            messagebox.showerror('Erro', 'Você precisa digitar uma moeda válida!')
            break

        # definindo o simbolo do valor resultante da conversão
        simbolos_das_moedas = {'BRL': 'R$', 'USD': '$', 'AUD': '$', 'CAD': '$', 'EUR': '€', 'ARS': '$'}
        for moe, sim in simbolos_das_moedas.items():
            if moe == moeda_que_converte:
                simbolo = sim

        # requisitando e formatando api da cotação
        link_api_cotacao = f'https://api.exchangerate-api.com/v4/latest/{moeda_que_e_convertida.upper()}'
        obtem_cotacao = requests.get(link_api_cotacao)
        formata_cotacao = json.loads(obtem_cotacao.text)
        formata_cotacao = formata_cotacao['rates']

        try:
            valor_que_converte = float(formata_cotacao[moeda_que_converte])
            valor_que_e_convertido = float(entry_recebe_valor.get())
        except ValueError:
            messagebox.showerror('Erro', 'Você precisa digitar um valor numérico!')
            break

        valor_convertido.set(f'{simbolo} {valor_que_e_convertido*valor_que_converte:.2f}'.replace('.', ','))

        cotacao = f'1 {moeda_que_e_convertida} equivale à {valor_que_converte} {moeda_que_converte}'.replace('.', ',')
        exibe_valor_da_cotacao['text'] = cotacao
        break


exibe_valor = Label(frame_exibe_valor, textvariable=valor_convertido, width=15, height=2, bg=branco, fg=preto, font=('Times 19 bold'), relief=SOLID)
exibe_valor.place(x=48, y=15)

frame_baixo = Frame(jan, width=330, height=229)
frame_baixo.grid(row=2, column=0)

label_texto1 = Label(frame_baixo, text='De', width=5, height=1, fg=cinza, font=('Arialblack 11 bold'))
label_texto1.place(x=30, y=10)

label_texto2 = Label(frame_baixo, text='Para', width=5, height=1, fg=cinza, font=('Arialblack 11 bold'))
label_texto2.place(x=170, y=10)

cotacao = ''

exibe_valor_da_cotacao = Label(frame_baixo, text=cotacao, width=22, height=1, font=('Ivy 10'), fg=preto)
exibe_valor_da_cotacao.place(x=60, y=145)

combobox1 = ttk.Combobox(frame_baixo, width=10, justify='center', font=('Arial 0 bold'))
combobox1['values'] = ('BRL', 'USD', 'AUD', 'CAD', 'EUR', 'ARS')
combobox1.current(1)
combobox1.place(x=40, y=40)

combobox2 = ttk.Combobox(frame_baixo, width=10, justify='center', font=('Arial 0 bold'))
combobox2['values'] = ('BRL', 'USD', 'AUD', 'CAD', 'EUR', 'ARS')
combobox2.current(0)
combobox2.place(x=172, y=40)

valor_padrao_inserido = StringVar()

entry_recebe_valor = ttk.Entry(frame_baixo, width=18, textvariable=valor_padrao_inserido, justify='center', font=('Times 18'))
entry_recebe_valor.place(x=50, y=95)

botao_converter = Button(frame_baixo, text='Converter', command=converter, font=('Arial 0 bold'), pady=4, width=25, height=1, fg=preto, bg=azul, relief=RAISED, overrelief=RIDGE)
botao_converter.place(x=35, y=180)

jan.mainloop()

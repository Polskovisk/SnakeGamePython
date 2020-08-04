# Gamezin criado apenas for fun, infelizmente hardcoded, então para mudar o tamanho da tela e etc tem que mudar varias coisinhas :)\
# Mentira, é facil, poderia fazer de um jeito que o player escolha o tamanho? Sim. Vou fazer? Não. FODASE
from tkinter import *
import random
import datetime

#Constantes globais e uma variavel, fodase
MoveSpeed = 15
GAMESPEED = 1000 // MoveSpeed
DEBUG = False

#Presente para quem passar de 50 no movespeed
ART = """ 
   |\---/|
   | ,_, |
    \_`_/-..----.
 ___/ `   ' ,""+ \  sk
(__...'   __\    |`.___.';
  (_,...'(_,.`__)/'.....+
  """

class Snake(Canvas):
    def __init__(self):
        super().__init__(width=600, height=700, background='black', highlightthickness=0)

        self.difficulty = 'Normal'
        self.SpeedChangeBool = False
        self.SnakeSpeed = 15
        self.Time = 0
        self.desc = 'Normal: walls dont kill and speed dont change.'

        self.ColorSnake = 'Green'
        self.FruitColor = 'Red'
        self.TimePosition = (300, 20)
        self.ScorePosition = (self.TimePosition[0]-220, self.TimePosition[1])
        self.SpeedPosition = (self.TimePosition[0]+200, self.TimePosition[1])


        self.menu()
        self.time()


    def menu(self):
        # Criação do menu, textos e tags :)
        self.create_text(
            300, 250, text='Snake Game', tags='start_title', fill='#fff', font=('Courier', 18, 'underline'))

        start = Button(self, text='Start', command=self.init_game)
        self.difficultB = Button(
            self, text=f'Difficulty: {self.difficulty}', command=self.difficult_update)
        start.configure(width=10, activebackground='#fff',
                        font=('Courier', 10), bd=0)
        self.difficultB.configure(
            width=25, activebackground='#fff', font=('Courier', 10), bd=0)

        self.create_rectangle(580, 680, 20, 20, outline='white')

        self.create_window(300, 300, window=start)
        self.create_window(300, 330, window=self.difficultB)

        self.create_text(
        300, 400, text=self.desc, tags='desc', fill='green', font=('Courier', 10))

    def init_game(self):
        global MoveSpeed, GAMESPEED
        MoveSpeed = 15
        #Velocidade do game dividia pela movespeed global, começando com 66.6 e indo diminuindo (Na maior dificuldade).
        GAMESPEED = 1000 // MoveSpeed
        #Deleta tudo, função para quando for dar o restart no game :)
        self.delete(ALL)

        # Posição de cada parte do corpo no canvas, X, Y, (15 é o tamanho, toda interação o segundo valor tem que adicionar ou subtrair 15)
        self.snake_body = [(300, 300), (285, 300), (270, 300)]
        # Bind nas teclas para jogar
        self.bind_all('<Key>', self.snake_direction)
        # Primeira posição da comida, sendo ela random.
        self.food_respawn()

        # Placar, Tick, Tempo e Velocidade
        self.Score = 0
        self.Time = 0
        self.TimeConverted = ''
        self.SpeedVariable = ''
        self.Tick = True

        # Primeira direção já definida.
        self.direction = "Right"

        self.SpeedChange()
        self.init_draw()
        self.after(GAMESPEED, self.loop)

    def difficult_update(self):
        #Dificuldades feitas do jeito mais bosta possivel, mas ta suave :)
        if (self.difficulty == 'Normal'):
            self.difficulty = 'Hard'
            self.desc = 'Hard: walls kill but speed dont change'
            self.itemconfigure(self.find_withtag('desc'),
                           text=self.desc, fill='yellow')
        elif (self.difficulty == 'Hard'):
            self.difficulty = 'Demon Hands'
            self.desc = 'God bless you, i think you cant pass 50 speed :)'
            self.itemconfigure(self.find_withtag(
                'desc'), text=self.desc, fill='red')
            self.SpeedChangeBool = True
        else:
            self.difficulty = 'Normal'
            self.desc = 'Normal: walls dont kill and speed dont change.'
            self.itemconfigure(self.find_withtag(
                'desc'), text=self.desc, fill='green')

        self.difficultB.configure(text=f'Difficulty: {self.difficulty}')

    def init_draw(self):
        #Faz o desenho inicial.
        global DEBUG
        # Cria o corpo da cobra, Posx_1, Posy_1, Posx_2, Posy_2.
        for x in self.snake_body:
            self.create_rectangle(x[0], x[1], x[0]+15, x[1]+15,
                                  fill='green', outline='black', tags='snake')

        # Criação da primeira frutinha no game.
        self.create_rectangle(self.food[0], self.food[1], self.food[0]+15,
                              self.food[1]+15, fill='red', outline='black', tags='food')

        # Criação do texto de Score
        self.create_text(self.ScorePosition, text=f'Score: {self.Score}', tags='score', fill='#fff', font=('Courier', 14))

        # Criação do texto de Tempo
        self.create_text(
            self.TimePosition, text=f'Time: {self.TimeConverted}', tags='time', fill='#fff', font=('Courier', 14))

        # Criação do texto de Speed
        self.create_text(
            self.SpeedPosition, text=f'Speed: {MoveSpeed}', tags='speed', fill='#fff', font=('Courier', 14))
        
        #Criação do texto informativo do ganho de velocidade
        self.create_text(
            self.SpeedPosition[0]-200, self.SpeedPosition[1]+40, text=f'Speed Gain: {self.SpeedVariable} for each 5 points.', tags='speedgain', fill='#fff', font=('Courier', 10))

        #Divisão da tela
        self.create_line(0,90,self.winfo_width(), 90, fill='white')

        #Informa que o ganho de velocidade esta desligado se não estiver na dificuldade correta.
        if self.difficulty != 'Demon Hands':
            self.itemconfigure(self.find_withtag(
                'speedgain'), text=f'Speed gain is enable only in "Demon Hands" mode')

        #Modo DEBUG, coloca um texto na tela informando posição da cobra (cabeça) e da comida.
        if DEBUG:
            self.create_text(300, 685, text=f'Snake: {self.snake_body[0]}, Food: {self.food}', tags='debug', fill='#fff', font=('Courier', 14))
            self.DebugText()

    #Texto do Debug sendo atualizado a cada segundo.
    def DebugText(self):
        self.itemconfigure(self.find_withtag(
            'debug'), text=f'Snake: {self.snake_body[0]}, Food: {self.food}, Speed: {GAMESPEED}')
        self.after(GAMESPEED, self.DebugText)

    #Randomizador de ganho de velocidade + texto :)
    def SpeedChange(self):
        if self.SpeedChangeBool:
            self.speed = random.randint(1,5)
            self.SpeedVariable = f'(+{self.speed})'
        else:
            self.SpeedVariable = ''

    #Relogio fodase
    def time(self):
        self.Time += 1
        self.TimeConverted = str(datetime.timedelta(seconds=self.Time))
        self.itemconfigure(self.find_withtag('time'),
                           text=f'Time: {self.TimeConverted}')
        
        self.after(1000, self.time)

    #Movimento da cobra
    def move_snake(self):
        #Primeira definição de variavel, pega pos da cabeça.
        head_x_pos, head_y_pos = self.snake_body[0]

        #Checka qual a ultima tecla apertada e executa o movimento, clamp esta ai para o game normal, deste modo ao bater na parede ela vai para o outro lado ou morre
        if self.direction == 'Left':
            new_head_pos = (clamp(head_x_pos - self.SnakeSpeed, 0, 600), 
                            clamp(head_y_pos, 90, 690))
        elif self.direction == 'Right':
            new_head_pos = (clamp(head_x_pos + self.SnakeSpeed, 0, 600),
                            clamp(head_y_pos, 90, 690))
        elif self.direction == 'Up':
            new_head_pos = (clamp(head_x_pos, 0, 585),
                            clamp(head_y_pos - self.SnakeSpeed, 90, 690))
        elif self.direction == 'Down':
            new_head_pos = (clamp(head_x_pos, 0, 585),
                            clamp(head_y_pos + self.SnakeSpeed, 90, 690))

        # Adiciona uma nova cabeça com um novo valor e remove a ultima parte da array do corpo, fazendo com que ela se "mova"
        self.snake_body = [new_head_pos] + self.snake_body[:-1]


        # Atualiza as cordenadas do corpo, sem isso a tela não atualiza
        for i, position in zip(self.find_withtag('snake'), self.snake_body):
            self.coords(i, position[0], position[1],
                        position[0]+15, position[1]+15)

    #Yey Checks
    def check_food(self):
        # Check para ver se a posição da cabeça da cobra é a mesma da comida, adiciona mais um corpo a cobra e aumenta o score em 1
        if self.snake_body[0] == self.food:
            self.food_respawn()

            # Adiciona 1 ao score e atualiza o placar
            self.Score += 1
            self.itemconfigure(self.find_withtag('score'),
                               text=f'Score: {self.Score}')

            #Na maior dificuldade vê se o resto da divisão do score (por 5), se for 0 executa o codigo abaixo, caso contrario vida que segue
            if self.Score % 5 == 0 and self.difficulty == 'Demon Hands':
                global MoveSpeed, GAMESPEED
                #Atualiza a velocidade da cobra pelo modificador random adquirido
                MoveSpeed += self.speed
                GAMESPEED = 1000 // MoveSpeed
                self.itemconfigure(self.find_withtag(
                    'speed'), text=f'Speed: {MoveSpeed}')

                #Adquire um novo valor.
                self.SpeedChange()
                #Informa o valor.
                self.itemconfigure(self.find_withtag(
                    'speedgain'), text=f'Speed Gain: {self.SpeedVariable} for each 5 points.')

            # Pega a ultima parte da cobra e a repete, adiciona e cria o retangulo
            tail_x_pos, tail_y_pos = self.snake_body[-1]
            self.snake_body.append(self.snake_body[-1])
            self.create_rectangle(tail_x_pos, tail_y_pos, tail_x_pos+15, tail_y_pos+15,
                                  fill='green', outline='black', tags='snake')

    def check_collision(self):
        # Check para ver se a posição da cabeça da cobra é a mesma do corpo, retorna true
        head_x_pos, head_y_pos = self.snake_body[0]

        #Se for o modo normal a check da parede retorna false e apenas do corpo é contada.
        if (self.difficulty != 'Normal'):
           HardCollision = head_x_pos in (0,600) or head_y_pos in (90, 685)
        else:
            HardCollision = False

        return (
            HardCollision or (head_x_pos, head_y_pos) in self.snake_body[1:]
        )

    def snake_direction(self, event):
        # Check de direção, evita usar direções opostas e passa a direção para frente caso não tenha problema.
        # Tudo que era preciso era um check de tick para evitar o player floodar as teclas.
        if self.Tick:
            # Desliga o tick para receber o proximo movimento
            self.Tick = False

            # Originalmente eu tinha feito com o codigo das teclas deixando mais simples, porém até implementar o tick mudei para esse. Fica esse por preguiça
            directions = ('Up', 'Down', 'Left', 'Right')
            direction_negate = ({"Left", "Right"}, {"Up", "Down"})

            # Se não existir a tecla o programa manda fodase para o que vc apertou
            if (event.keysym not in directions):
                return

            # Se a direção apertada não for contraria a que você esta indo a direção é atualizada.
            if {event.keysym, self.direction} not in direction_negate:
                self.direction = event.keysym

    def food_respawn(self):
        # Verifica se a posição da comida não é a mesma de alguma parte do corpo da cobra, caso contrario ira continuar o loop até encontrar uma posição valida.
        global MoveSpeed
        while True:
            # O spawn da comida esta limitada a um certo espaço, diminui o espaço para evitar aparecer nas bordas
            # Se o jogo continuar por muito tempo (improvavel) a pessoa tera que usar os cantos para que a comida spawne em alguma posição possivel.
            self.food = (random.randint(8, 37)*self.SnakeSpeed, random.randint(8, 45)*self.SnakeSpeed)

            if self.food not in self.snake_body:
                self.coords(self.find_withtag(
                    'food'), self.food[0], self.food[1], self.food[0]+15, self.food[1]+15)
                return

    #Tela final yey
    def end_screen(self):
        global MoveSpeed
        #Primeiramente limpamos o canvas.
        self.delete(ALL)

        #Textos, Game Over, Pontuação, Velocidade atingida (Se estivar na dificuldade correta.)
        self.create_text(300, 250, text='Game Over', font=('Courier', 20, 'underline'), fill='#fff')
        self.create_text(300, 300, text=f'You scored: {self.Score}', font=('Courier', 18, 'underline'), fill='#fff')
        if self.difficulty == 'Demon Hands':
            self.create_text(300, 340, text=f'Your speed: {MoveSpeed}', font=(
                'Courier', 14), fill='red')

        #Botões de start e menu :)
        restart = Button(self, text='Restart', command=self.init_game)
        menu = Button(self, text='Menu', command=self.restart_menu)

        restart.configure(width=10, activebackground='#fff', font=('Courier', 10), bd=0)
        menu.configure(width=10, activebackground='#fff',
                          font=('Courier', 10), bd=0)

        self.create_window(350, 380, window=restart)
        self.create_window(240, 380, window=menu)

        #Presente caso a pessoa passe de 50 de velocidade. Tem que passar de 50 >:(
        if MoveSpeed > 50:
            self.create_text(300, 450, text='Okay, i was wrong, take this as a prize.', font=(
                'Courier', 10), fill='#fff')
            self.create_text(300, 550, text=ART, fill='white', justify=LEFT, font=('Courier', 14))

    # Apenas a função de restart
    def restart_menu(self):
        self.delete(ALL)
        self.menu()
    
    #Famoso loop
    def loop(self):
        # Check de collision logo após mover a cobra.
        if self.check_collision():
            self.end_screen()
            return

        # Seta o Tick do game para true, evita multiplos comandos do teclado de uma vez só fazendo o codigo bugar e a cobra morrer.
        self.Tick = True

        #Vê se a cobra comeu a comidinha e dps executa o movimento
        self.check_food()
        self.move_snake()

        self.after(GAMESPEED, self.loop)


# Clamp, retorna o minimo quando no maximo, o maximo quando no minimo, caso contrario mantem o valor. (Se pa nem se chama clamp mas posso chamar de rogerio se eu quiser fodase)
def clamp(n, minn, maxn):
    if n > maxn:
        return minn
    elif n < minn:
        return maxn
    else:
        return n


# Cria a aplicação
root = Tk()
root.title('Snake')
root.resizable(False, False)

# Adiciona o canvas a aplicação
board = Snake()
board.pack()

root.mainloop()
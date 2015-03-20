# -*- coding: utf-8 -*-
"""
Projeto base para Exercício Programa de Software Design
@author: mirwox
@author: lpsoares
"""
#  Usa trechos adaptados  do tutorial DrawingDemoQt.py  de  Kari Laitinen
#   disponível em http://www.naturalprogramming.com/pythonqt/DrawingDemoQt.py
#  Função drawSquares tirada de http://zetcode.com/gui/pyqt4/thetetrisgame/ 
import sys
import types
import os
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Variáveis globais

# Imagens do fundo e do tanque
background = None 
tank = None 

# Coordenadas do tanque
tankX = 100
tankY = 100
deltaTank = 3 #Incremento do movimento do tanque
# Coordenadas da bola
ballX = 0
ballY = 0
# Contador de tempo do jogo
t = 0
# Timer
timer = None
# Janela principal do jogo
window = None
# Largura e altura dos quadrados do piso
sqHeight = 36
sqWidth = 36
# Nome do jogador
playerName = ""
# De quanto em quanto tempo pede para o jogador de deseja mudar a velocidade
promptInterval = 35

# Função que lê imagem de um arquivo e devolve um variável do tipo imagem
def readImage(filename):
    imagem = QImage()
    isloaded = imagem.load(filename)
    print("Imagem %s lida: %d, tamanho %d x %dn"%(filename, isloaded, imagem.width(), imagem.height()))
    return QImage(filename)

# Inicialização da janela do jogo. Executado no começo
def init(window):
    global tank
    global background
    # Faz a leitura dos arquivos
    background = readImage('./background.png') # Fonte: OpenGameArt.org http://tinyurl.com/lduon52
    tank = readImage('./metalslug.png') # Fonte: Game Sprite Archive - SNK Playmore
    # Definição da posição 100,100 no desktop e do tamanho 768 x 432 da janela
    window.setGeometry(100, 100, 768, 432)
    window.setWindowTitle("Base projeto")  
    # Informa à janela que a função paint faz o redesenho da tela
    window.paintEvent = types.MethodType(paint, window) 
    window.show()    

def drawSquare(widget, painter, x, y, width, height, colorIndex):
    """
    Desenha um único quadrado com bordas
    Retirado do exemplo TetrisQt4 usado na 1.a aula
    
    """
    # Cores a serem usadas    
    colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                  0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

    # QColor cria uma cor com base no RGB passado
    color = QColor(colorTable[colorIndex%len(colorTable)])
    
    painter.fillRect(x + 1, y + 1, width - 2, 
        height - 2, color)

    painter.setPen(color.light())
    painter.drawLine(x, y + height - 1, x, y)
    painter.drawLine(x, y, x + width - 1, y)

    painter.setPen(color.dark())
    painter.drawLine(x + 1, y + height - 1,
        x + width - 1, y + height - 1)
    painter.drawLine(x + width - 1, 
        y + height - 1, x + width - 1, y + 1)


def drawSquares(numberRows, painter):
    """
        Desenha os diversos quadradinhos que compõem o piso
        A quantidade na horizontal é o tamanho da tela / largura do quadrado
        A quantidade na vertical é numberRows
    """
    colorIndex = 0
    numberRows = 4
    h = window.height() 
    w = window.width()
    for x in range(0, w, w//sqWidth):
        colorIndex+=1
        for y in range(h - numberRows*sqHeight, h, sqHeight):
            drawSquare(window, painter, x, y, sqWidth, sqHeight, colorIndex )    

def drawTank(painter, numberRows):
    """
     Desenha a imagem do tanque           
    """
    tankY =  window.height() - numberRows*sqHeight - tank.height()  
    painter.drawImage(tankX, tankY,tank)     

def mixedDrawings(painter):
    """Desenhos sem um objetivo específico,
       apenas para demonstrar o que o painter da PyQt faz
    """    
    if playerName== "":
        painter.drawText( 20, 20, "Window size is %dx%d "  %  \
                                    ( window.width(), window.height() ) )      
    else:
        painter.drawText( 20, 20, ("Olá "+playerName+"!!") )
                                    
    # Desenha uma linha na diagonal da tela                                          
    painter.drawLine( 0, 0,
                window.width(), window.height() ) ;
    
    
    #  drawRect Desenha retângulo com a pen atual e a preenche com a brush que estiver ativa    
    painter.drawRect( 10, 190, 120, 100 )

    # Desenha um polígono
    painter.drawPolygon( QPoint( 400, 150 ), QPoint( 450, 180 ),
                           QPoint( 450, 220 ), QPoint( 400, 250 ),
                           QPoint( 350, 220 ), QPoint( 350, 180 ) )
                           
def paint(window, event):
    """
        Código que desenha toda a lógica do jogo
        Altere variáveis e coloque a lógica na função gameLoop\
        Aqui deve ir somente código gráfico / de desenho na tela
    """
    painter = QPainter()
    painter.begin(window)
          
    # Brush é a cor de recheio, Pen é a cor da borda
    painter.setBrush( Qt.green )
    painter.setPen(Qt.red)

    # Desenha a imagem do fundo    
    painter.drawImage(0,0, background)  
    font = QFont("Arial", pointSize=28, weight = QFont.Bold)
    painter.setFont(font)         
    
    # Faz alguns desenhos a título de exemplo
    mixedDrawings(painter)
       
    # Quantas linhas de retângulos serão desenhados
    numberRows = 4
    
    drawSquares(numberRows, painter)
    drawTank(painter, numberRows)
 
    orange = QColor("#ffc600") # Como criar uma cor dado o valor RGB
    orangeBrush = QBrush(orange)  # Brush é usado para preencher
    orangePen = QPen(orange)      # Pen é usado para o contorno

    # Escreve "Design de software no fundo", escreve 2x para dar
    # efeito sombreado
    if t%10 > 5: # 5 instantes sim, 5 instantes não. Faz piscar
        font = QFont("Arial", pointSize=40, weight = QFont.Bold)
        painter.setPen(Qt.black)
        painter.drawText( 352, 352, "Design de Software" )   
        painter.setPen(orangePen)
        painter.drawText( 350, 350, "Design de Software" )             

    # Desenha a bola cadente 
    painter.setPen(Qt.blue)
    painter.setBrush(orangeBrush)
    painter.drawEllipse(ballX, ballY, 40,40)
    painter.end()  


def gameLoop():
    """
        Loop principal do programa
    """
    global t 
    global tankX
    global ballX
    global ballY
    global playerName
    global deltaTank
    
    # Define a posição inicial de ballX
    if t == 0:
        ballX = window.width()/2  
        
    # Pergunta o nome do usuário     
    if playerName == "":
        name, ok = QInputDialog.getText(window, 'Input Dialog', 'Qual é seu nome?')
        if ok: # ok significa que o usuário digitou algo
            playerName = name    

    # Movimenta o tanque na horizontal
    tankX = tankX + deltaTank
    
    # Trunca tankX e ballY para que não saiam da tela
    tankX = tankX % window.width()
    ballY = ballY + 6
    ballY = ballY % window.height()
    
    # Pergunta a cada promptInterval repetições se o usuário deseja
    # Inverter o tanque
    if t%promptInterval == 0:
        answer, ok = QInputDialog.getInteger(window, 'Tank command', 'Inverter o Tanque?(1) Sim e (-1) Não')
        if ok:
            if answer==1:
                deltaTank*=-1  
    t +=1 #Contador global de tempo, pode ser útil                    
    window.update() # Faz window se desenhar novamente

#  Ponto inicial do programa
def main( args ) :
   print("Suas imagens devem estar no diretório de trabalho:\n", os.getcwd())        
   this_application = QApplication( args ) # Cria uma aplicacao gráfica
   global window
   window = QWidget() # Cria uma janela gráfica
   init(window)
   
   global timer #Avisa ao Python que vamos usar a variável timer declarada no escopo global
   timer = QTimer() # Cria um timer
   timer.timeout.connect(gameLoop) # timer vai chamar a função gameloop repetidamente   
   frameDelay = 100 # Tempo que um frame leva em ms
   timer.start(frameDelay) # Iniciar o timer com base no tempo frameDelay
   this_application.exec_()

# Se este arquivo estiver sendo executado, chama a função main  
if __name__== "__main__" :
   main( sys.argv )
import tkinter as tk
import math
from A_star_player import AStarPlayer

class HexBoard:

    def __init__(self, size: int, board):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = board # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
        self.player_positions = {1: set(), 2: set()}  # Registro de fichas por jugador

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        """Coloca una ficha si la casilla está vacía."""
        if player_id == 0 or self.board[row][col] == 0: 
            self.board[row][col] = player_id
            return True
        
        return False
    
    def Print(self):
        for i in range(self.size): #fila
            print(" " * i, end="")
            for j in range(self.size): #columna (iterate over all columns)
                print(self.board[i][j], end=" ")
            print()
            



    def get_possible_moves(self) -> list:
        """Optimiza la generación de movimientos posibles."""
        possible_moves = set()
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)  # Direcciones en un tablero hexagonal
        ]

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] in (1, 2):  # Si la casilla pertenece a un jugador
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == 0:
                            possible_moves.add((nr, nc))
        return list(possible_moves)

    def check_connection(self, player_id: int) -> bool:
        """Verifica si el jugador ha conectado sus dos lados."""
        visited = set()
        target_row = self.size - 1 if player_id == 1 else None
        target_col = self.size - 1 if player_id == 2 else None

        def dfs(row, col):
            if (row, col) in visited:
                return False
            visited.add((row, col))

            if player_id == 1 and row == target_row:
                return True
            if player_id == 2 and col == target_col:
                return True

            directions = [
                (-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)
            ]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player_id:
                    if dfs(nr, nc):
                        return True
            return False

        if player_id == 1:
            for col in range(self.size):
                if self.board[0][col] == player_id and dfs(0, col):
                    return True
        elif player_id == 2:
            for row in range(self.size):
                if self.board[row][0] == player_id and dfs(row, 0):
                    return True

        return False
    
    def longest_path(self, x: int, y: int, player: int) -> tuple[int, tuple[int, int]]:
        directions = [
            (1, 0),
            (1, -1),
            
        ]
        
        for direction in directions:
            if x + direction[0] < self.size and\
                x + direction[0] >= 0 and \
                y + direction[1] >= 0 and \
                y + direction[1] < self.size \
                and self.board[x + direction[0]][y + direction[1]] == player and player == 1: 
                    return  1 + self.longest_path( x +direction[0], y + direction[1], player )[0], self.longest_path(x + direction[0], y + direction[1], player )[1]
            elif x + direction[1] < self.size and\
                x + direction[1] >= 0 and\
                y + direction[0]>= 0 and \
                y + direction[0]< self.size \
                and self.board[x + direction[1]][y + direction[0]] == player and player == 2:
                    return  1 + self.longest_path(x +direction[1], y + direction[0], player )[0], self.longest_path(x + direction[1], y + direction[0], player )[1]
        return 0, (x,y)

    def get_longest_path(self):
        
        max_len1 = 0
        X1min = -1
        y1min = -1
        
        X1max = -1
        y1max = -1
        
        max_len2 = 0        
        X2min = -1
        y2min = -1
        
        X2max = -1
        y2max = -1
        
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]== 1:
                    longest, coordenada = self.longest_path(i, j, 1)
                    if longest >= max_len1:
                        max_len1 = longest
                        X1min = i
                        y1min = j
                        X1max = coordenada[0]
                        y1max = coordenada [1]
                if self.board[j][i]== 2:
                    longest, coordenada = self.longest_path(j, i, 2)
                    if longest >= max_len2:
                        max_len2 = longest
                        X2min = j
                        y2min = i
                        X2max = coordenada[0]
                        y2max = coordenada [1]
        
        if max_len1 == self.size - 1: 
            max_len1 = float('inf')
            return max_len1, max_len2
        if max_len2 == self.size - 1: 
            max_len2 = float('inf')
            return max_len1, max_len2

        max_len1 = max_len1^2
        max_len2 = max_len2^2
        
        if X1min - 1 >= 0 :
            if self.board[X1min - 1][y1min] == 0:
                max_len1 = max_len1 + 1
                max_len1 = max_len1 + 2 if  X1min - 2 >= 0 and y1min + 1 < self.size and  self.board[X1min - 2][y1min] == 0 and  self.board[X1min - 2][y1min + 1] == 0 else max_len1
            if y1min + 1 < self.size and self.board[X1min - 1][y1min + 1] == 0:
                max_len1 = max_len1 + 1
                max_len1 = max_len1 + 2 if  X1min - 2 >= 0 and y1min +2 < self.size and  self.board[X1min - 2][y1min + 1] == 0 and  self.board[X1min - 2][y1min + 2] == 0 else max_len1
        
        if X1max + 1 < self.size :
            if self.board[X1max + 1][y1max] == 0:
                max_len1 = max_len1 + 1
                max_len1 = max_len1 + 2 if  X1max + 2 < self.size and y1max - 1 < self.size and  self.board[X1max + 2][y1max] == 0 and  self.board[X1max +2][y1max - 1] == 0 else max_len1
            if y1max - 1 >= 0 and self.board[X1max + 1][y1max - 1] == 0:
                max_len1 = max_len1 + 1
                max_len1 = max_len1 + 2 if  X1max + 2 < self.size and y1max - 2 >= 0 and  self.board[X1max + 2][y1max - 1] == 0 and  self.board[X1max + 2][y1max - 2] == 0 else max_len1
        
        
        #######
        if y2min - 1 >= 0 :
            if self.board[X1min][y1min - 1] == 0:
                max_len2 = max_len2 + 1
                max_len2 = max_len2 + 2 if  y2min - 2 >= 0 and X2min + 1 < self.size and  self.board[X2min][y2min - 2] == 0 and  self.board[X2min + 1][y2min - 2] == 0 else max_len2
            if X2min + 1 < self.size and self.board[X2min + 1][y2min - 1] == 0:
                max_len2 = max_len2 + 1
                max_len2 = max_len2 + 2 if  y2min - 2 >= 0 and X2min +2 < self.size and  self.board[X2min+1][y2min - 2] == 0 and  self.board[X2min + 2][y2min - 2] == 0 else max_len2
        
        if y2max + 1 < self.size :
            if self.board[X2max][y2max + 1] == 0:
                max_len2 = max_len2 + 1
                max_len2 = max_len2 + 2 if  y2max + 2 < self.size and X2max - 1 >= 0 and  self.board[X2max][y2max + 2] == 0 and  self.board[X2max - 1][y2max + 2] == 0 else max_len2
            if X2max - 1 >= 0 and self.board[X2max - 1][y2max + 1] == 0:
                max_len2 = max_len2 + 1
                max_len2 = max_len2 + 2 if  X2max - 2 >= 0 and y2max + 2 < self.size and  self.board[X2max - 2][y2max + 2] == 0 and  self.board[X2max - 1][y2max + 2] == 0 else max_len2
        
        ####
        for x in range(X1max, self.size -1):
            for y in range(y1min, y1max):
                if self.board[x][y] == 2:
                    max_len2 = max_len2 + 1
                    break
                # if self.board[x][y] == 1:
                #     max_len1 = max_len1 + 1

        for x in range(X1min - 1):
            for y in range(y1min, y1max):
                if self.board[x][y] == 2:
                    max_len2 = max_len2 + 1
                #     break
                # if self.board[x][y] == 1:
                #     max_len1 = max_len1 + 1
        
        for x in range(y2min-1):
            for y in range(X2min, X2max):
                if self.board[x][y] == 1:
                    max_len1 = max_len1 + 1
                #     break
                # if self.board[x][y] == 2:
                #     max_len2 = max_len2 + 1

        for x in range(y2max, self.size -1 ):
            for y in range(X2min, X2max):
                if self.board[x][y] == 1:
                    max_len1 = max_len1 + 1
                #     break
                # if self.board[x][y] == 2:
                #     max_len2 = max_len2 + 1

        return max_len1, max_len2

class Player:

    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")

class PlayerEveliz(Player):

    def __init__(self, player_id: int):
        super().__init__(player_id)
    
    def minimax(self, board: HexBoard, depth: int, alpha: float, beta: float, maximizing_player: bool) -> tuple:
        """
        Implementa el algoritmo Minimax con poda alfa-beta.
        :param board: El estado actual del tablero.
        :param depth: La profundidad máxima de búsqueda.
        :param alpha: El valor alfa para la poda.
        :param beta: El valor beta para la poda.
        :param maximizing_player: True si es el turno del jugador actual, False si es el turno del oponente.
        :return: Una tupla (mejor_valor, mejor_movimiento).
        """
        if depth == 0 or board.check_connection(1) or board.check_connection(2):
            return self.evaluate_board(board), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            motions =  board.get_possible_moves()
            if motions == board.size^2: return None, (board.size/2, board.size/2)
            for move in motions:
                board.place_piece(move[0], move[1], self.player_id)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.place_piece(move[0], move[1], 0)  # Deshacer movimiento
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Poda beta
            return max_eval, best_move
        else:
            min_eval = float('inf')
            opponent_id = 2 if self.player_id == 1 else 1
            for move in board.get_possible_moves():
                board.place_piece(move[0], move[1], opponent_id)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.place_piece(move[0], move[1], 0)  # Deshacer movimiento
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Poda alfa
            return min_eval, best_move

    def evaluate_board(self, board: HexBoard) -> int:

        valueX, valueY = board.get_longest_path()
        
        # print(valueY - valueX)
        
        if self.player_id == 1: return valueX - valueY/2
        else: return valueY - valueX/2

    def play(self, board: HexBoard) -> tuple:
        _, best_move = self.minimax(board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
        return best_move



def main():
    # # Configuración de la ventana principal
    # root = tk.Tk()
    # root.title("Tablero Hexagonal")

    # # Tamaño del canvas ajustado al tamaño de la pantalla
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    # canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
    # canvas.pack()

    # Crear el tablero hexagonal
    rows = 7
    cols = 7
    
    ai_player = PlayerEveliz(player_id=1)  # La máquina será el jugador 2
    board_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    hex_board = HexBoard(rows, board_matrix)
    
    ia_otra = AStarPlayer(2)
    # hex_board.place_piece(3, 3, 1)
    
    turno = 1
    while not hex_board.check_connection(1) and not hex_board.check_connection(2):
        if turno == 2:
            jugada = ai_player.play(hex_board)
            hex_board.place_piece(jugada[0], jugada[1], ai_player.player_id)
            turno = 1
            
        else:
            jugada =  ia_otra.play(hex_board)
            # jugada = tuple(map(int, input("Introduce tu jugada (fila columna): ").split()))
            hex_board.place_piece(jugada[0], jugada[1], 2)
            turno = 2
        print("\nTablero actual:")
        hex_board.Print()
    
    

if __name__ == "__main__":
    main()


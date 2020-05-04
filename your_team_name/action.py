class Action:
    def __init__(self, type, n, a, b, colour):
        self.type = type
        self.n = n
        self.a = a
        self.b = b
        self.colour = colour
        if colour == "white":
            self.enemy = "black"
        elif colour == "black":
            self.enemy = "white"

    def apply_to(self, state):
        #return a state
        def boom(current_state, coord, boomed, colour, enemy):
            new_state = {}
            new_state[colour] = [x for x in current_state[colour] if x[1:3] != coord]
            new_state[enemy] = [y for y in current_state[enemy] if y[1:3] != coord]
            boomed.append(coord)
            xmin = coord[0]-1
            if xmin < 0:
                xmin = 0
            xmax = coord[0]+2
            if xmax > 8:
                xmax = 8
            ymin = coord[1]-1
            if ymin < 0:
                ymin = 0
            ymax = coord[1]+2
            if ymax > 8:
                ymax = 8
            if len(new_state[colour]) == 0 and len(new_state[enemy]) == 0:
                return new_state
            for x in range(xmin, xmax):
                for y in range(ymin, ymax):
                    if [x,y] not in boomed:
                        for member in new_state[colour]+new_state[enemy]:
                            if member[1:3] == [x,y]:
                                new_state = boom(new_state, [x,y], boomed, colour, enemy)
                                break;

            return new_state
        def move(current_state, number, coord, f_coord, colour):
            new_state = copy.deepcopy(current_state)

            #if moving onto another white then form a stack
            white_list=[[white[1], white[2]] for white in current_state[colour]]
            if f_coord in white_list:
                for white_member in new_state[colour]:
                    if white_member[1:3] == coord:
                        #if moving all of the stack at once then remove current stack
                        if white_member[0] == number:
                            new_state[colour].remove(white_member)
                            break
                        #if moving part of the stack then remove a number from the stack
                        if white_member[0] > number:
                            white_member[0] -= number

                #then add the removed items onto existing stack at the destination
                for white_member in new_state[colour]:
                    if white_member[1:3] == f_coord:
                        white_member[0] += number
                        return new_state

            #if not moving onto any other white
            for white_member in new_state[colour]:
                if white_member[1:3] == coord:
                    #if moving all of the stack at once then just change the coord
                    if number == white_member[0]:
                        white_member[1] = f_coord[0]
                        white_member[2] = f_coord[1]
                    #if moving a part of the stack then add another stack to the destination
                    if number < white_member[0]:
                        white_member[0] -= number
                        new_state[colour] += [[number] + f_coord]

            return new_state

        if self.type == "BOOM":
            return boom(state, self.a, [], self.colour, self.enemy)
        elif self.type == "MOVE":
            return move(state, self.n, self.a, self.b)
        return state

    def return_action(self):
        if self.type == "BOOM":
            return (self.type, self.a)
        else if self.type == "MOVE":
            return (self.type, self.a, self.b)
        return None

    def is_valid_move(self, state):
        for i in self.b:
            if i<0 or i>7:
                return False
        #check if not going to black
        enemy_positions = [tuple(mem[1:3]) for mem in state[enemy]]
        if self.b in enemy_positions:
            return False
        return True

    def apply_move(self, state, a, b):
        if self.is_valid(state):
            pass

    @classmethod
    def move_from_attributes(cls, n, coord, step, direction):
        return cls("MOVE", n, coord, (coord[0]+step*direction[0], coord[1]+step*direction[1]), colour)

import sys
import argparse
import Queue
import json


class Game:
    def __init__(self, name, player_count):
        self.name = name
        self.player_count = player_count
        self.players = []

    def __repr__(self):
        return "<Game name:%s player_count:%s players:%s>" % (self.name, self.player_count, self.players)
    def __str__(self):
        return "Game %s has %s players and they are %s" %(self.name, self.player_count, self.players)

    def at_capacity(self):
        return len(self.players) == self.player_count

    def add_player(self, player):
        if not self.at_capacity():
            self.players.append(player)
            return True
        else:
            print("Game is at capacity!")
            return False

class Player:
    def __init__(self, name, rankings):
        self.name = name
        self.priorities = rankings

    def __repr__(self):
        return "<Player name:%s priorities:%s" %(self.name, self.priorities)
    def __str__(self):
        return "From str method of Player: name is %s, priorities are %s" %(self.name, self.priorities)

    def ranking(self, gameID):
        return self.priorities[gameID]

    def has_rankings(self):
        return len(self.priorities)



def main():
    parser = argparse.ArgumentParser(description="A simple tool to help you optimize your next board game night. See the README for more info!")
    parser.add_argument('-i', '--input', default='data/example.json')
    opts = parser.parse_args()

    try:
        json_object = json.load(open(opts.input))

    except IOError:
        print "Something went wrong when reading your input file. Does it exist?"

    json_games = json_object['games']
    json_players = json_object['players']

    games = {}
    for g,v in enumerate(json_games):
        games[g] = (Game(v['name'], v['count']))

    players = []
    for p, v in enumerate(json_players):
        players.append(Player(v['name'], v['rankings']))

    players_to_allocate = set(players)
    games_to_fill = set(games.keys())

    for gameID in games_to_fill:
        current_game = games[gameID]
        game_queue = Queue.PriorityQueue()
        for player in players_to_allocate:
            if player.has_rankings():
                game_queue.put((player.ranking(gameID), player))
            else:
                game_queue.put((len(games), player))
        while not current_game.at_capacity():
            scheduled_player = game_queue.get()[1]
            if current_game.add_player(scheduled_player):
                players_to_allocate.remove(scheduled_player)

    for g in games.values():
        print(g)

# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
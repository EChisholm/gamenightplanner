import Queue
import argparse
import json


class Game:
    def __init__(self, name, player_count):
        self.name = name
        self.player_count = player_count
        self.players = []

    def __repr__(self):
        return "<Game name:%s player_count:%s players:%s>" % (self.name, len(self.players), self.players)

    def __str__(self):
        return "Game %s has %s players and they are %s" % (self.name, len(self.players), self.players)

    def at_capacity(self):
        return len(self.players) == self.player_count

    def add_player(self, player):
        if not self.at_capacity():
            self.players.append(player)
            # print self
            return True
        else:
            print("Sorry %s Game %s is at capacity!") % (player, self.name)
            return False


class Player:
    def __init__(self, name, rankings, priority):
        self.name = name
        self.rankings = rankings
        self.priority = priority

    def __repr__(self):
        return "<Player name:%s priorities:%s" % (self.name, self.rankings)

    def __str__(self):
        return "From str method of Player: name is %s, rankings are %s and they have priority %s" % (
        self.name, self.rankings, self.priority)

    def ranking(self, gameID):
        return self.rankings[gameID - 1]

    def modify_priority(self, new_value):
        self.priority = self.priority + new_value

    def has_rankings(self):
        if len(self.rankings) == 0:
            return False
        else:
            return True


def main():
    parser = argparse.ArgumentParser(description="A simple tool to help you optimize your next board game night. See the README for more info!")
    parser.add_argument('-i', '--input', default='data/example.json')
    parser.add_argument('-p', '--priority', default='data/priority.json')
    opts = parser.parse_args()

    try:
        json_input = json.load(open(opts.input))
        json_priority = json.load(open(opts.priority))

    except IOError:
        print "Something went wrong when reading your input files. Do they exist?"
        raise
    json_games = json_input['games']
    json_players = json_input['players']

    games = {}
    for g, v in enumerate(json_games, start=1):
        games[g] = (Game(v['name'], v['count']))

    number_of_games = len(games)

    players = []
    for p, v in enumerate(json_players):
        try:
            priority = json_priority[v['name']]
        except KeyError:
            priority = 0
        players.append(Player(v['name'], v['rankings'], priority))

    player_queue = Queue.PriorityQueue()
    for p in players:
        player_queue.put((p.priority, p))

    score = 0
    leftover_players = []
    while not player_queue.empty():
        current_player_to_allocate = player_queue.get()[1]
        if current_player_to_allocate.has_rankings():
            for value, ranking in enumerate(current_player_to_allocate.rankings, start=1):
                if games[ranking].add_player(current_player_to_allocate):
                    score += value
                    current_player_to_allocate.modify_priority(-1 * value)
                    break
        else:
            leftover_players.append(current_player_to_allocate)

    for gameID, game in games.iteritems():
        while not game.at_capacity():
            for current_player in leftover_players:
                if game.add_player(current_player):
                    leftover_players.remove(current_player)

    player_priorities_for_json = {}
    for player in players:
        player_priorities_for_json[player.name] = player.priority

    with open('data/priority.json', 'w') as f:
        json.dump(player_priorities_for_json, f)

    print"Result of score: %s " % score
    for gameID, game in games.iteritems():
        print (gameID, game)

# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
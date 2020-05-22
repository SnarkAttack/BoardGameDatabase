from django.http import HttpResponse
from django.views import View
from ..models import BoardGame, Player, Play
from django.template import loader
from pybgg_json import PyBggInterface

from .utilities.conversion_utilities import str_repr_int

class UpdateCollectionView(View):
    
    def create_or_update_player_model(player_data, player):

        player.player_name = player_data.get('name', None)
        player.bgg_username = player_data.get('username', None)
        player.bgg_id = player_data.get('userid', None)

        return True

    def create_or_update_play_model(play_data, play, game_id):

        play.game = BoardGame.objects.get(bgg_id=game_id)
        play.play_date = play_data.get('date', None)
        play.ignore = play_data.get('incomplete', None)

        return True

    def create_or_update_player_score_model(player_score_data, player_score):

        score = player_score_data.get('score', '')
        player_score.score = score if str_repr_int(score) else None
        #player_score.role = player_score_data.get('role', None)
        #player_score.start_player = player_score_data.get('startPlayer', False)
        #player_score.seat_order = player_score_data.get('startposition', 0)
        #player_score.new_player = player_score_data.get('newPlayer', False)
        #team = player_score_data.get('team', '')
        #player_score.team = team if str_repr_int(team) else None
        # This field is required
        player_score.winner = True if player_score_data.get('win') == 1 else 0

        return True
    
    def create_or_update_board_game_model(boardgame_model, game_dict_contents):
        try:
            game_names = game_dict_contents['name']
            if type(game_names) is list:
                for name in game_names:
                    if 'primary' in name:
                        boardgame_model.name = name['primary']['value']
            else:
                boardgame_model.name = game_names['primary']['value']
                    
            boardgame_model.min_players = int(game_dict_contents['minplayers'])
            boardgame_model.max_players = int(game_dict_contents['maxplayers'])

            best_player_count = 0
            for item in game_dict_contents['poll']:
                if item['name'] == 'suggested_numplayers':
                    best = 0
                    for row in item['results']:
                        for value in row['result']:
                            if int(value['numvotes']) > best:
                                best_player_count = row['numplayers']
                                best = int(value['numvotes'])

            boardgame_model.best_with = best_player_count

            boardgame_model.len_m = int(game_dict_contents['playingtime'])
            boardgame_model.min_len_m = int(game_dict_contents['minplaytime'])
            boardgame_model.max_len_m = int(game_dict_contents['maxplaytime'])

            ratings_dict = game_dict_contents['statistics']['ratings']

            boardgame_model.average = float(ratings_dict['average'])
            boardgame_model.bayes_average = float(ratings_dict['bayesaverage'])

            boardgame_model.weight = float(ratings_dict['averageweight'])

            categories = []
            mechanics = []
            link =  game_dict_contents['link']
            if 'boardgamecategory' in link:
                for game_category in link['boardgamecategory']:
                    category, created = BoardGameCategory.objects.get_or_create(category_name=game_category['value'])
                    if created:
                        category.save()
                boardgame_model.categories.add(category)
            elif 'boardgamemechanic' in link:
                for game_mechanic in link['boardgamemechanic']:
                    mechanic, created = BoardGameMechanic.objects.get_or_create(mechanic_name=game_mechanic['value'])
                    if created:
                        mechanic.save()
                    boardgame_model.mechanics.add(mechanic)
            elif 'boardgameexpansion' in link and 'inbound' not in link['boardgameexpansion']:
                for game_expansion in link['boardgameexpansion']:
                    base_game, created = BoardGame.objects.get_or_create(bgg_id=game_expansion['id'])
                    if created:
                        base_game.save()
                    boardgame_model.base_game = base_game

        # Catch exceptions here so we can keep moving on
        except TypeError as e:
            print(f"Caught exception when trying to parse {boardgame_model.bgg_id}: {e}")
        
        return True
    
    def get(self, request, bgg_username):
        pybgg_int = PyBggInterface()
        
        plays = pybgg_int.plays_request(username=bgg_username)
        
        for play in plays['plays']['play']:
            
            print(play)
            
            game_data = play['item']
            game, created = BoardGame.objects.get_or_create(bgg_id=game_data['objectid'], name=game_data['name'])
            # Not trying to populate here
            game.save()

            play_obj, _ = Play.objects.get_or_create(play_id=play['id'])
            self.create_or_update_play_model(play, play_obj, game.bgg_id)
            play_obj.save()
            
            for player_data in play['players']['player']:
                player, _ = Player.objects.get_or_create(player_name=player_data['name'])
                self.create_or_update_player_model(player_data, player)
                player.save()
                
                player_score, _ = play_obj.player_scores.get_or_create(player=player)
                self.create_or_update_player_score_model(player_data, player_score)
                player_score.play = play_obj
                player_score.save()

        return HttpResponseRedirect(reverse('game_index'))
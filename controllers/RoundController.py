from datetime import datetime
import random


class RoundController:
    """Controller for managing tournament rounds and matches"""

    def __init__(self, master_controller):
        """Initialize round controller

        Args:
            master_controller: Main application controller
        """
        self.master_controller = master_controller
        self.data_manager = master_controller.tournament_controller.data_manager
        self.current_tournament = None
        self.callbacks = {
            'get_current_tournament': self.get_current_tournament,
            'load_players_data': self.load_players_data,
            'create_new_round': self.create_new_round,
            'finish_round': self.finish_round,
            'update_match_scores': self.update_match_scores,
            'calculate_player_points': self.calculate_player_points,
            'return_list_tournament': self.return_to_tournaments
        }

    def get_callbacks(self):
        """Return the callback dictionary for the view

        Returns:
            dict: Dictionary containing view callback functions
        """
        return self.callbacks

    def set_current_tournament(self, tournament_name):
        """Set the current tournament being managed

        Args:
            tournament_name: Name of the tournament to manage
        """
        self.current_tournament = tournament_name

    def get_current_tournament(self):
        """Get the current tournament data

        Returns:
            dict: Current tournament data
        """
        if not self.current_tournament:
            self.current_tournament = (self.master_controller.
                                       tournament_controller.current_tournament)

        data = self.data_manager.load_data()
        tournaments = data.get("tournaments", {})
        return tournaments.get(self.current_tournament, {})

    def load_players_data(self):
        """Load player data for the current tournament

        Returns:
            dict: Dictionary of player data
        """
        data = self.data_manager.load_data()
        return data.get("players", {})

    def create_new_round(self):
        """Create a new round with paired players

        Returns:
            tuple: (success, message)
        """
        tournament_data = self.get_current_tournament()

        # Check if tournament exists
        if not tournament_data:
            return False, "Tournoi non trouvé"

        # Check if all previous rounds are completed
        rounds_data = tournament_data.get('rounds_data', [])
        for round_data in rounds_data:
            if not round_data.get('end_time'):
                return False, ("Veuillez terminer le tour en"
                               "cours avant d'en créer un nouveau")

        # Check if we've reached the maximum number of rounds
        max_rounds = tournament_data.get('rounds', 4)
        if len(rounds_data) >= max_rounds:
            return False, f"Le nombre maximum de tours ({max_rounds}) a été atteint"

        # Get player IDs from tournament
        player_ids = tournament_data.get('players', [])
        if len(player_ids) < 8:
            return False, "Le tournoi doit avoir au moins 8 joueurs"

        # Generate pairs based on tournament progress
        round_number = len(rounds_data) + 1
        round_name = f"Round {round_number}"

        # First round: random pairing
        if round_number == 1:
            pairs = self._generate_first_round_pairs(player_ids)
        else:
            # Subsequent rounds: pair by score
            pairs = self._generate_subsequent_round_pairs(player_ids, rounds_data)

        # Create matches from pairs
        matches = [((pair[0], 0), (pair[1], 0)) for pair in pairs]

        # Create round data
        new_round = {
            'name': round_name,
            'start_time': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'end_time': None,
            'matches': matches
        }

        # Update tournament data
        data = self.data_manager.load_data()
        if 'rounds_data' not in data['tournaments'][self.current_tournament]:
            data['tournaments'][self.current_tournament]['rounds_data'] = []

        data['tournaments'][self.current_tournament]['rounds_data'].append(new_round)
        data['tournaments'][self.current_tournament]['current_round'] = round_number

        # Save updated data
        self.data_manager.save_data(data)

        return True, f"Tour {round_name} créé avec succès"

    def _generate_first_round_pairs(self, player_ids):
        """Generate random pairs for the first round

        Args:
            player_ids: List of player IDs

        Returns:
            list: List of player pairs
        """
        # Shuffle players randomly
        shuffled_players = player_ids.copy()
        random.shuffle(shuffled_players)

        # Create pairs
        pairs = []
        for i in range(0, len(shuffled_players), 2):
            if i + 1 < len(shuffled_players):
                pairs.append((shuffled_players[i], shuffled_players[i + 1]))

        return pairs

    def _generate_subsequent_round_pairs(self, player_ids, rounds_data):
        """Generate pairs for subsequent rounds based on scores

        Args:
            player_ids: List of player IDs
            rounds_data: Data from previous rounds

        Returns:
            list: List of player pairs
        """
        # Calculate current points for each player
        player_points = self.calculate_player_points()

        # Sort players by points (descending)
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        sorted_player_ids = [player[0] for player in sorted_players]

        # Get all previous matches to avoid duplicates
        previous_matches = set()
        for round_data in rounds_data:
            for match in round_data.get('matches', []):
                player1 = match[0][0]
                player2 = match[1][0]
                previous_matches.add(tuple(sorted([player1, player2])))

        # Generate pairs avoiding duplicates
        pairs = []
        unmatched = sorted_player_ids.copy()

        while unmatched:
            player1 = unmatched.pop(0)

            # Find first available opponent that hasn't played against player1
            for i, player2 in enumerate(unmatched):
                if tuple(sorted([player1, player2])) not in previous_matches:
                    pairs.append((player1, player2))
                    unmatched.pop(i)
                    break
            else:
                # If all opponents have been played against, just take the next one
                if unmatched:
                    player2 = unmatched.pop(0)
                    pairs.append((player1, player2))

        return pairs

    def finish_round(self, round_name):
        """Mark a round as finished

        Args:
            round_name: Name of the round to finish

        Returns:
            tuple: (success, message)
        """
        tournament_data = self.get_current_tournament()

        # Find the round
        rounds_data = tournament_data.get('rounds_data', [])
        round_index = None

        for i, round_data in enumerate(rounds_data):
            if round_data.get('name') == round_name:
                round_index = i
                break

        if round_index is None:
            return False, f"Tour {round_name} non trouvé"

        # Check if the round is already finished
        if rounds_data[round_index].get('end_time'):
            return False, f"Le tour {round_name} est déjà terminé"

        # Update round end time
        data = self.data_manager.load_data()
        data['tournaments'][self.current_tournament]
        ['rounds_data'][round_index]['end_time'] = (datetime.now()
                                                    .strftime("%d/%m/%Y %H:%M"))

        # Save updated data
        self.data_manager.save_data(data)

        return True, f"Tour {round_name} terminé avec succès"

    def update_match_scores(self, round_name, player1_id, player2_id, score1, score2):
        """Update scores for a match

        Args:
            round_name: Name of the round
            player1_id: ID of player 1
            player2_id: ID of player 2
            score1: Score for player 1
            score2: Score for player 2

        Returns:
            tuple: (success, message)
        """
        tournament_data = self.get_current_tournament()

        # Find the round
        rounds_data = tournament_data.get('rounds_data', [])
        round_index = None
        match_index = None

        for i, round_data in enumerate(rounds_data):
            if round_data.get('name') == round_name:
                round_index = i
                # Find the match
                for j, match in enumerate(round_data.get('matches', [])):
                    match_player1 = match[0][0]
                    match_player2 = match[1][0]
                    if ((match_player1 == player1_id and match_player2 == player2_id)
                        or
                       (match_player1 == player2_id and match_player2 == player1_id)):
                        match_index = j
                        break
                break

        if round_index is None or match_index is None:
            return False, "Match non trouvé"

        # Update match scores
        data = self.data_manager.load_data()
        match = data['tournaments'][self.current_tournament]
        ['rounds_data'][round_index]['matches'][match_index]

        # Determine which player is which in the stored match
        if match[0][0] == player1_id:
            match[0] = (player1_id, score1)
            match[1] = (player2_id, score2)
        else:
            match[0] = (player2_id, score2)
            match[1] = (player1_id, score1)

        data['tournaments'][self.current_tournament]
        ['rounds_data'][round_index]['matches'][match_index] = match

        # Save updated data
        self.data_manager.save_data(data)

        return True, "Scores mis à jour avec succès"

    def calculate_player_points(self):
        """Calculate points for each player in the tournament

        Returns:
            dict: Dictionary of player points
        """
        tournament_data = self.get_current_tournament()
        player_points = {player_id: 0 for player_id in
                         tournament_data.get('players', [])}

        # Sum points from all rounds
        for round_data in tournament_data.get('rounds_data', []):
            for match in round_data.get('matches', []):
                player1_id, score1 = match[0]
                player2_id, score2 = match[1]

                if player1_id in player_points:
                    player_points[player1_id] += float(score1)
                if player2_id in player_points:
                    player_points[player2_id] += float(score2)

        return player_points

    def return_to_tournaments(self):
        """Return to the tournaments list view"""
        self.master_controller.show_view("tournaments")

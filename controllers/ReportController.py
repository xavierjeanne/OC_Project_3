class ReportController:
    """Controller for generating and displaying reports"""

    def __init__(self, master_controller):
        """Initialize report controller

        Args:
            master_controller: Main application controller
        """
        self.master_controller = master_controller
        self.data_manager = master_controller.tournament_controller.data_manager
        self.callbacks = {
            'load_all_players':
                self.load_all_players,
            'load_all_tournaments':
                self.load_all_tournaments,
            'get_tournament_details':
                self.get_tournament_details,
            'get_tournament_players':
                self.get_tournament_players,
            'get_tournament_rounds_matches':
                self.get_tournament_rounds_matches,
            'get_players_alphabetical':
                self.get_players_alphabetical,
            'get_tournaments_for_display':
                self.get_tournaments_for_display,
            'get_tournament_names':
                self.get_tournament_names,
            'get_tournament_details_for_display':
                self.get_tournament_details_for_display,
            'get_tournament_players_for_display':
                self.get_tournament_players_for_display,
            'get_tournament_rounds_matches_for_display':
                self.get_tournament_rounds_matches_for_display,
            'get_tournament_standings_for_display':
                self.get_tournament_standings_for_display,  # Add this line
            'return_home':
                self.return_home
        }

    def get_callbacks(self):
        """Return the callback dictionary for the view
        Returns:
            dict: Dictionary containing view callback functions
        """
        return self.callbacks

    def load_all_players(self):
        """Load all players from the database

        Returns:
            dict: Dictionary of all players
        """
        data = self.data_manager.load_data()
        return data.get("players", {})

    def load_all_tournaments(self):
        """Load all tournaments from the database

        Returns:
            dict: Dictionary of all tournaments
        """
        data = self.data_manager.load_data()
        return data.get("tournaments", {})

    def get_tournament_details(self, tournament_name):
        """Get details of a specific tournament

        Args:
            tournament_name: Name of the tournament

        Returns:
            dict: Tournament details
        """
        data = self.data_manager.load_data()
        tournaments = data.get("tournaments", {})
        return tournaments.get(tournament_name, {})

    def get_tournament_players(self, tournament_name):
        """Get players of a specific tournament

        Args:
            tournament_name: Name of the tournament

        Returns:
            dict: Dictionary of tournament players
        """
        data = self.data_manager.load_data()
        tournaments = data.get("tournaments", {})
        tournament = tournaments.get(tournament_name, {})

        # Get player IDs from tournament
        player_ids = tournament.get('players', [])

        # Get player details
        all_players = data.get("players", {})
        tournament_players = ({player_id: all_players.get(player_id, {})
                              for player_id in player_ids if player_id in all_players})

        return tournament_players

    def get_tournament_rounds_matches(self, tournament_name):
        """Get rounds and matches of a specific tournament

        Args:
            tournament_name: Name of the tournament

        Returns:
            list: List of rounds with matches
        """
        data = self.data_manager.load_data()
        tournaments = data.get("tournaments", {})
        tournament = tournaments.get(tournament_name, {})

        return tournament.get('rounds_data', [])

    def get_players_alphabetical(self):
        """Get all players sorted alphabetically by last name

        Returns:
            list: List of player dictionaries with display-ready format
        """
        # Use load_all_players instead of player_manager
        players_data = self.load_all_players()

        # Sort players alphabetically by name
        sorted_players = sorted(
            players_data.items(),
            key=lambda x: x[1].get('last_name', '').lower()
            if isinstance(x[1], dict) else ''
        )

        # Format for display
        result = []
        for player_id, player in sorted_players:
            if isinstance(player, dict):
                result.append({
                    'last_name': player.get('last_name', ''),
                    'first_name': player.get('first_name', ''),
                    'birth_date': player.get('birth_date', ''),
                    'id': player_id
                })

        return result

    def get_tournaments_for_display(self):
        """Get all tournaments formatted for display

        Returns:
            list: List of tournament dictionaries with display-ready format
        """
        # Use load_all_tournaments instead of tournament_manager
        tournaments_data = self.load_all_tournaments()

        # Format for display
        result = []
        for name, tournament in tournaments_data.items():
            result.append({
                'name': name,
                'location': tournament.get('location', ''),
                'start_date': tournament.get('start_date', ''),
                'end_date': tournament.get('end_date', ''),
                'status': tournament.get('status', 'Non démarré')
            })

        return result

    def get_tournament_names(self):
        """Get list of all tournament names

        Returns:
            list: List of tournament names
        """
        # Use load_all_tournaments instead of tournament_manager
        tournaments_data = self.load_all_tournaments()
        return list(tournaments_data.keys())

    def get_tournament_details_for_display(self, tournament_name):
        """Get details of a specific tournament formatted for display

        Args:
            tournament_name (str): Name of the tournament

        Returns:
            dict: Result containing success status, message, and data
        """
        if not tournament_name:
            return {
                'success': False,
                'message': "Veuillez sélectionner un tournoi",
                'data': None
            }

        # Use get_tournament_details instead of tournament_manager
        tournament_data = self.get_tournament_details(tournament_name)

        if not tournament_data:
            return {
                'success': False,
                'message': f"Tournoi {tournament_name} non trouvé",
                'data': None
            }

        # Format for display
        result = {
            'name': tournament_name,
            'location': tournament_data.get('location', ''),
            'start_date': tournament_data.get('start_date', ''),
            'end_date': tournament_data.get('end_date', ''),
            'rounds': tournament_data.get('rounds', ''),
            'description': tournament_data.get('description', ''),
            'status': tournament_data.get('status', 'Non démarré')
        }

        return {
            'success': True,
            'message': "",
            'data': result
        }

    def get_tournament_players_for_display(self, tournament_name):
        """Get players of a specific tournament formatted for display

        Args:
            tournament_name (str): Name of the tournament

        Returns:
            dict: Result containing success status, message, and data
        """
        if not tournament_name:
            return {
                'success': False,
                'message': "Veuillez sélectionner un tournoi",
                'data': None
            }

        players = self.get_tournament_players(tournament_name)

        if not players:
            return {
                'success': False,
                'message': f"Aucun joueur trouvé pour le tournoi {tournament_name}",
                'data': None
            }

        # Sort players alphabetically
        sorted_players = sorted(
            players.items(),
            key=lambda x: x[1]['last_name'].lower()
        )

        # Format for display
        result = []
        for player_id, player in sorted_players:
            result.append({
                'last_name': player.get('last_name', ''),
                'first_name': player.get('first_name', ''),
                'birth_date': player.get('birth_date', ''),
                'id': player_id
            })

        return {
            'success': True,
            'message': "",
            'data': result
        }

    def get_tournament_rounds_matches_for_display(self, tournament_name):
        """Get rounds and matches of a specific tournament formatted for display

        Args:
            tournament_name (str): Name of the tournament

        Returns:
            dict: Result containing success status, message, and data
        """
        if not tournament_name:
            return {
                'success': False,
                'message': "Veuillez sélectionner un tournoi",
                'data': None
            }

        rounds_data = self.get_tournament_rounds_matches(tournament_name)

        if not rounds_data:
            return {
                'success': False,
                'message': f"Aucun tour trouvé pour le tournoi {tournament_name}",
                'data': None
            }

        # Get players data for displaying names
        players_data = self.load_all_players()

        # Format rounds and matches for display
        formatted_rounds = []
        try:
            for round_data in rounds_data:
                formatted_round = {
                    'name': round_data.get('name', ''),
                    'start_time': round_data.get('start_time', 'Non démarré'),
                    'end_time': round_data.get('end_time', 'En cours'),
                    'matches': []
                }

                # Format matches
                matches = round_data.get('matches', [])
                for match in matches:
                    if len(match) != 2:
                        continue  # Skip invalid matches

                    player1_id, score1 = match[0]
                    player2_id, score2 = match[1]

                    player1_data = players_data.get(player1_id, {})
                    player2_data = players_data.get(player2_id, {})

                    player1_name = player1_data.get('last_name', '')
                    player2_name = player2_data.get('last_name', '')
                    player1_first_name = player1_data.get('first_name', '')
                    player2_first_name = player2_data.get('first_name', '')

                    formatted_match = {
                        'player1_name': f"{player1_first_name} {player1_name}".strip(),
                        'score1': score1,
                        'player2_name': f"{player2_first_name} {player2_name}".strip(),
                        'score2': score2
                    }

                    formatted_round['matches'].append(formatted_match)

                formatted_rounds.append(formatted_round)

            return {
                'success': True,
                'message': "",
                'data': formatted_rounds
            }
        except Exception as e:
            # Add error handling to prevent crashes
            return {
                'success': False,
                'message': f"Erreur lors du traitement des données: {str(e)}",
                'data': None
            }

    def return_home(self):
        """Navigate back to home view"""
        self.master_controller.show_view("home")

    def get_tournament_standings_for_display(self, tournament_name):
        """Get player standings/rankings for a specific tournament
        Args:
            tournament_name (str): Name of the tournament
        Returns:
            dict: Result containing success status, message, and data
        """
        if not tournament_name:
            return {
                'success': False,
                'message': "Veuillez sélectionner un tournoi",
                'data': None
            }

        # Get tournament data
        tournament_data = self.get_tournament_details(tournament_name)

        if not tournament_data:
            return {
                'success': False,
                'message': f"Tournoi {tournament_name} non trouvé",
                'data': None
            }

        # Calculate player points
        player_points = {}
        rounds_data = tournament_data.get('rounds_data', [])

        # Initialize points for all players
        for player_id in tournament_data.get('players', []):
            player_points[player_id] = 0

        # Sum points from all rounds
        for round_data in rounds_data:
            for match in round_data.get('matches', []):
                if len(match) == 2:
                    player1_id, score1 = match[0]
                    player2_id, score2 = match[1]

                    if player1_id in player_points:
                        player_points[player1_id] += float(score1)
                    if player2_id in player_points:
                        player_points[player2_id] += float(score2)

        # Sort players by points (descending)
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)

        # Get player details
        players_data = self.load_all_players()

        # Format for display
        result = []
        for rank, (player_id, scores) in enumerate(sorted_players, 1):
            player_data = players_data.get(player_id, {})
            result.append({
                'rank': rank,
                'last_name': player_data.get('last_name', ''),
                'first_name': player_data.get('first_name', ''),
                'score': scores
            })

        return {
            'success': True,
            'message': "",
            'data': result
        }

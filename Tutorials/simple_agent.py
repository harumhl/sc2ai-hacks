# simple_agent.py
# Description: Demonstrates the Starcraft API
# Code modified from:
    # https://chatbotslife.com/building-a-basic-pysc2-agent-b109cde1477c
# Usage:
    # Call Google's with your agent via the following terminal command:
    # python -m pysc2.bin.agent --map Simple64 --agent simple_agent.SimpleAgent --agent_race T
# General Architecture:
    # Terminal loads our agent into Google's code
    # The agent/our code is given OBSERVATIONS about the current game state
    # Our code figures out what ACTIONS it wants to take
    # Google's code inputs our actions into Starcraft
    # Game time is moved forward
    # Google's code returns the results of our actions
    # Repeat
from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
import time

# Nicknames--------------------------------------------------------------------
# Functions
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id

# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Unit IDs
_TERRAN_BARRACKS = 21
_TERRAN_COMMANDCENTER = 18
_TERRAN_SUPPLYDEPOT = 19
_TERRAN_SCV = 45

# Parameters
_PLAYER_SELF = 1
_SUPPLY_USED = 3
_SUPPLY_MAX = 4
_NOT_QUEUED = [0]
_QUEUED = [1]

# Classes --------------------------------------------------------------------
class SimpleAgent(base_agent.BaseAgent):
    """A specialization of the base agent. """

    # State Tracking
    base_top_left = None
    supply_depot_built = False
    scv_selected = False
    barracks_built = False
    barracks_selected = False
    barracks_rallied = False
    army_selected = False
    army_rallied = False

    # Helper functions
    def transformLocation(self, x, x_distance, y, y_distance):
        """Targets a location x_distance,y_distance from current location x,y"""
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]
        return [x + x_distance, y + y_distance]
 
    # Inherited Functions
    def step(self, obs):
        """ Determines what the agent does each step of game time"""
        super(SimpleAgent, self).step(obs) # Advances game time by one step
        time.sleep(0) # Time that game is paused while comutation continues

        # Check if our base on on the top or bottom of the 64unit map
        if self.base_top_left is None:
            player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base_top_left = player_y.mean() <= 31

        # Control the agent's thinking and acting
        if not self.supply_depot_built:
            if not self.scv_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()

                target = [unit_x[0], unit_y[0]]

                self.scv_selected = True

                    # Add an action to the action queue.
                    # Starcraft will run the queue at the next step
                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()

                target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)

                self.supply_depot_built = True

                # Add an action to the action queue.
                # Starcraft will run the queue at the next step
                return actions.FunctionCall(_BUILD_SUPPLYDEPOT, [_NOT_QUEUED, target])
        elif not self.barracks_built:
            if _BUILD_BARRACKS in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()

                target = self.transformLocation(int(unit_x.mean()), 20, int(unit_y.mean()), 0)

                self.barracks_built = True

                # Add an action to the action queue.
                # Starcraft will run the queue at the next step
                return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])
        elif not self.barracks_rallied:
            if not self.barracks_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()

                if unit_y.any():
                    target = [int(unit_x.mean()), int(unit_y.mean())]

                    self.barracks_selected = True

                    # Add an action to the action queue.
                    # Starcraft will run the queue at the next step
                    return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            else:
                self.barracks_rallied = True

                if self.base_top_left:
                        # Add an action to the action queue.
                        # Starcraft will run the queue at the next step
                    return actions.FunctionCall(_RALLY_UNITS_MINIMAP, [_NOT_QUEUED, [29, 21]])

                    # Add an action to the action queue.
                    # Starcraft will run the queue at the next step
                return actions.FunctionCall(_RALLY_UNITS_MINIMAP, [_NOT_QUEUED, [29, 46]])
        elif obs.observation["player"][_SUPPLY_USED] < obs.observation["player"][_SUPPLY_MAX] and _TRAIN_MARINE in obs.observation["available_actions"]:
                # Add an action to the action queue.
                # Starcraft will run the queue at the next step
            return actions.FunctionCall(_TRAIN_MARINE, [_QUEUED])
        elif not self.army_rallied:
            if not self.army_selected:
                if _SELECT_ARMY in obs.observation["available_actions"]:
                    self.army_selected = True
                    self.barracks_selected = False

                    # Add an action to the action queue.
                    # Starcraft will run the queue at the next step
                    return actions.FunctionCall(_SELECT_ARMY, [_NOT_QUEUED])
            elif _ATTACK_MINIMAP in obs.observation["available_actions"]:
                self.army_rallied = True
                self.army_selected = False

                if self.base_top_left:
                        # Add an action to the action queue.
                        # Starcraft will run the queue at the next step
                    return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, [39, 45]])

                    # Add an action to the action queue.
                    # Starcraft will run the queue at the next step
                return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, [21, 24]])
                    # Add an action to the action queue.
                    # Starcraft will run the queue at the next step
        return actions.FunctionCall(_NOOP, [])

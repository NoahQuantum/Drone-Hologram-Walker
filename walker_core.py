import numpy as np

"""
Project: Drone-Hologram-Walker
Module: walker_core.py (The Soul)
Description: Generates 3D coordinates for a walking human figure (Head, Left Foot, Right Foot).
License: GNU GPL v3.0
Authors: Noah & Partners
"""

class WalkerSoul:
    def __init__(self, stride_length=1.0, step_height=0.3, walk_speed=1.0):
        """
        Initialize the walking parameters based on biomechanical principles.
        :param stride_length: Distance covered in one full gait cycle (meters).
        :param step_height: Maximum height a foot reaches during the swing phase (meters).
        :param walk_speed: Frequency of the steps (Cycles per second / Hz).
        """
        self.stride_length = stride_length
        self.step_height = step_height
        self.walk_speed = walk_speed
        self.head_base_height = 1.7 # Reference height for the top drone

    def get_positions(self, t):
        """
        Calculate the 3D trajectory of 3 drones at time t.
        :param t: Elapsed time in seconds.
        :return: Dictionary with (x, y, z) coordinates for head and feet.
        """
        # Linear progress based on time and speed
        # phase represents the position within one 360-degree gait cycle
        phase = 2 * np.pi * self.walk_speed * t
        
        # 1. Head (Center of Mass): 
        # Moves forward linearly with a dual-frequency vertical oscillation (bouncy gait).
        head_x = self.stride_length * (self.walk_speed * t)
        head_y = 0
        # The center of mass naturally oscillates twice per cycle (once per step).
        head_z = self.head_base_height + 0.06 * np.sin(2 * phase)

        # 2. Left Foot (Swing & Stance phase):
        # Positioned to represent the primary contact point.
        l_phase = phase
        l_x = head_x + (self.stride_length * 0.5) * np.cos(l_phase)
        l_y = -0.15 # Fixed lateral width for stability
        # The foot lifts during the swing phase and stays at ground level during stance.
        l_z = max(0, self.step_height * np.sin(l_phase))

        # 3. Right Foot: 
        # Mirroring the left foot with a 180-degree phase shift.
        r_phase = phase + np.pi
        r_x = head_x + (self.stride_length * 0.5) * np.cos(r_phase)
        r_y = 0.15   
        r_z = max(0, self.step_height * np.sin(r_phase))

        return {
            "head": (head_x, head_y, head_z),
            "left_foot": (l_x, l_y, l_z),
            "right_foot": (r_x, r_y, r_z)
        }

if __name__ == "__main__":
    # Internal test to verify numerical stability
    walker = WalkerSoul()
    print("WalkerSoul: Generating mathematical gait coordinates...")
    sample_pos = walker.get_positions(0.5)
    print(f"Sample at 0.5s -> Head: {sample_pos['head']}")

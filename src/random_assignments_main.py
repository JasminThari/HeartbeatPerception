import pandas as pd 
import random
from itertools import combinations
from collections import Counter

person_video_segments = {
    1: [0, 25, 30, 35, 40, 45, 50, 70, 75, 90, 110],
    2: [5, 10, 15, 25, 35, 45, 65, 70, 85, 95, 105],
    3: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 110],
    4: [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110],
    5: [0, 10, 20, 30, 40, 50, 60, 70, 90, 100, 110],
    6: [0, 10, 20, 30, 40, 50, 70, 80, 90, 100, 110],
    7: [0, 10, 20, 25, 40, 45, 50, 80, 85, 90, 110],
    9: [0, 10, 20, 30, 40, 50, 70, 80, 90, 100, 110],
    10: [0, 5, 15, 20, 25, 55, 60, 65, 85, 95, 105],
    11: [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110],
    12: [0, 10, 20, 30, 50, 60, 70, 80, 90, 100, 110],
    13: [5, 15, 20, 25, 35, 45, 55, 65, 75, 85, 105]
    }

##### Randomly assign pairs of participants to unique video segments #####
def pair_participants(person_video_segments):
    # Create unique pairs of people
    unique_pairs = list(combinations(person_video_segments.keys(), 2))

    # Shuffle the segment lists for each person to ensure random selection
    remaining_segments = {person: random.sample(segments, len(segments)) for person, segments in person_video_segments.items()}

    # Assign pairs with random unique segments for each person
    random_pairings = []

    for person1, person2 in unique_pairs:
        # Get the next available random segments for each person
        if remaining_segments[person1] and remaining_segments[person2]:
            segment1 = remaining_segments[person1].pop(0)
            segment2 = remaining_segments[person2].pop(0)
            random_pairings.append((person1, segment1, person2, segment2))
    
    df_random_pairings = pd.DataFrame(random_pairings, columns=['Participant_x', 'Segment_x', 'Participant_y', 'Segment_y'])
    
    return df_random_pairings

df_random_pairings = pair_participants(person_video_segments)
df_random_pairings.to_csv('assignments/participants_pairings.csv', index=False)

##### Randomly assign left or right side to each pair while ensuring equal distribution #####

# Step 1: Generate all possible pairs
participants = list(person_video_segments.keys())
all_pairs = list(combinations(participants, 2))
random.shuffle(all_pairs)  # Shuffle the pairs

# Step 2: Initialize Quotas
def initialize_quotas():
    random.shuffle(participants)
    left_quota = {participant: 5 for participant in participants}
    
    # Assign extra Left quotas to reach total of 33 Left assignments
    extra_left = 33 - len(participants) * 5  # Adjusted for 33 total Left assignments
    for i in range(extra_left):
        left_quota[participants[i]] = 6
    return left_quota

# Step 3: Define the Assignment Function
def assign_pair_balanced(row, left_quota, left_count, right_count):
    x = row['Participant_x']
    y = row['Participant_y']
    
    # Check remaining Left quotas
    x_left_remaining = left_quota[x] - left_count[x]
    y_left_remaining = left_quota[y] - left_count[y]
    
    # Possible assignments
    assignments = []
    
    if x_left_remaining > 0 and y_left_remaining > 0:
        # Both can be assigned to Left; decide based on who needs more Left assignments
        if x_left_remaining > y_left_remaining:
            assignments.append((x, y))
        elif y_left_remaining > x_left_remaining:
            assignments.append((y, x))
        else:
            # If equal, randomly choose
            assignments.extend([(x, y), (y, x)])
    elif x_left_remaining > 0:
        assignments.append((x, y))
    elif y_left_remaining > 0:
        assignments.append((y, x))
    else:
        # Neither can be assigned to Left based on quota; assign randomly
        assignments.extend([(x, y), (y, x)])
    
    # Choose assignment
    chosen_assignment = random.choice(assignments)
    
    # Update counts
    left_count[chosen_assignment[0]] += 1
    right_count[chosen_assignment[1]] += 1
    
    return pd.Series({'Left': chosen_assignment[0], 'Right': chosen_assignment[1]})

# Main loop to ensure condition is met
while True:
    # Initialize the data and counts
    df_side_assignment = pd.DataFrame(all_pairs, columns=['Participant_x', 'Participant_y'])
    left_quota = initialize_quotas()
    left_count = {participant: 0 for participant in participants}
    right_count = {participant: 0 for participant in participants}
    
    # Apply the assignment function
    df_side_assignment[['Left', 'Right']] = df_side_assignment.apply(assign_pair_balanced, axis=1, args=(left_quota, left_count, right_count))
    
    # Check if the value counts for 'Left' are all 5 or 6
    left_counts = df_side_assignment['Left'].value_counts()
    if all(count in [5, 6] for count in left_counts.values):
        break  # Exit the loop if the condition is met
    
df_side_assignment.to_csv('assignments/participants_side_assignment.csv', index=False)

##### Randomly assign heartbeats to pairs while ensuring equal distribution #####

def assign_heartbeat(row):
    # Get available participants
    x = row['Participant_x']
    y = row['Participant_y']
    
    # Get the current count of heartbeats for both participants
    x_count = heartbeat_count[x]
    y_count = heartbeat_count[y]
    
    # Decide randomly but balance the distribution with constraints
    if x_count < 6 and (y_count >= 6 or random.choice([True, False])):
        heartbeat_count[x] += 1
        return x
    else:
        heartbeat_count[y] += 1
        return y

# Main loop to ensure condition is met
while True:
    # Step 1: Generate all possible pairs
    participants = list(person_video_segments.keys())
    all_pairs = list(combinations(participants, 2))
    random.shuffle(all_pairs)  # Shuffle the pairs

    # Step 2: Initialize dataframe with pairs
    df_heat_beat = pd.DataFrame(all_pairs, columns=['Participant_x', 'Participant_y'])

    # Step 3: Distribute heartbeats ensuring max 6 and min 5 for each participant
    heartbeat_count = Counter()
    
    # Apply the assignment function
    df_heat_beat['HeartBeat']= df_heat_beat.apply(assign_heartbeat, axis=1)
    
    # Check if the value counts for 'Left' are all 5 or 6
    heartbeat_counts = df_heat_beat['HeartBeat'].value_counts()
    if all(count in [5, 6] for count in heartbeat_counts.values):
        break  # Exit the loop if the condition is met

df_heat_beat.to_csv('assignments/participants_heartbeat_assignment.csv', index=False)

#### Merge all assignments into a single dataframe ####
df_heat_beat = pd.read_csv('assignments/participants_heartbeat_assignment.csv')
df_side_assignment = pd.read_csv('assignments/participants_side_assignment.csv')
df_random_pairings = pd.read_csv('assignments/participants_pairings.csv')

df_merge_1 = pd.merge(df_random_pairings, df_side_assignment, on=['Participant_x', 'Participant_y'])
df_final = pd.merge(df_merge_1, df_heat_beat, on=['Participant_x', 'Participant_y'])

df_final.to_csv('assignments/final_assignment.csv', index=False)
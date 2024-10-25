# Import libraries
from psychopy import visual, core, event
import csv
import os
import pandas as pd
import random
import argparse  

## --------------------- Parse command-line arguments  --------------------- ##

parser = argparse.ArgumentParser(description='Run the PsychoPy experiment.')
parser.add_argument('num', type=int, help='Experiment number')
parser.add_argument('participant', type=str, help='Participant ID')
parser.add_argument('gender', type=str, help='Gender m/f')
parser.add_argument('fullname', type=str, help='Full name')
args = parser.parse_args()

participant = args.participant
full_name = args.fullname
num = args.num

## --------------------- Set up the environment  --------------------- ##

# Initialize the window
win = visual.Window(fullscr=True, color='black', checkTiming=True, useFBO=True)

# Initialize the global clock
globalClock = core.Clock()

# Create the square stimulus
square = visual.Rect(
    win,
    width=0.2,  # Adjust size as needed
    height=0.3,
    fillColor='black',
    lineColor='black',
    pos=(0, 0.39) # -0.5 # Position the square as needed
)

# Create the break text stimulus
start_text = visual.TextStim(
    win,
    text="Press space to start the experiment",
    font='Arial', 
    color='white',
    pos=(0, 0),    
    height=0.12,    
    bold=True
)

# Create the text stimuli for response screen
left_arrow_text = visual.TextStim(
    win,
    text="←",
    font='Arial', 
    color='white',
    pos=(-0.15, 0),  
    height=0.17,    
    bold=True
)

# Create TextStim for "OR"
or_text = visual.TextStim(
    win,
    text="OR",
    font='Arial', 
    color='white',
    pos=(0, 0),    
    height=0.12,    
    bold=False
)

# Create TextStim for the right arrow
right_arrow_text = visual.TextStim(
    win,
    text="→",
    font='Arial', 
    color='white',
    pos=(0.15, 0),   
    height=0.17,    
    bold=True
)

# Create the break text stimulus
break_text = visual.TextStim(
    win,
    text="Break",
    font='Arial', 
    color='white',
    pos=(0, 0),    
    height=0.12,    
    bold=True
)

# Open a CSV file to save responses
data_file = open(f'Responses_Participant_{participant}_{full_name}.csv', 'w', newline='')
data_writer = csv.writer(data_file)

# Write header
data_writer.writerow(['Video', 'Response'])

# Initialize video count
video_count = 0

## --------------------- Load the videos and stim_times --------------------- ##

video_folder = f'../Data/Video/Experiment_{num}'  # Adjust the path as necessary

# Get list of video files
video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
random.shuffle(video_files)

video_objects = []
for video_file in video_files:
    video_path = os.path.join(video_folder, video_file)
    video_objects.append(visual.MovieStim(win, video_path, loop=False, size=(1440, 900), noAudio=True))
    print(f"Loaded video: {video_file}")

# Display the start text and wait for the user to press space
start_text.draw()
win.flip()
start_keys = event.waitKeys(keyList=['space', 'escape'])
if 'escape' in start_keys:
    print("Escape key pressed. Exiting.")
    win.close()
    core.quit()

# Process each video
for i, video in enumerate(video_objects):
    video_base = os.path.splitext(video_file)[0]
    video_file = video_files[i]
    
    # Get the stim_times file
    stim_times_df = pd.read_csv('assignments/final_assignment_with_peaks.csv')
    
    # Load the stim_times
    # Extract the stim_times as a list
    stim_times_str = stim_times_df.query("ID==@video_base")['Stimuli_Seconds'].values[0]
    stim_times = [float(i) for i in stim_times_str.split(',')]
        
    # Load the video
    video = video_objects[i]
    core.wait(1.2)
    
    # Reset the global clock
    globalClock.reset()
    
    stim_duration = 0.35  # Duration to show red in seconds
    
    # Create a copy of stim_times for manipulation
    pending_stim_times = stim_times.copy()
    
    # Main loop: Continue until the video finishes
    while not video.isFinished:
        t = globalClock.getTime()
        if t == 1:
            print(f"Main loop started")
        # Draw the current frame of the video
        video.draw()
        
        # Determine if the square should be red
        show_red = False
        # Iterate over a copy of the list to allow removal during iteration
        for stim_time in pending_stim_times.copy():
            if stim_time <= t < stim_time + stim_duration:
                show_red = True
                break
            elif t >= stim_time + stim_duration:
                # Remove the time if the stimulus window has passed
                pending_stim_times.remove(stim_time)
        
        # Update square color based on timing
        if show_red:
            square.fillColor = 'red'
            square.lineColor = 'red'
        else:
            square.fillColor = 'black'
            square.lineColor = 'black'
        
        # Draw the square
        square.draw()
        
        # Update the window with the drawn content
        win.flip()
        
        # Check for user input to exit
        keys = event.getKeys(keyList=["escape"])
        if keys:
            print("Escape key pressed. Exiting.")
            break
    video.stop()
    video.seek(0)
    del video
    # After the loop ends (video is finished), present the response screen
    # Draw the text stimuli
    left_arrow_text.draw()
    or_text.draw()
    right_arrow_text.draw()
    win.flip()
    
    
    # Wait for user response
    response_keys = event.waitKeys(keyList=['left', 'right', 'escape'])
    
    # Process the response
    if 'escape' in response_keys:
        print("Escape key pressed. Exiting.")
        break
    else:
        response = response_keys[0]  # Get the first key pressed
        print(f"User pressed: {response}")
        data_writer.writerow([video_base, response])
    
    # Increment video count
    video_count += 1

    # Check if a break is needed after every 33 videos
    if video_count % 34 == 0 and video_count != 0:
        # Display break screen
        break_text.draw()
        win.flip()
        # Wait until user presses 'space' or 'escape'
        break_keys = event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in break_keys:
            print("Escape key pressed during break. Exiting.")
            break
        # Optionally, clear events
        event.clearEvents()
    
    # Optionally, add a brief pause between videos
    #core.wait(1.0)
    
# Close the data file
data_file.close()

# Close the window and quit
win.close()
core.quit()

#%% Import libraries
from psychopy import visual, core, event
import csv

#%% Load the videos




# Initialize the window
win = visual.Window(fullscr=True, color='black', checkTiming=False)

# Initialize the global clock and reset it to start timing from zero
globalClock = core.Clock()
globalClock.reset()

# Load the video
video_path = '../Data/Video/test.mp4'  # Ensure this path is correct

video = visual.MovieStim(win, video_path, loop=False)

# Create the square stimulus
square = visual.Rect(
    win,
    width=0.2,  # Adjust size as needed
    height=0.3,
    fillColor='black',
    lineColor='black',
    pos=(0, -0.8)  # Position the square as needed
)

# Define stimulus times in seconds
stim_times = [1.5, 3.0, 4.5, 6.0, 7.5]

stim_duration = 0.35  # Duration to show red in seconds

# Create a copy of stim_times for manipulation
pending_stim_times = stim_times.copy()

# Open a CSV file to save responses
data_file = open('responses.csv', 'w', newline='')
data_writer = csv.writer(data_file)

# Write header
data_writer.writerow(['Response'])

# Main loop: Continue until the video finishes
while not video.isFinished:
    t = globalClock.getTime()
    
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

# After the loop ends (video is finished), present the response screen
# Create the text stimulus
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
else:
    response = response_keys[0]  # Get the first key pressed
    print(f"User pressed: {response}")
    data_writer.writerow([response])

# Close the data file
data_file.close()

# Close the window and quit
win.close()
core.quit()

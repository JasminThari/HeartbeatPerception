# # from psychopy import visual, core, event

# # # Initialize the window
# # win = visual.Window(fullscr=True, color='black', checkTiming=False)

# # # Initialize the global clock and reset it to start timing from zero
# # globalClock = core.Clock()
# # globalClock.reset()

# # # Load the video
# # video_path = '../Video/test.mp4'  # Ensure this path is correct

# # video = visual.MovieStim(win, video_path, loop=False)

# # # Create the square stimulus
# # square = visual.Rect(
# #     win,
# #     width=0.2,  # Adjust size as needed
# #     height=0.3,
# #     fillColor='black',
# #     lineColor='black',
# #     pos=(0, -0.8)  # Position the square as needed
# # )

# # # Define stimulus times in seconds
# # stim_times = [1.5, 3.0, 4.5, 6.0, 7.5]
# # stim_duration = 0.35  # Duration to show red in seconds

# # # Create a copy of stim_times for manipulation
# # pending_stim_times = stim_times.copy()

# # # Main loop: Continue until the video finishes
# # while not video.isFinished:
# #     t = globalClock.getTime()
    
# #     # Draw the current frame of the video
# #     video.draw()
    
# #     # Determine if the square should be red
# #     show_red = False
# #     # Iterate over a copy of the list to allow removal during iteration
# #     for stim_time in pending_stim_times.copy():
# #         if stim_time <= t < stim_time + stim_duration:
# #             show_red = True
# #             break
# #         elif t >= stim_time + stim_duration:
# #             # Remove the time if the stimulus window has passed
# #             pending_stim_times.remove(stim_time)
    
# #     # Update square color based on timing
# #     if show_red:
# #         square.fillColor = 'red'
# #         square.lineColor = 'red'
# #     else:
# #         square.fillColor = 'black'
# #         square.lineColor = 'black'
    
# #     # Draw the square
# #     square.draw()
    
# #     # Update the window with the drawn content
# #     win.flip()
    
# #     # Check for user input to exit
# #     keys = event.getKeys(keyList=["escape"])
# #     if keys:
# #         print("Escape key pressed. Exiting.")
# #         break

# # # After the loop ends, close the window and exit
# # win.close()
# # core.quit()

# from psychopy import visual, core, event

# # Initialize the window
# win = visual.Window(fullscr=True, color='black', units='norm', checkTiming=False)

# # Initialize the global clock and reset it to start timing from zero
# globalClock = core.Clock()
# globalClock.reset()

# # Load the video
# video_path = '../Video/test.mp4'  # Ensure this path is correct

# video = visual.MovieStim(win, video_path, loop=False)  # Adjust size as needed

# # Create the square stimulus
# square = visual.Rect(
#     win,
#     width=0.2,  # Adjust size as needed
#     height=0.3,
#     fillColor='black',
#     lineColor='black',
#     pos=(0, -0.8)  # Position the square as needed
# )

# # Define stimulus times in seconds
# stim_times = [1.5, 3.0, 4.5, 6.0, 7.5]
# stim_duration = 0.35  # Duration to show red in seconds

# # Create a copy of stim_times for manipulation
# pending_stim_times = stim_times.copy()

# # Initialize variables for response
# response = None
# response_time = None

# # Initialize mouse
# mouse = event.Mouse(win=win)

# # Define arrow stimuli using Unicode arrows
# left_arrow = visual.TextStim(win, text='←', pos=(-0.5, -0.5), color='blue', height=0.1)
# right_arrow = visual.TextStim(win, text='→', pos=(0.5, -0.5), color='blue', height=0.1)

# # Hide the mouse cursor initially
# win.mouseVisible = False

# # Main loop: Continue until the video finishes
# while not video.status == visual.FINISHED:
#     t = globalClock.getTime()
    
#     # Draw the current frame of the video
#     video.draw()
    
#     # Determine if the square should be red
#     show_red = False
#     # Iterate over a copy of the list to allow removal during iteration
#     for stim_time in pending_stim_times.copy():
#         if stim_time <= t < stim_time + stim_duration:
#             show_red = True
#             break
#         elif t >= stim_time + stim_duration:
#             # Remove the time if the stimulus window has passed
#             pending_stim_times.remove(stim_time)
    
#     # Update square color based on timing
#     if show_red:
#         square.fillColor = 'red'
#         square.lineColor = 'red'
#     else:
#         square.fillColor = 'black'
#         square.lineColor = 'black'
    
#     # Draw the square
#     square.draw()
    
#     # Update the window with the drawn content
#     win.flip()
    
#     # Check for user input to exit
#     keys = event.getKeys(keyList=["escape"])
#     if keys:
#         print("Escape key pressed. Exiting.")
#         core.quit()

# # After the video finishes, display arrows and collect response
# if video.status == visual.FINISHED:
#     # Make the mouse visible for response
#     win.mouseVisible = True

#     # Draw the arrows
#     left_arrow.draw()
#     right_arrow.draw()
#     win.flip()

#     # Reset the mouse click state
#     mouse.clickReset()
    
#     # Wait for a mouse click on one of the arrows
#     while response is None:
#         # Check if the left mouse button was clicked
#         if mouse.getPressed()[0]:  # Left button clicked
#             # Get the position of the click
#             click_pos = mouse.getPos()
#             # Check if the click was on the left arrow
#             if left_arrow.contains(click_pos):
#                 response = 'left'
#                 response_time = globalClock.getTime()
#                 print(f"Participant clicked LEFT at {response_time:.3f} seconds.")
#             # Check if the click was on the right arrow
#             elif right_arrow.contains(click_pos):
#                 response = 'right'
#                 response_time = globalClock.getTime()
#                 print(f"Participant clicked RIGHT at {response_time:.3f} seconds.")
#             else:
#                 print("Click was not on any arrow. Waiting for a valid click.")
#                 # Optionally, provide feedback or continue waiting
#             # Optional: Add a short delay to prevent multiple detections
#             core.wait(0.2)
#         core.wait(0.01)  # Prevent high CPU usage

# # Optional: Save the response data
# # For example, append to a list or write to a file
# # Here, we'll just print it
# print(f"Response: {response} at {response_time} seconds.")

# # Close the window and exit
# win.close()
# core.quit()

# from psychopy import visual, core, event

# # Initialize the window
# win = visual.Window(fullscr=True, color='black', units='norm', checkTiming=False)

# # Define arrow stimuli using Unicode arrows
# left_arrow = visual.TextStim(win, text='←', pos=(-0.5, -0.7), color='white', height=0.5)
# right_arrow = visual.TextStim(win, text='→', pos=(0.5, -0.4), color='white', height=0.5)

# # Draw the arrows
# left_arrow.draw()
# right_arrow.draw()
# win.flip()

# # Inform the user
# print("Arrows should be visible on the screen. Press any key to exit.")

# # Wait for a key press
# event.waitKeys()

# # Close the window
# win.close()
# core.quit()


from psychopy import visual, core, event

# Initialize the window
win = visual.Window(fullscr=True, color='black', units='norm', checkTiming=False)
print("Window initialized.")

# Initialize the global clock and reset it to start timing from zero
globalClock = core.Clock()
globalClock.reset()
print("Global clock reset.")

# Load the video
video_path = '../Video/test.mp4'  # Ensure this path is correct
print(f"Loading video from: {video_path}")


video = visual.MovieStim(win, video_path, loop=False)  # Fallback to MovieStim


# Create the square stimulus
square = visual.Rect(
    win,
    width=0.2,  # Adjust size as needed
    height=0.3,
    fillColor='black',
    lineColor='black',
    pos=(0, -0.8)  # Position the square as needed
)
print("Square stimulus created.")

# Define stimulus times in seconds
stim_times = [1.5, 3.0, 4.5, 6.0, 7.5]
stim_duration = 0.35  # Duration to show red in seconds
print(f"Stimulus times: {stim_times}, Duration: {stim_duration}")

# Create a copy of stim_times for manipulation
pending_stim_times = stim_times.copy()

# Initialize variables for response
response = None
response_time = None

# Initialize mouse
mouse = event.Mouse(win=win)
print("Mouse initialized.")

# Define arrow stimuli using Unicode arrows with increased height
left_arrow = visual.TextStim(
    win,
    text='←',
    pos=(-0.6, 0.8),  # Adjusted position to accommodate larger size
    color='white',
    height=0.3,  # Increased height from 0.1 to 0.3
    font='Arial'
)
right_arrow = visual.TextStim(
    win,
    text='→',
    pos=(0.6, 0.8),  # Adjusted position to accommodate larger size
    color='white',
    height=0.3,  # Increased height from 0.1 to 0.3
    font='Arial'
)
print("Arrow stimuli defined with increased size.")

# Define grey box stimuli for arrows
left_box = visual.Rect(
    win,
    width=0.4,        # Adjust width based on arrow size
    height=0.4,       # Adjust height based on arrow size
    fillColor='grey',
    lineColor='grey',
    pos=left_arrow.pos  # Same position as the left arrow
)

right_box = visual.Rect(
    win,
    width=0.4,        # Adjust width based on arrow size
    height=0.4,       # Adjust height based on arrow size
    fillColor='grey',
    lineColor='grey',
    pos=right_arrow.pos  # Same position as the right arrow
)
print("Grey box stimuli for arrows defined.")

# Hide the mouse cursor initially
win.mouseVisible = False
print("Mouse cursor hidden.")

# Main loop: Continue until the video finishes
print("Starting video playback.")
while not video.status == visual.FINISHED:
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
        win.close()
        core.quit()

print("Video playback finished. Proceeding to display arrows.")

# After the video finishes, display arrows and collect response
if video.status == visual.FINISHED:
    # Make the mouse visible for response
    win.mouseVisible = True
    print("Mouse cursor made visible.")
    
    # Draw the grey boxes first
    left_box.draw()
    right_box.draw()
    
    # Then draw the arrows on top of the boxes
    left_arrow.draw()
    right_arrow.draw()
    
    # Update the window with the drawn content
    win.flip()
    print("Arrows and their surrounding boxes drawn on the screen.")
    
    # Reset the mouse click state
    mouse.clickReset()
    print("Mouse click state reset.")
    
    # Wait for a mouse click on one of the arrows
    while response is None:
        # Check if the left mouse button was clicked
        if mouse.getPressed()[0]:  # Left button clicked
            # Get the position of the click
            click_pos = mouse.getPos()
            print(f"Mouse clicked at position: {click_pos}")
            
            # Check if the click was inside the left box
            if left_box.contains(click_pos):
                response = 'left'
                response_time = globalClock.getTime()
                print(f"Participant clicked LEFT at {response_time:.3f} seconds.")
            # Check if the click was inside the right box
            elif right_box.contains(click_pos):
                response = 'right'
                response_time = globalClock.getTime()
                print(f"Participant clicked RIGHT at {response_time:.3f} seconds.")
            else:
                print("Click was not on any arrow box. Waiting for a valid click.")
                # Optional: provide feedback or continue waiting
            
            # Add a short delay to prevent multiple detections from a single click
            core.wait(0.2)
        core.wait(0.01)  # Prevent high CPU usage

# Optional: Save the response data
# For example, append to a list or write to a file
# Here, we'll just print it
print(f"Response: {response} at {response_time} seconds.")

# Close the window and exit
win.close()
core.quit()


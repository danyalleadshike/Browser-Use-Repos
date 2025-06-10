from robocorp import windows

# Get the Calculator window.
calc = windows.find_window("name:Calculator")

# Press button "0" (the locator may vary based on the Windows version).
button0 = calc.find("(name:0 or name:num0Button) and type:Button")
button0.click()

# Clear the Calculator (the locator may vary based on the Windows version).
calc.click("id:clearEntryButton or name:Clear")

# Send the keys directly to the Calculator by typing them from the keyboard.
calc.send_keys(keys="96+4=")
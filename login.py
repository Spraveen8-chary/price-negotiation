# import os

# def print_directory_structure(folder_path, indent=''):
#     # Print the current folder name
#     print(indent + os.path.basename(folder_path) + '/')

#     # Iterate over all items in the folder
#     for item in os.listdir(folder_path):
#         item_path = os.path.join(folder_path, item)

#         # If it's a subdirectory, recursively print its structure
#         if os.path.isdir(item_path):
#             print_directory_structure(item_path, indent + '  ')
#         else:
#             # If it's a file, print its name
#             print(indent + '  ' + item)

# # Specify the path to the folder you want to print the structure of
# folder_path = 'C:\\Users\\Admin\\Desktop\\Attendance_via_QR_&_face_recognition'

# # Call the function to print the directory structure
# print_directory_structure(folder_path)

# import logging

# # Configure basic logging settings
# logging.basicConfig(level=logging.DEBUG,  # Set the threshold level for logging
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# # Create a logger object
# logger = logging.getLogger("MyLogger")

# # Log messages
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")



# nested if

a = int(input("Enter a value : "))
b = int(input("Enter a value : "))
c = int(input("Enter a value : "))
print(f"a = {a}, b = {b}, c = {c}")

if a > b: 
    if a > c :
        print(f"{a} is greatest")
    else:
        print(f"{c} is greatest")
else: 
    if b > c:
        print(f"{b} is greatest")
    else:
        print(f"{c} is greatest")

import os

# Directory containing the HTML files
directory = "C:/webstuff/sonofcauvery/html"  # Update this path if necessary

# Favicon HTML lines to insert
favicon_html = '''
<link rel="icon" type="image/png" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
'''

# Insert favicon HTML into all HTML files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Check if favicon is already present
        if 'favicon' not in content:
            # Insert favicon HTML just before the closing </head> tag
            content = content.replace("</head>", favicon_html + "\n</head>")

            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
        print(f"Updated {filename}")

print("All HTML files updated with favicon.")

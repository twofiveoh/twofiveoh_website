import os

directory = "../src/episode"

for filename in os.listdir(directory):
    fullfilename = os.path.join(directory, filename)
    print(f'trying to open {fullfilename}')
    if (filename.endswith('.md') and os.path.isfile(fullfilename)):
        with open(fullfilename, 'r+') as file: 
            contents = file.read()
            contents = contents.replace('https://open.spotify.com/show/39lr9bBUcXgZRXsxTw1axM', '')
            file.close()

        with open(fullfilename, 'w') as file:
            file.write(contents)
            file.close()

        

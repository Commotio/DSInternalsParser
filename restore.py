import os
import sys

# File paths
userfile = "output_ntlm.txt"
hashfile = "cracked.txt"
outputfile = "crackedusers.txt"

# Check if files exist
for file in [userfile, hashfile]:
    if not os.path.isfile(file):
        print(f"Error: File {file} does not exist.")
        sys.exit(1)

# Initialize hash-password map
hash_password_map = {}

# Read the hash-password file and populate the map
with open(hashfile, 'r') as hf:
    for line in hf:
        parts = line.strip().split(':', 1)
        if len(parts) == 2:
            hash, password = parts
            hash = hash.strip()
            password = password.strip()
            if hash and password:
                hash_password_map[hash] = password
            else:
                print(f"Warning: Skipping invalid entry in {hashfile}: '{line.strip()}'")

# Process the userfile and write results
total_lines = sum(1 for line in open(userfile, 'r'))
current_line = 0

with open(userfile, 'r') as uf, open(outputfile, 'w') as of:
    for line in uf:
        parts = line.strip().split(':', 1)
        if len(parts) == 2:
            username, hash = parts
            username = username.strip()
            hash = hash.strip()
            if username and hash:
                password = hash_password_map.get(hash)
                if password:
                    of.write(f"{username}:hash:{password}\n")

        # Update progress bar
        current_line += 1
        percent = (current_line * 100) // total_lines
        progress = f"{percent:3d}%"
        sys.stdout.write(f"\rProcessing: {progress}")
        sys.stdout.flush()

# Print newline after progress bar completion
print(f"\nPassword assignment completed. Check the {outputfile} for results.")

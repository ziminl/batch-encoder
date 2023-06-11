







import random
import string
import io
import base64
print()

def log(str):
    print("-> " + str)

infile = "in.bat"
outfile = "out.cmd"
log(f"In File: {infile}")
log(f"Out File: {outfile}")

tra_charvar_rename = True  # Replaces each character with a variable, windows is weird and then evaluates the contents, makes the code VERY difficult to manually reverse
tra_uselesscode_troll = True  # adds useless code statements (obfuscated too) to slow manual reversal
tra_base64_encode = True  # New method: Base64 encoding
obf_charset = string.ascii_letters  # complicated, just leave it unless you know what you are doing
obf_varmin = 69  # minimum variable length - more than 50 or it might have duplicates
obf_varmax = 420  # maximum variable length - less than 1000 or it might crash
obf_add_cmds_chance = 100  # chance of a 'junk event' triggering every line in % (100 is always 0 is never)
obf_add_cmds_times = 10  # how many lines junk to add when a 'junk event' triggers
obf_add_cmds_list = [
    "cmd /c echo>nul Nope",
    "echo>nul Nop",
    "cd>nul",
    "post ponepost ponepost ponepost ponepost pone"
]

def random_string_generator(min, max):
    return ''.join(random.choice(obf_charset) for x in range(random.randrange(min, max)))
lines_raw = []
lines_pre = []
lines_obf = []
lines_final = []
headers = []
mappings = {}

log("Reading InFile")
lines_raw = open(infile).readlines()
log("Cleaning")
for line in lines_raw:
    lines_pre.append(line.strip())

log(f"Generating Mappings ({str(len(obf_charset))} items)")
for char in obf_charset:
    mp = random_string_generator(obf_varmin, obf_varmax)
    mappings[char] = mp
    headers.append(f"set {mp}={char}")
log("Done!")
log("Obfuscating Code using mappings")
ignore = string.digits + string.whitespace + string.punctuation

def obfuscate(line):
    obfl = ""
    for char in line:
        if not char in ignore:
            obfl = obfl + f"%{mappings[char]}%"
        else:
            obfl = obfl + char
    return obfl
  
def base64_encode(line):
    encoded = base64.b64encode(line.encode('utf-8')).decode('utf-8')
    return f"certutil -decode {encoded} temp.bat & type temp.bat & del /f /q temp.bat"

for line in lines_pre:
    if line.startswith("rem "):
        continue
    if tra_charvar_rename:
        lines_obf.append(obfuscate(line))
    if tra_uselesscode_troll:
        num = random.randrange(0, 100)
        if num < obf_add_cmds_chance:
            for i in range(obf_add_cmds_times):
                lines_obf.append(obfuscate(random.choice(obf_add_cmds_list)))
    if tra_base64_encode:
        lines_obf.append(base64_encode(line))  # Adding base64-encoded version of each line

log(f"Obfuscated {str(len(lines_pre))} Lines")
mark = [
    "bat obfuscator by z"
    "@echo off"
]
lines_final = mark + headers + lines_obf
log(f"Writing to {outfile}")
with io.open(outfile, "w", encoding="utf-8") as f:
    for line in lines_final:
        f.write(line + "\n")
print()
log("done")












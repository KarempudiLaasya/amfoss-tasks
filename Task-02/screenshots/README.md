## Level 1

the task was to find a Devil Fruit that can be awakened and recover the awakening signature.

There were many Devil Fruit files in different sectors.at first I checked the files, but the important thing was not the name or timestamp. I checked the `eat.sh` script to understand what it actually looks for. The script checks if the given fruit file is writable using `-w`. If it is writable, the fruit is accepted and the script decrypts the hidden message using OpenSSL.

### Commands used

```bash
cd GrandLine/Loguetown_Reef
ls -la
cd sector_A
ls -la
cd ../sector_B
ls -la
cd ../sector_C
ls -la
cd ../sector_D
ls -la
cd ..
cat eat.sh
./eat.sh <writable_fruit_file>

```

## Level 2

the task was to investigate whiskey peak and find the hidden clue

For Level 2, I first checked the git history and branches to find the hidden investigation for Whiskey Peak. From there I found the Level 2 implementation and the hidden `unlock_vault.sh` script. The script takes the awakening signature from Level 1 and checks its SHA-256 hash with the target hash. Once it matches, the same signature is used as the password to decrypt the encrypted flag. The script then creates two identical log files and replaces line 42 in `bounty_hunter_feed.log` with the decrypted flag. By comparing the two files using `diff`, the changed line can be seen and the Level 2 flag is obtained.

### Commands used

```bash
git branch -a
git log --oneline origin/whiskey_peak_investigation
git show bc5aff3 --name-only
git show bc5aff3
cd GrandLine/Whiskey_Peak/.baroque_works_cache
cat unlock_vault.sh
export AWAKENING_SIGNATURE="ONE_PIECE{GITO_GITO_NO_AWAKENING}"
./unlock_vault.sh
diff -u marine_intercept.log bounty_hunter_feed.log
```

clue = BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}



## Level 3

the task was to find the hidden genuine transmission report among the many decoy reports.

The Wax_Jungle folder contained a large number of report files which were all over different folders. Most of them were decoys. The genuine report contained the Level 2 Executive Transmission Code in its broadcast representation. I converted my Level 2 code into Base64 and searched for it across the files. The matching file was the genuine report.

### Commands used

```bash
git fetch origin
git checkout little_garden
cd GrandLine/Wax_Jungle
echo "BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}" | base64
grep -rl "<the base 64 string>" .
cat <file that matched>
```

at the end I recovered the first cipher fragment

```text
PONEGLYPH_FRAGMENT_I = "KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL"
```

## Level 4

the task was to find the hidden blueprint by checking the true type of the file and extracting its layers.

the problem was that the files had no extensions so I used the `file` command to find out what it actually was. I kept checking the extracted files and uncompressed them. The file turned out to contain a gzip layer, then a tar archive, and then a zip archive. After extracting the zip, there were two things to inspect. `hull_design` was a decoy, while `secret_link.txt` contained the actual content needed for the level.

as a result got the second fragment

```text
PONEGLYPH_FRAGMENT_II="SwnbzptDiM3JSpvFiMuJ28PJzA1J28VIzA="
```

### commands used

```bash
cd GrandLine/Water_7/galley_la_company
file puffing_tom_blueprints
cp puffing_tom_blueprints step1.gz
gunzip step1.gz
file step1
mv step1 step2.tar
tar -xf step2.tar
file step1_blueprints.zip
unzip step1_blueprints.zip
ls -la blueprints_extracted
file blueprints_extracted/*
cat secret_link.txt
```

## Level 5
in this task we were asked to recover the missing files from git history and find the real decoder needed to combine the cipher fragments.but the problem was the current timeline had already gone through the Buster Call, so important files were deleted. so I used the `alternate_timeline` branch and checked the Git history to find a commit from before the files were removed. After going back to that commit, I searched through the vaults and checked the decoder scripts.Most of them were decoys, but there was a hidden `.cp9_secure_vault/poneglyph.py` file. It takes the two cipher fragments, decodes the combined value and gives the next step.

### Commands used

```bash
git checkout alternate_timeline
git log --oneline
git checkout <the commit hash>
ls GrandLine/Enies_Lobby
find . -type f
cat vault_1/decode.sh
cat .cp9_secure_vault/poneglyph.py
python3 .cp9_secure_vault/poneglyph.py
```

as a result a new git repo url was found https://github.com/rogueone-x/Laugh-Tale-Merge-War

## Level 6
the final task was to merge the two conflicting git timelines and recover the final password.The new repository had two branches, ancient_history and pirate_king_path.each branch contained only part of the information needed for the final password.I had to merge the branches instead of choosing only one side.This caused merge conflicts in the two key files, so I opened them, removed the Git conflict markers and combined the content from both branches.After resolving the conflicts, I added the files and completed the merge.then I ran the final script and entered the reconstructed password.

### Commands used

```bash
git clone https://github.com/rogueone-x/Laugh-Tale-Merge-War.git
cd Laugh-Tale-Merge-War
git fetch origin
git checkout -b ancient_history origin/ancient_history
git checkout -b pirate_king_path origin/pirate_king_path
git checkout ancient_history
git merge pirate_king_path
nano treasure/key_part_1.txt
nano treasure/key_part_2.txt
git add treasure/key_part_1.txt treasure/key_part_2.txt
git commit -m "merge"
chmod +x victory.sh
./victory.sh
```

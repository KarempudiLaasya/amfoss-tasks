//log book is created to record clues and stuff
The goal of the //LEVEL-1 OF TASK-02 was to find the real fruit among many fake ones
There was a hint given in question stating "Your journey begins where many great pirate legends began...Loguetown."
hence i did cd Loguetown
listed items in it with ls -la to get files and directories,permissions,file size,timestamps etc..
it had four sectors in it
sector_A
sector_B
sector_C
sector_D
i went through all of them through cd command and used ls -la in each one of them and compared the files 
in sector c a unique permission was given to a file in it with the name devil_fruit_6.txt
hence used the command ./eat.sh on it which revealed the first clue ONE_PIECE{GITO_GITO_NO_AWAKENING}
//LEVEL-2 OF TASK-02
commands used:
git log --graph --oneline --all
git show
git diff
export AWAKENING_SIGNATURE="ONE_PIECE{...}"   
echo $AWAKENING_SIGNATURE                     
Using git log i went through the repos history and looked for suspicious commits.later did git show hash of suspicious commit.exported the key of first level into environment variable and used to decrypt the flag
//LEVEL-3 OF TASK-02
Commands used:
git branch -a
git checkout little_garden
find GrandLine/Wax_Jungle -type f -name "*.log"
find GrandLine/Wax_Jungle -type f -name "*.log" | xargs -I{} sh -c 'sort -u "{}"' | sort | uniq -c | sort -rn
grep -rl "QkFST1FVRV9ESUFMe1NQTElUX1RJTUVMSU5FX01JU0RJUkVDVElPTn0K" GrandLine/Wax_Jungle
cat <path-to-agent_manifest.log>
base64 -d
Initially the Wax_Jungle directory appeared almost empty because I was on the main branch.Later i have listed all branches and switched to little_garden branch.This changed my working directory and many files appeared in it.The structure i have followed to look through those many files was to first start by sort -u so to remove duplicate lines within a file then sorted them alphabetically,later used uniq-c to keep count of unique lines.ones which had the lowest count became the obvious targets for finding clues.one of the clue was base 64 encoded.when decoded,it matched the exact clue found in level-2.
grep was used in order to find the file which translated to clue from level-2 which ultimately revealed the cypher fragment PONEGLYPH_FRAGMENT_I = "KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL".

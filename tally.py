import os

jamdir = "jam0001"
votesfile = "rawvotes.txt"

teams = {}
users = {}
for teamName in os.listdir(jamdir):
    if not os.path.exists(f"{jamdir}/{teamName}/TEAM"): continue

    teamName = teamName.lower()
    team = []
    teams[teamName] = team
    with open(f"{jamdir}/{teamName}/TEAM") as f:
        for line in f:
            for name in line.split():
                name = name.strip().lower()
                if name.startswith("[delete this line"): continue
                if name == "": continue
                users[name] = teamName
                team.append(name)

tallies = []
with open(votesfile) as f:
    for line in f:
        issueName, count, voters = line[:-1].split(";")
        if not issueName.startswith("Team: "): continue
        voters = voters.strip()
        if voters == "": continue

        teamName = issueName.replace("Team: ", "")
        rawTeamName = teamName
        teamName = teamName.lower()
        voters = map(lambda x: x.strip().lower(), voters.split(":"))

        tally = 0
        for voter in voters:
            if voter not in users:
                print("Vote from non-participant:", voter, "voted for", rawTeamName)
            elif users[voter] == teamName:
                print("Self-vote:", voter, "voted for their own team", rawTeamName)
            else:
                tally += 1

        tallies.append((rawTeamName, tally))

tallies.sort(key=lambda x: x[1])
for tally in tallies:
    print(tally[0] + ": " + str(tally[1]))

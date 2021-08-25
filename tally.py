import os

jamdir = "jam0001"
votesfile = "rawvotes.txt"

teams = {}
users = {}
for realTeamName in os.listdir(jamdir):
    if not os.path.exists(f"{jamdir}/{realTeamName}/TEAM"): continue

    teamName = realTeamName.lower()
    team = {"name": teamName, "users": [], "tally": 0}
    teams[teamName] = team
    with open(f"{jamdir}/{realTeamName}/TEAM") as f:
        for line in f:
            for name in line.split():
                name = name.strip().lower()
                if name[0] == "@": name = name[1:]
                if name.startswith("[delete this line"): continue
                if name == "": continue
                users[name] = teamName
                team["users"].append(name)

with open(votesfile) as f:
    for line in f:
        issueName, count, voters = line[:-1].split(";")
        if not issueName.startswith("Team: "): continue
        voters = voters.strip()
        if voters == "": continue

        teamName = issueName.replace("Team: ", "")
        teamName = teamName.lower()
        voters = map(lambda x: x.strip().lower(), voters.split(":"))

        team = teams[teamName]
        for voter in voters:
            if voter not in users:
                print("Vote from non-participant:", voter, "voted for", team["name"])
            elif users[voter] == teamName:
                print("Self-vote:", voter, "voted for their own team", team["name"])
            else:
                team['tally'] += 1

for team in sorted(teams.values(), key=lambda team: team["tally"]):
    print(f"{team['name']}: {team['tally']}")

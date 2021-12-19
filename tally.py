import os
import re

jamdir = "../jam0002"
votesfile = "rawvotes.txt"

teams = {}
users = {}
for realTeamName in os.listdir(jamdir):
    if not os.path.exists(f"{jamdir}/{realTeamName}/TEAM"): continue

    teamId = ""
    regex = r".*/pull/(\d+)"
    with open(f"{jamdir}/{realTeamName}/README.md" if os.path.exists(f"{jamdir}/{realTeamName}/README.md") else f"{jamdir}/{realTeamName}/readme.md") as f:
        for line in f:
            teamId = re.match(regex, line).groups()[0]
            break

    team = {"id": teamId, "name": realTeamName, "users": [], "tally": 0}
    teams[teamId] = team
    with open(f"{jamdir}/{realTeamName}/TEAM") as f:
        for line in f:
            for name in line.split():
                name = name.strip().lower()
                if name[0] == "@": name = name[1:]
                if name.startswith("https://github.com/") == "@": name = name[len("https://github.com/"):]
                if name.startswith("[delete this line"): continue
                if name == "": continue
                users[name] = teamId
                team["users"].append(name)

with open(votesfile) as f:
    for line in f:
        pullId, count, voters = line[:-1].split(";")
        voters = voters.strip()
        if voters == "": continue

        voters = map(lambda x: x.strip().lower(), voters.split(":"))

        if not pullId in teams: continue
        team = teams[pullId]
        for voter in voters:
            if voter not in users:
                print("Vote from non-participant:", voter, "voted for", team["name"])
            elif users[voter] == pullId:
                print("Self-vote:", voter, "voted for their own team", team["name"])
            else:
                team['tally'] += 1

for team in sorted(teams.values(), key=lambda team: team["tally"]):
    print(f"{team['name']}: {team['tally']}")

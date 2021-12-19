let https = require("https");
let fs = require("fs");

let authorization = "Basic <insert your own base64-encoded username:token>";
let repo = "langjam/jam0002";
let outfile = "rawvotes.txt";

function get(url, accept) {
	return new Promise((resolve, reject) => {
		let headers = {
			"User-Agent": "Reactionator",
			"Accept": accept,
			"Authorization": authorization,
		};

		process.stderr.write(Buffer.from("==> GET " + url + "... ", "utf-8"));
		let req = https.get(url, { headers }, res => {
			let data = "";
			res.on("data", d => {
				data += d;
			});

			res.on("end", () => {
				if (res.statusCode != 200) {
					process.stderr.write(Buffer.from("ERR " + res.statusCode + "\n"));
					throw new Error(data);
				} else {
					process.stderr.write(Buffer.from("OK\n"));
				}

				resolve(data);
			});
		}).on("error", reject);
	});
}

function apiIssueReactions(repo, comment) {
	return `/repos/${repo}/issues/comments/${comment}/reactions`;
}

async function main(repo, stream) {
	let votes = [];
	for (let pageNum = 1; ; ++pageNum) {
		let page = JSON.parse(await get(
			`https://api.github.com/repos/${repo}/pulls?state=closed&page=${pageNum}`,
			"application/vnd.github.v3+json"));
		if (page.length == 0) {
			break;
		}

		for (let issue of page) {
			let count = 0;
			let people = [];
			for (let reactionPageNum = 1; ; ++reactionPageNum) {
				let reactionPage = JSON.parse(await get(
					`https://api.github.com/repos/${repo}/issues/${issue.number}/reactions?page=${reactionPageNum}`,
					"application/vnd.github.squirrel-girl-preview"));
				if (reactionPage.length == 0) {
					break;
				}

				for (let reaction of reactionPage) {
					if (reaction.content == "+1") {
						count += 1;
						people.push(reaction.user.login);
					}
				}
			}

			stream.write(issue.number + ";" + count + ";" + people.join(":") + "\n");
		}
	}
}

let stream = fs.createWriteStream(outfile);
main(repo, stream).then(() => stream.close());

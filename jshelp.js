let jobsQueue = require("./jobsQueue.json")
let heldJobs = JSON.parse(fs.readFileSync("./HeldJobs.json"))
for (let i = 0; i < heldJobs.length; i++) {
    let heldJob = heldJobs[i]
    for (let j = 0; j < jobsQueue.Altamore.length; j++) {
        let job = jobsQueue.Altamore[j]
        if (JSON.stringify(heldJob) === JSON.stringify(job)) {
            jobsQueue.Altamore.splice(j, 1)
            i--
            break
        }
    }
}
console.log(jobsQueue.Altamore.length, "jobs left from Altamore")
if (heldJobs.length > 0) { console.log(heldJobs.length, "jobs held") }
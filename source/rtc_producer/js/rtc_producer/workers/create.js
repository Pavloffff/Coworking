const os = require('os')
const mediasoup = require('mediasoup')
const config = require('../config/config')

const totalThreads = os.cpus().length / 2

const createWorkers = ()=>new Promise(async(resolve, reject)=>{
    let workers = []
    for (let i = 0; i < totalThreads; i++) {
        const worker = await mediasoup.createWorker({
            rtcMinPort: config.workerSettings.rtcMinPort,
            rtcMaxPort: config.workerSettings.rtcMaxPort,
            logLevel: config.workerSettings.logLevel,
            logTags: config.workerSettings.logTags,
        })
        worker.on('died',()=>{
            console.log("Worker has died")
            process.exit(1)
        })
        workers.push(worker)
    }
    resolve(workers)
})

module.exports = createWorkers

function getWorker(workers) {
    return new Promise(async(resolve, reject)=>{
        const workersLoad = workers.map(worker=>{
            return new Promise(async(resolve, reject)=>{
                const stats = await worker.getResourceUsage();
                const cpuUsage = stats.ru_utime + stats.ru_stime;
                resolve(cpuUsage)
            })
        })
        const workersLoadCalc = await Promise.all(workersLoad)
        let leastLoadedWorker = 0;
        let leastWorkerLoad = 0
        for(let i = 0; i < workersLoadCalc.length; i++){
            if(workersLoadCalc[i] < leastWorkerLoad){
                leastLoadedWorker = i
            }
        }
        resolve(workers[leastLoadedWorker])
    })
}

module.exports = getWorker

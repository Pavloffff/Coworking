const config = require('../config/config')
const newDominantSpeaker = require('../speakers/create')

class Channel {
    constructor(name, worker) {
        this.name = name
        this.worker = worker
        this.router = null
        this.clients = []
        this.activeSpeakerList = []
    }
    addClient(client) {
        this.clients.push(client)
    }
    createRouter(io) {
        return new Promise(async(resolve, reject)=>{
            this.router = await this.worker.createRouter({
                mediaCodecs: config.routerMediaCodecs
            })
            this.activeSpeakerObserver = await this.router.createActiveSpeakerObserver({
                interval: 300 //300 is default
            })
            this.activeSpeakerObserver.on('dominantspeaker', ds=>newDominantSpeaker(ds,this,io))
            resolve()
        })
    }
}

module.exports = Channel

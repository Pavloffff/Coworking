const updateActiveSpeakers = require("./update")

function newDominantSpeaker(ds, channel, io) {
    console.log('dominant speaker', ds.producer.id)
    const i = channel.activeSpeakerList.findIndex(pid=>pid === ds.producer.id)
    if(i > -1) {
        const [ pid ] = channel.activeSpeakerList.splice(i,1)
        channel.activeSpeakerList.unshift(pid)
    } else{
        channel.activeSpeakerList.unshift(ds.producer.id)
    }
    console.log(channel.activeSpeakerList)
    const newTransportsByPeer = updateActiveSpeakers(channel,io)
    for(const [socketId, audioPidsToCreate] of Object.entries(newTransportsByPeer)){
        const videoPidsToCreate = audioPidsToCreate.map(aPid=>{
            const producerClient = channel.clients.find(c=>c?.producer?.audio?.id === aPid)
            return producerClient?.producer?.video?.id
        })
        const associatedUserNames = audioPidsToCreate.map(aPid=>{
            const producerClient = channel.clients.find(c=>c?.producer?.audio?.id === aPid)
            return producerClient?.userName
        })
        io.to(socketId).emit('newProducersToConsume', {
            routerRtpCapabilities: channel.router.rtpCapabilities,
            audioPidsToCreate,
            videoPidsToCreate,
            associatedUserNames,
            activeSpeakerList: channel.activeSpeakerList.slice(0,5)
        })
    }
}

module.exports = newDominantSpeaker

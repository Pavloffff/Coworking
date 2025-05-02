const config = require('../config/config')

class Client {
    constructor(name, socket) {
        this.name = name
        this.socket = socket
        this.upstreamTransport = null
        this.producer = {}
        this.downstreamTransports = []
        this.channel = null
    }
    addTransport(type, audioPid = null, videoPid = null) {
        return new Promise(async(resolve, reject)=>{
            const { listenIps, initialAvailableOutgoingBitrate, maxIncomingBitrate} = config.webRtcTransport
            const transport = await this.channel.router.createWebRtcTransport({
                enableUdp: true,
                enableTcp: true,
                preferUdp: true,
                listenInfos: listenIps,
                initialAvailableOutgoingBitrate,
            })

            if (maxIncomingBitrate) {
                try{
                    await transport.setMaxIncomingBitrate(maxIncomingBitrate)
                } catch (err) {
                    console.log("Error setting bitrate")
                    console.log(err)
                }
            }

            const clientTransportParams = {
                id: transport.id,
                iceParameters: transport.iceParameters,
                iceCandidates: transport.iceCandidates,
                dtlsParameters: transport.dtlsParameters,
            }

            if(type === "producer") {
                this.upstreamTransport = transport
            } else if (type === "consumer") {
                this.downstreamTransports.push({
                    transport,
                    associatedVideoPid: videoPid,
                    associatedAudioPid: audioPid,
                })
            }
            resolve(clientTransportParams)
        })
    }
    addProducer(kind,newProducer) {
        this.producer[kind] = newProducer
        if (kind === "audio") {
            this.channel.activeSpeakerObserver.addProducer({
                producerId: newProducer.id
            })
        }
    }
    addConsumer(kind,newConsumer,downstreamTransport) {
        downstreamTransport[kind] = newConsumer
    }
}

module.exports = Client

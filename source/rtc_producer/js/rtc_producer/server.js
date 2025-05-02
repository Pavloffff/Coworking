const fs = require('fs')
const https = require('https')
const http = require('http')
const cors = require('cors')

const express = require('express')
const app = express()

app.use(cors({
    origin: '*',
    methods: '*',
    allowedHeaders: '*',
    exposedHeaders: '*'
}))

app.use(express.static('public'))

// const key = fs.readFileSync('./config/cert.key')
// const cert = fs.readFileSync('./config/cert.crt')
// const options = {key,cert}

// const httpsServer = https.createServer(options, app)
const httpServer = http.createServer(app)
const socketio = require('socket.io')
const config = require('./config/config')

const Client = require('./types/client')
const Channel = require('./types/channel')

const createWorkers = require('./workers/create')
const getWorker = require('./workers/get')
const updateSpeakers = require('./speakers/update')

const io = socketio(httpServer,{
    cors: {
        origin: "*",
        methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allowedHeaders: ["*"],
        credentials: true
    }
})

let workers = null
// TODO redis
const channels = []

const initMediaSoup = async()=>{
    workers = await createWorkers()
}

initMediaSoup()

io.on('connect', socket=>{
    let client;

    // изменить room на channel
    socket.on('joinRoom', async({userName, channelName}, ackCb)=>{
        let newChannel = false
        client = new Client(userName, socket)
        let requestedChannel = channels.find(channel => channel.name === channelName)
        if (!requestedChannel) {
            newChannel = true
            client = new Client(userName, socket)
            const workerToUse = await getWorker(workers)
            requestedChannel = new Channel(channelName, workerToUse)
            await requestedChannel.createRouter(io)
            channels.push(requestedChannel)
        }
        client.channel = requestedChannel
        client.channel.addClient(client)
        socket.join(client.channel.name)

        const audioPidsToCreate = client.channel.activeSpeakerList.slice(0,5)
        
        // убрать видео
        const videoPidsToCreate = audioPidsToCreate.map(aid=>{
            const producingClient = client.channel.clients.find(c=>c?.producer?.audio?.id === aid)
            return producingClient?.producer?.video?.id
        })

        const associatedUserNames = audioPidsToCreate.map(aid=>{
            const producingClient = client.channel.clients.find(c=>c?.producer?.audio?.id === aid)
            return producingClient?.name
        })

        // убрать видео
        ackCb({
            routerRtpCapabilities: client.channel.router.rtpCapabilities,
            newChannel,
            audioPidsToCreate,
            videoPidsToCreate,
            associatedUserNames
        })
    })
    socket.on('requestTransport',async({type, audioPid}, ackCb)=>{
        let clientTransportParams
        if(type === "producer"){
            clientTransportParams = await client.addTransport(type)
        }else if(type === "consumer"){
            const producingClient = client.channel.clients.find(c=>c?.producer?.audio?.id === audioPid)
            // убрать видео
            const videoPid = producingClient?.producer?.video?.id
            clientTransportParams = await client.addTransport(type, audioPid, videoPid)
        }
        ackCb(clientTransportParams)
    })
    socket.on('connectTransport',async({dtlsParameters, type, audioPid}, ackCb)=>{
        if (type === "producer") {
            try {
                await client.upstreamTransport.connect({dtlsParameters}) 
                ackCb("success")               
            } catch(error){
                console.log(error)
                ackCb('error')
            }
        } else if(type === "consumer") {
            try {
                const downstreamTransport = client.downstreamTransports.find(t=>{
                    return t.associatedAudioPid === audioPid
                })
                downstreamTransport.transport.connect({dtlsParameters})
                ackCb("success")
            } catch(error) {
                console.log(error)
                ackCb("error")
            }
        }
    })
    socket.on('startProducing',async({kind,rtpParameters},ackCb)=>{
        try {
            const newProducer = await client.upstreamTransport.produce({kind,rtpParameters})
            client.addProducer(kind,newProducer)
            if (kind === "audio") {
                client.channel.activeSpeakerList.push(newProducer.id)
            }
            ackCb(newProducer.id)
        } catch(err) {
            console.log(err)
            ackCb(err)
        }

        const newTransportsByPeer = updateSpeakers(client.channel, io)
        for (const [socketId, audioPidsToCreate] of Object.entries(newTransportsByPeer)) {
            const videoPidsToCreate = audioPidsToCreate.map(aPid=>{
                const producerClient = client.channel.clients.find(c=>c?.producer?.audio?.id === aPid)
                return producerClient?.producer?.video?.id
            })
            const associatedUserNames = audioPidsToCreate.map(aPid=>{
                const producerClient = client.channel.clients.find(c=>c?.producer?.audio?.id === aPid)
                return producerClient?.name
            })
            io.to(socketId).emit('newProducersToConsume', {
                routerRtpCapabilities: client.channel.router.rtpCapabilities,
                audioPidsToCreate,
                videoPidsToCreate,
                associatedUserNames,
                activeSpeakerList: client.channel.activeSpeakerList.slice(0,5)
            })
        }
    })
    socket.on('audioChange',typeOfChange=>{
        if(typeOfChange === "mute") {
            client?.producer?.audio?.pause()
        } else {
            client?.producer?.audio?.resume()
        }
    })
    socket.on('consumeMedia',async({rtpCapabilities, pid, kind}, ackCb)=>{
        console.log("Kind: ", kind, "   pid:", pid)
        try {
            if (!client.channel.router.canConsume({producerId:pid, rtpCapabilities})) {
                ackCb("cannotConsume")
            } else {
                const downstreamTransport = client.downstreamTransports.find(t=>{
                    if (kind === "audio") {
                        return t.associatedAudioPid === pid
                    } else if (kind === "video") {
                        return t.associatedVideoPid === pid
                    }
                })
                const newConsumer = await downstreamTransport.transport.consume({
                    producerId: pid,
                    rtpCapabilities,
                    paused: true
                })
                client.addConsumer(kind,newConsumer,downstreamTransport)
                const clientParams = {
                    producerId: pid,
                    id: newConsumer.id,
                    kind: newConsumer.kind,
                    rtpParameters: newConsumer.rtpParameters
                }
                ackCb(clientParams)
            }
        } catch(err) {
            console.log(err)
            ackCb('consumeFailed')
        }
    })
    socket.on('unpauseConsumer',async({pid,kind}, ackCb)=>{
        const consumerToResume = client.downstreamTransports.find(t=>{
            return t?.[kind].producerId === pid
        })
        await consumerToResume[kind].resume()
        ackCb()
    })
})

// httpsServer.listen(config.port)
httpServer.listen(config.port, '0.0.0.0', () => {
  console.log(`Server running on 0.0.0.0:${config.port}`)
})

import { AxiosResponse } from 'axios'
import { VoiceChannelModel } from '../types'
import { handleApiRequest } from '../apiHandler'
import databaseReaderApiClient from '../databaseReaderClient'
import serversConfiguratorApiClient from '../serversConfiguratorClient'

export const voiceChannelsApi = {
	getServerVoiceChannels: async (
		server_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<VoiceChannelModel[]>> => {
		return handleApiRequest<VoiceChannelModel[]>({
			method: 'get',
			url: `voice-channels/server?server_id=${server_id}`,
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
	addVoiceChannel: async (
		server_id: number,
		name: string,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<VoiceChannelModel>> => {
		return handleApiRequest<VoiceChannelModel>({
			method: 'post',
			url: 'voice-channels/add',
			data: {
				voice_channel_id: 0,
				name: name,
				server_id: server_id,
			},
			access_token,
			refresh_token,
			apiClient: serversConfiguratorApiClient,
		})
	},
	getCurrentVoiceChannel: async (
		server_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<VoiceChannelModel>> => {
		return handleApiRequest<VoiceChannelModel>({
			method: 'get',
			url: `/voice-channels/${server_id}`,
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
}

import { AxiosResponse } from 'axios'
import { VoiceItemModel, VoiceItemScheme } from '../types'
import { handleApiRequest } from '../apiHandler'
import databaseReaderApiClient from '../databaseReaderClient'
import serversConfiguratorApiClient from '../serversConfiguratorClient'

export const voiceItemsApi = {
	getVoiceChannelsVoiceItems: async (
		voice_channel_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<VoiceItemScheme[]>> => {
		return handleApiRequest<VoiceItemScheme[]>({
			method: 'get',
			url: `voice-items/voice-channel?voice_channel_id=${voice_channel_id}`,
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
	addVoiceItem: async (
		voice_item_id: number,
		user_id: number,
		voice_channel_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<VoiceItemModel>> => {
		return handleApiRequest<VoiceItemScheme>({
			method: 'post',
			url: 'voice-items/add',
			data: {
				voice_item_id: voice_item_id || 0,
				user_id: user_id,
				voice_channel_id: voice_channel_id,
			},
			access_token,
			refresh_token,
			apiClient: serversConfiguratorApiClient,
		})
	},
}

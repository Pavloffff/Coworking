import { AxiosResponse } from 'axios'
import { TextChannelModel } from '../types'
import { handleApiRequest } from '../apiHandler'
import databaseReaderApiClient from '../databaseReaderClient'
import serversConfiguratorApiClient from '../serversConfiguratorClient'

export const textChannelsApi = {
	getServerTextChannels: async (
		server_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<TextChannelModel[]>> => {
		return handleApiRequest<TextChannelModel[]>({
			method: 'get',
			url: `text-channels/server?server_id=${server_id}`,
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
	addTextChannel: async (
		server_id: number,
		name: string,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<TextChannelModel>> => {
		return handleApiRequest<TextChannelModel>({
			method: 'post',
			url: 'text-channels/add',
			data: {
				text_channel_id: 0,
				name: name,
				server_id: server_id,
			},
			access_token,
			refresh_token,
			apiClient: serversConfiguratorApiClient,
		})
	},
	getCurrentTextChannel: async (
		server_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<TextChannelModel>> => {
		return handleApiRequest<TextChannelModel>({
			method: 'get',
			url: `/text-channels/${server_id}`,
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
}

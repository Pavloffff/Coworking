import { AxiosResponse } from 'axios'
import { ServerModel, ServerScheme } from '../types'
import databaseReaderApiClient from '../databaseReaderClient'
import { handleApiRequest } from '../apiHandler'
import serversConfiguratorApiClient from '../serversConfiguratorClient'

export const serversApi = {
	getUserServers: async (
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<ServerModel[]>> => {
		return handleApiRequest<ServerModel[]>({
			method: 'get',
			url: '/servers/user',
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
	addServer: async (
		name: string,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<ServerScheme>> => {
		return handleApiRequest<ServerScheme>({
			method: 'post',
			url: '/servers/add',
			data: {
				server_id: 0,
				name: name,
				owner: {
					user_id: 0,
					name: '',
					email: '',
					tag: 0,
					password_hash: '',
					password_salt: '',
					avatar_url: '',
				},
			},
			access_token,
			refresh_token,
			apiClient: serversConfiguratorApiClient,
		})
	},
	getCurrentServer: async (
		server_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<ServerModel>> => {
		return handleApiRequest<ServerModel>({
			method: 'get',
			url: `/servers/${server_id}`,
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
}

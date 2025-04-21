import { AxiosResponse } from 'axios'
import { User, UserData } from '../types'
import { handleApiRequest } from '../apiHandler'
import databaseReaderApiClient from '../databaseReaderClient'
import serversConfiguratorApiClient from '../serversConfiguratorClient'

export const userApi = {
	getCurrentUser: async (
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<User>> => {
		return handleApiRequest<User>({
			method: 'get',
			url: 'users/current',
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
	getServerUsers: async (
		server_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<User[]>> => {
		return handleApiRequest<User[]>({
			method: 'get',
			url: `users/server_id?server_id=${server_id}`,
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
	addServerUser: async (
		server_id: number,
		user_data: string,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<UserData>> => {
		return handleApiRequest<UserData>({
			method: 'post',
			url: 'user-servers/add',
			data: {
				server_id: server_id,
				user_data: user_data,
			},
			access_token,
			refresh_token,
			apiClient: serversConfiguratorApiClient,
		})
	},
}

import { AxiosResponse } from 'axios'
import { User } from '../types'
import { handleApiRequest } from '../apiHandler'
import databaseReaderApiClient from '../databaseReaderClient'

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
}

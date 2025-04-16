import { AxiosResponse } from 'axios'
import databaseReaderApiClient from '../databaseReaderClient'
import serversConfiguratorApiClient from '../serversConfiguratorClient'
import { User, AddUserResponse, AuthResponse } from '../types'

export const authApi = {
	login: (request: User): Promise<AxiosResponse<AuthResponse>> => {
		return databaseReaderApiClient.post('/users/login', {
			...request,
			user_id: request.user_id || 0,
			tag: request.tag || 0,
			avatar_url: request.avatar_url || '',
			name: request.name || '',
			password_salt: request.password_salt || '',
		})
	},

	refresh: (request: AuthResponse): Promise<AxiosResponse<AuthResponse>> => {
		return databaseReaderApiClient.post('/users/refresh', {
			...request,
		})
	},

	register: (request: User): Promise<AxiosResponse<AddUserResponse>> => {
		return serversConfiguratorApiClient.post('/users/add', {
			...request,
			tag: request.tag || 0,
			avatar_url: request.avatar_url || '',
			password_salt: request.password_salt || '',
		})
	},
}

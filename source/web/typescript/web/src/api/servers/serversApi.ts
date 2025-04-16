import { AxiosResponse } from 'axios'
import { ServerModel } from '../types'
import databaseReaderApiClient from '../databaseReaderClient'
import Cookies from 'js-cookie'

export const serversApi = {
	getUserServers: async (
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<ServerModel[]>> => {
		try {
			return databaseReaderApiClient.get('/servers/user', {
				headers: {
					Authorization: `Bearer ${access_token}`,
				},
			})
		} catch (error) {
			console.log(error)
			const refresh_response = await databaseReaderApiClient.post(
				'/users/refresh',
				{
					access_token,
					refresh_token,
				}
			)
			const { access, refresh } = refresh_response.data
			Cookies.set('access_token', access, { expires: 1 })
			Cookies.set('refresh_token', refresh, { expires: 7 })
			return databaseReaderApiClient.get('/servers/user', {
				headers: {
					Authorization: `Bearer ${access_token}`,
				},
			})
		}
	},
}

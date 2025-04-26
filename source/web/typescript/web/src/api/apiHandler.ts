import axios, { AxiosInstance, AxiosResponse } from 'axios'
// import Cookies from 'js-cookie'
import databaseReaderApiClient from './databaseReaderClient'

interface ApiRequestConfig {
	method: 'get' | 'post' | 'put' | 'delete'
	url: string
	access_token: string
	refresh_token: string
	data?: unknown
	apiClient: AxiosInstance
	authRefreshPath?: string
}

export async function handleApiRequest<T>(
	config: ApiRequestConfig
): Promise<AxiosResponse<T>> {
	try {
		return await config.apiClient({
			method: config.method,
			url: config.url,
			data: config.data,
			headers: {
				Authorization: `Bearer ${config.access_token}`,
				...(config.data instanceof FormData
					? {}
					: { 'Content-Type': 'application/json' }),
			},
		})
	} catch (error) {
		if (isTokenExpiredError(error)) {
			const newTokens = await refreshTokens({
				apiClient: config.apiClient,
				access_token: config.access_token,
				refresh_token: config.refresh_token,
				authRefreshPath: config.authRefreshPath || '/users/refresh',
			})

			// Повторяем исходный запрос с новым токеном
			return config.apiClient({
				method: config.method,
				url: config.url,
				data: config.data,
				headers: {
					Authorization: `Bearer ${newTokens.access}`,
				},
			})
		}
		throw error
	}
}

async function refreshTokens(config: {
	apiClient: AxiosInstance
	access_token: string
	refresh_token: string
	authRefreshPath: string
}) {
	try {
		const response = await databaseReaderApiClient.post(
			config.authRefreshPath,
			{
				access_token: config.access_token,
				refresh_token: config.refresh_token,
			}
		)

		// Cookies.set('access_token', response.data.access, { expires: 1 })
		// Cookies.set('refresh_token', response.data.refresh, { expires: 7 })
		localStorage.setItem('access_token', response.data.access)
		localStorage.setItem('refresh_token', response.data.refresh)
		return response.data
	} catch (error) {
		console.error('Failed to refresh tokens:', error)
		throw error
	}
}

function isTokenExpiredError(error: unknown): boolean {
	return (
		axios.isAxiosError(error) &&
		error.response?.status === 401 &&
		error.response?.data?.code === 'token_not_valid'
	)
}

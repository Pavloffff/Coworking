import { AxiosResponse } from 'axios'
import { ChatItemScheme } from '../types'
import { handleApiRequest } from '../apiHandler'
import databaseReaderApiClient from '../databaseReaderClient'

export const chatItemsApi = {
	getTextChannelsChatItems: async (
		text_channel_id: number,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<ChatItemScheme[]>> => {
		return handleApiRequest<ChatItemScheme[]>({
			method: 'get',
			url: `chat-items/text-channel?text_channel_id=${text_channel_id}`,
			access_token,
			refresh_token,
			apiClient: databaseReaderApiClient,
		})
	},
	addChatItem: async (
		user_data: string,
		text_channel_id: number,
		text: string | null,
		file: File | null,
		access_token: string,
		refresh_token: string
	): Promise<AxiosResponse<ChatItemScheme>> => {
		const modelData = {
			user_data,
			text_channel_id,
			text: text || undefined,
			file_url: undefined,
		}

		const formData = new FormData()
		formData.append('model', JSON.stringify(modelData))

		if (file) {
			formData.append('file', file)
		}

		return handleApiRequest<ChatItemScheme>({
			method: 'post',
			url: 'chat-items/add',
			access_token,
			refresh_token,
			data: formData,
			apiClient: databaseReaderApiClient,
		})
	},
}
